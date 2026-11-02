import { Router } from 'express';
import { randomBytes, randomUUID, createHash } from 'node:crypto';
import { promisify } from 'node:util';
import { scrypt as scryptCallback, timingSafeEqual } from 'node:crypto';
import jwt from 'jsonwebtoken';
import rateLimit from 'express-rate-limit';
import { pool, config, fail, idOf } from './common.js';
const scrypt = promisify(scryptCallback);
export const hash = value => createHash('sha256').update(value).digest('hex');
export const randomToken = () => randomBytes(32).toString('base64url');
if (!config.jwtSecret || Buffer.byteLength(config.jwtSecret) < 32)
  throw new Error('JWT_SECRET에 무작위 32바이트 이상의 비밀값을 지정하세요.');

// 비밀번호는 복호화가 불가능한 scrypt + 사용자별 무작위 salt로 저장한다.
async function passwordHash(password, salt = randomBytes(16).toString('hex')) {
  return `${salt}:${Buffer.from(await scrypt(password, salt, 64)).toString('hex')}`;
}
async function matches(password, stored) {
  if (!stored) return false; // 소셜 계정은 로컬 비밀번호가 없다.
  const actual = await passwordHash(password, stored.split(':')[0]);
  return timingSafeEqual(Buffer.from(actual), Buffer.from(stored));
}
function credentials(body) {
  if (!body || typeof body.email !== 'string' || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(body.email) || body.email.length > 254 ||
      typeof body.password !== 'string' || body.password.length < 12 || body.password.length > 128)
    throw fail(400, 'VALIDATION_ERROR', '이메일과 12~128자 비밀번호가 필요합니다.');
  return { email: body.email.trim().toLowerCase(), password: body.password };
}
function accessToken(userId) {
  // 알고리즘/발급자/대상/만료를 고정한다. JWT payload에는 개인정보와 비밀을 넣지 않는다.
  return jwt.sign({ type: 'access' }, config.jwtSecret, { algorithm: 'HS256', subject: String(userId),
    issuer: config.issuer, audience: config.audience, expiresIn: '15m' });
}
export function requireAuth(req, _res, next) {
  try {
    const match = /^Bearer ([^ ]+)$/.exec(req.headers.authorization || '');
    if (!match) throw new Error();
    const p = jwt.verify(match[1], config.jwtSecret, { algorithms: ['HS256'], issuer: config.issuer, audience: config.audience });
    if (p.type !== 'access') throw new Error();
    req.userId = idOf(p.sub); next();
  } catch { next(fail(401, 'UNAUTHORIZED', '유효한 액세스 토큰이 필요합니다.')); }
}
export async function issueTokens(userId, db = pool, family = randomUUID(), expires = new Date(Date.now() + 7 * 86400000)) {
  const refreshToken = randomToken();
  // 리프레시 토큰 원문은 응답에서 한 번만 전달하고 DB에는 SHA-256만 보관한다.
  await db.execute('INSERT INTO refresh_tokens(token_hash,user_id,family_id,expires_at) VALUES(?,?,?,?)',
    [hash(refreshToken), userId, family, expires]);
  return { accessToken: accessToken(userId), refreshToken, tokenType: 'Bearer', expiresIn: 900 };
}
function refreshBody(body) {
  if (typeof body?.refreshToken !== 'string' || !/^[A-Za-z0-9_-]{43}$/.test(body.refreshToken))
    throw fail(400, 'VALIDATION_ERROR', 'refreshToken이 필요합니다.');
  return body.refreshToken;
}
export const authRouter = Router();
authRouter.use(rateLimit({ windowMs: 60000, limit: 30 }));
authRouter.use((_req, res, next) => { res.set('Cache-Control', 'no-store'); next(); });
authRouter.post('/register', async (req, res) => {
  const { email, password } = credentials(req.body);
  try {
    const [r] = await pool.execute('INSERT INTO users(email,password_hash) VALUES(?,?)', [email, await passwordHash(password)]);
    res.status(201).json({ id: r.insertId, email });
  } catch (e) {
    if (e.code === 'ER_DUP_ENTRY') throw fail(409, 'EMAIL_EXISTS', '이미 등록된 이메일입니다.');
    throw e;
  }
});
authRouter.post('/login', async (req, res) => {
  const { email, password } = credentials(req.body);
  const [rows] = await pool.execute('SELECT id,password_hash FROM users WHERE email=?', [email]);
  if (!rows[0] || !await matches(password, rows[0].password_hash)) throw fail(401, 'LOGIN_FAILED', '로그인에 실패했습니다.');
  res.json(await issueTokens(rows[0].id));
});
authRouter.post('/refresh', async (req, res) => {
  const token = refreshBody(req.body), db = await pool.getConnection();
  let result, rejected = false;
  try {
    await db.beginTransaction();
    // 같은 사용자에 대한 refresh/logout을 직렬화한다. 회전/재사용 검사를 하나의 트랜잭션으로 묶는다.
    const [lookup] = await db.execute('SELECT user_id FROM refresh_tokens WHERE token_hash=?', [hash(token)]);
    if (!lookup[0]) throw fail(401, 'INVALID_REFRESH', '유효하지 않은 리프레시 토큰입니다.');
    await db.execute('SELECT id FROM users WHERE id=? FOR UPDATE', [lookup[0].user_id]);
    const [rows] = await db.execute('SELECT *, expires_at > UTC_TIMESTAMP() AS alive FROM refresh_tokens WHERE token_hash=? FOR UPDATE', [hash(token)]);
    const old = rows[0];
    if (old.revoked_at || !old.alive) {
      // 폐기 토큰 재사용 시 같은 로그인 세션(family)을 모두 폐기하고 COMMIT 후 401을 보낸다.
      await db.execute('UPDATE refresh_tokens SET revoked_at=COALESCE(revoked_at,UTC_TIMESTAMP()) WHERE family_id=?', [old.family_id]);
      rejected = true;
    } else {
      await db.execute('UPDATE refresh_tokens SET revoked_at=UTC_TIMESTAMP() WHERE id=?', [old.id]);
      result = await issueTokens(old.user_id, db, old.family_id, new Date(old.expires_at + 'Z'));
    }
    await db.commit();
  } catch (e) { await db.rollback(); throw e; } finally { db.release(); }
  if (rejected) throw fail(401, 'REFRESH_REUSED_OR_EXPIRED', '토큰이 만료되었거나 재사용되었습니다. 다시 로그인하세요.');
  res.json(result);
});
authRouter.post('/logout', async (req, res) => {
  const token = refreshBody(req.body), db = await pool.getConnection();
  try {
    await db.beginTransaction();
    const [rows] = await db.execute('SELECT user_id,family_id FROM refresh_tokens WHERE token_hash=?', [hash(token)]);
    if (rows[0]) {
      await db.execute('SELECT id FROM users WHERE id=? FOR UPDATE', [rows[0].user_id]);
      await db.execute('UPDATE refresh_tokens SET revoked_at=COALESCE(revoked_at,UTC_TIMESTAMP()) WHERE family_id=?', [rows[0].family_id]);
    }
    await db.commit();
  } catch (e) { await db.rollback(); throw e; } finally { db.release(); }
  // 액세스 JWT는 15분 만료까지 살아 있다. 즉시 차단이 필요하면 별도 denylist/session 검사가 필요하다.
  res.status(204).end();
});
