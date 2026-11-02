import { Router } from 'express';
import cookieParser from 'cookie-parser';
import { OAuth2Client } from 'google-auth-library';
import { pool, fail } from './common.js';
import { hash, randomToken, issueTokens } from './auth.js';
export const oauthRouter = Router();
oauthRouter.use(cookieParser());
oauthRouter.use((_req, res, next) => { res.set('Cache-Control', 'no-store'); next(); });
const redirectUri = process.env.GOOGLE_REDIRECT_URI || 'http://localhost:3000/api/auth/google/callback';
const cookie = { httpOnly: true, sameSite: 'lax', secure: process.env.NODE_ENV === 'production',
  path: '/api/auth/google', maxAge: 600000 };
function client() {
  if (!process.env.GOOGLE_CLIENT_ID || !process.env.GOOGLE_CLIENT_SECRET)
    throw fail(503, 'OAUTH_NOT_CONFIGURED', 'Google OAuth 환경변수를 설정하세요.');
  return new OAuth2Client(process.env.GOOGLE_CLIENT_ID, process.env.GOOGLE_CLIENT_SECRET, redirectUri);
}
oauthRouter.get('/google', async (_req, res) => {
  const oauth = client(), state = randomToken(), nonce = randomToken(), verifier = randomToken(), binding = randomToken();
  // state는 요청 연결, nonce는 ID 토큰 재전송 방지, PKCE는 인가 코드 탈취 방지를 담당한다.
  await pool.execute('INSERT INTO oauth_states(state_hash,binding_hash,nonce,verifier,expires_at) VALUES(?,?,?,?,DATE_ADD(UTC_TIMESTAMP(),INTERVAL 10 MINUTE))',
    [hash(state), hash(binding), nonce, verifier]);
  res.cookie('oauth_binding', binding, cookie);
  res.redirect(oauth.generateAuthUrl({ scope: ['openid', 'email', 'profile'], state, nonce,
    code_challenge: Buffer.from(hash(verifier), 'hex').toString('base64url'), code_challenge_method: 'S256' }));
});
oauthRouter.get('/google/callback', async (req, res) => {
  const oauth = client();
  if (typeof req.query.state !== 'string' || typeof req.cookies.oauth_binding !== 'string')
    throw fail(400, 'INVALID_STATE', 'OAuth 요청 연결 정보가 없습니다.');
  const db = await pool.getConnection();
  let state;
  try {
    await db.beginTransaction();
    const [rows] = await db.execute('SELECT * FROM oauth_states WHERE state_hash=? AND binding_hash=? AND expires_at>UTC_TIMESTAMP() FOR UPDATE',
      [hash(req.query.state), hash(req.cookies.oauth_binding)]);
    state = rows[0];
    if (!state) throw fail(400, 'INVALID_STATE', '만료되거나 이미 사용한 state입니다.');
    await db.execute('DELETE FROM oauth_states WHERE state_hash=?', [hash(req.query.state)]);
    await db.commit(); // 외부 HTTP 요청 전에 일회성 state 소비를 확정한다.
  } catch (e) { await db.rollback(); throw e; } finally { db.release(); }
  res.clearCookie('oauth_binding', { ...cookie, maxAge: undefined });
  if (req.query.error || typeof req.query.code !== 'string') throw fail(400, 'OAUTH_DENIED', 'Google 로그인이 취소되었거나 code가 없습니다.');
  let profile;
  try {
    const { tokens } = await oauth.getToken({ code: req.query.code, codeVerifier: state.verifier, redirect_uri: redirectUri });
    // 라이브러리가 Google 서명/issuer/audience/exp를 검증한다. nonce는 애플리케이션에서 비교한다.
    const ticket = await oauth.verifyIdToken({ idToken: tokens.id_token, audience: process.env.GOOGLE_CLIENT_ID });
    profile = ticket.getPayload();
    if (profile.nonce !== state.nonce || !profile.sub) throw new Error('nonce');
  } catch { throw fail(401, 'OAUTH_FAILED', 'Google 인가 코드 또는 ID 토큰 검증에 실패했습니다.'); }
  // 이메일이 같아도 로컬 계정과 자동 병합하지 않는다. 신원 식별자는 provider + sub다.
  const conn = await pool.getConnection();
  let userId;
  try {
    await conn.beginTransaction();
    const [rows] = await conn.execute("SELECT user_id FROM social_accounts WHERE provider='google' AND provider_subject=?", [profile.sub]);
    if (rows[0]) userId = rows[0].user_id;
    else {
      const [r] = await conn.execute('INSERT INTO users(email,password_hash) VALUES(NULL,NULL)');
      userId = r.insertId;
      await conn.execute("INSERT INTO social_accounts(provider,provider_subject,user_id,provider_email) VALUES('google',?,?,?)",
        [profile.sub, userId, profile.email_verified ? profile.email || null : null]);
    }
    await conn.commit();
  } catch (e) {
    await conn.rollback();
    // 최초 로그인 동시 요청은 UNIQUE 제약으로 중복 계정을 방지한 뒤 기존 연결을 조회한다.
    if (e.code !== 'ER_DUP_ENTRY') throw e;
    const [rows] = await pool.execute("SELECT user_id FROM social_accounts WHERE provider='google' AND provider_subject=?", [profile.sub]);
    if (!rows[0]) throw e;
    userId = rows[0].user_id;
  } finally { conn.release(); }
  // 프런트 없는 실습용 JSON 응답이다. 토큰을 URL 쿼리에 넣거나 Google 토큰을 앱 JWT로 쓰지 않는다.
  res.json(await issueTokens(userId));
});
