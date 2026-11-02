"""독립 실행 가능한 여섯 개 수업 버전을 생성한다. 수정 후 재실행하면 버전 소스를 덮어쓴다."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = ['v01-rest', 'v02-spec', 'v03-jwt', 'v04-oauth', 'v05-layered-swagger', 'v06-postman']

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + '\n', encoding='utf-8')

COMMON = r'''
import 'dotenv/config';
import express from 'express';
import helmet from 'helmet';
import rateLimit from 'express-rate-limit';
import mysql from 'mysql2/promise';

// 환경변수는 코드와 분리한다. 같은 스키마를 쓰되 버전별로 한 서버만 실행한다.
export const config = {
  port: Number(process.env.PORT || 3000),
  jwtSecret: process.env.JWT_SECRET,
  issuer: 'todo-api', audience: 'todo-client',
};
export const pool = mysql.createPool({
  host: process.env.DB_HOST || 'localhost', port: Number(process.env.DB_PORT || 3306),
  user: process.env.DB_USER || 'todo_app', password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME || 'todo_course', timezone: 'Z',
  connectionLimit: 10, dateStrings: true,
});
export function fail(status, code, message) {
  return Object.assign(new Error(message), { status, code });
}
// 문자열 ID를 숫자로 바꿀 때 NaN/음수/소수와 정밀도 손실을 함께 막는다.
export function idOf(value) {
  if (!/^[1-9]\d*$/.test(String(value)) || !Number.isSafeInteger(Number(value)))
    throw fail(400, 'INVALID_ID', '양의 정수 ID가 필요합니다.');
  return Number(value);
}
export function todoInput(body, partial = false) {
  if (!body || typeof body !== 'object' || Array.isArray(body))
    throw fail(400, 'VALIDATION_ERROR', 'JSON 객체가 필요합니다.');
  if (Object.keys(body).some(k => !['title', 'completed'].includes(k)))
    throw fail(400, 'VALIDATION_ERROR', 'title, completed만 입력할 수 있습니다.');
  const out = {};
  if (!partial || body.title !== undefined) {
    if (typeof body.title !== 'string' || !body.title.trim() || body.title.trim().length > 200)
      throw fail(400, 'VALIDATION_ERROR', '제목은 1~200자입니다.');
    out.title = body.title.trim();
  }
  if (body.completed !== undefined) {
    if (typeof body.completed !== 'boolean') throw fail(400, 'VALIDATION_ERROR', 'completed는 boolean입니다.');
    out.completed = body.completed;
  }
  if (partial && !Object.keys(out).length) throw fail(400, 'VALIDATION_ERROR', '수정할 필드가 없습니다.');
  return out;
}
export function makeApp() {
  const app = express();
  app.disable('x-powered-by');
  // 보안 헤더와 본문 크기 제한, 요청 제한은 공개 엔드포인트에도 적용한다.
  app.use(helmet());
  app.use(express.json({ limit: '16kb' }));
  app.use(rateLimit({ windowMs: 60000, limit: 300 }));
  app.get('/health', async (_req, res) => { await pool.query('SELECT 1'); res.json({ status: 'ok' }); });
  return app;
}
export function finish(app) {
  app.use((_req, _res, next) => next(fail(404, 'NOT_FOUND', '경로를 찾을 수 없습니다.')));
  // Express 5는 async 핸들러의 예외를 이 미들웨어로 전달한다. DB 상세는 외부에 숨긴다.
  app.use((err, _req, res, _next) => {
    const status = err.type === 'entity.parse.failed' ? 400 : err.status || 500;
    if (status >= 500) console.error(err.code || err.name);
    res.status(status).json({ error: { code: err.code || (status === 400 ? 'INVALID_JSON' : 'INTERNAL_ERROR'),
      message: status >= 500 ? '서버 오류가 발생했습니다.' : err.message } });
  });
  return app;
}
export async function start(app) {
  await pool.query('SELECT 1'); // DB가 준비되지 않았으면 서버를 열지 않고 실패시킨다.
  const server = app.listen(config.port, () => console.log(`Todo API: http://localhost:${config.port}`));
  for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => {
    server.close(async () => { await pool.end(); process.exit(0); });
  });
}
'''

REPO = r'''
import { pool } from './common.js';
const map = row => row && ({ ...row, completed: Boolean(row.completed) });
// 모든 쿼리는 바인딩 파라미터를 사용한다. owner 조건이 타인 데이터 접근을 막는다.
export const todoRepository = {
  async list(owner, limit, offset, completed) {
    const args = [owner];
    let where = 'owner_id = ?';
    if (completed !== undefined) { where += ' AND completed = ?'; args.push(completed); }
    const [rows] = await pool.query(`SELECT id, title, completed, created_at, updated_at FROM todos
      WHERE ${where} ORDER BY id DESC LIMIT ? OFFSET ?`, [...args, limit, offset]);
    return rows.map(map);
  },
  async find(owner, id) {
    const [rows] = await pool.execute('SELECT id, title, completed, created_at, updated_at FROM todos WHERE id=? AND owner_id=?', [id, owner]);
    return map(rows[0]);
  },
  async create(owner, data) {
    const [r] = await pool.execute('INSERT INTO todos(owner_id,title,completed) VALUES(?,?,?)', [owner, data.title, data.completed ?? false]);
    return this.find(owner, r.insertId);
  },
  async update(owner, id, data) {
    // SQL 필드명은 검증된 고정 목록에서만 생성한다. 사용자 문자열을 SQL에 삽입하지 않는다.
    const keys = Object.keys(data);
    await pool.execute(`UPDATE todos SET ${keys.map(k => `${k}=?`).join(',')} WHERE id=? AND owner_id=?`, [...keys.map(k => data[k]), id, owner]);
    return this.find(owner, id);
  },
  async remove(owner, id) {
    const [r] = await pool.execute('DELETE FROM todos WHERE id=? AND owner_id=?', [id, owner]);
    return r.affectedRows > 0;
  },
};
'''

SERVICE = r'''
import { todoRepository as repo } from './todo.repository.js';
import { fail, idOf, todoInput } from './common.js';
// 서비스는 HTTP 응답 객체를 몰라도 된다. 입력 규칙과 업무 규칙을 담당한다.
export const todoService = {
  async list(owner, query) {
    const page = query.page === undefined ? 1 : idOf(query.page);
    const limit = query.limit === undefined ? 20 : idOf(query.limit);
    if (limit > 100 || page > 1000000) throw fail(400, 'INVALID_PAGE', 'limit<=100, page<=1000000이어야 합니다.');
    if (query.completed !== undefined && !['true', 'false'].includes(query.completed))
      throw fail(400, 'VALIDATION_ERROR', 'completed 필터는 true 또는 false입니다.');
    return { data: await repo.list(owner, limit, (page - 1) * limit,
      query.completed === undefined ? undefined : query.completed === 'true'), page, limit };
  },
  async get(owner, value) {
    const todo = await repo.find(owner, idOf(value));
    if (!todo) throw fail(404, 'TODO_NOT_FOUND', '할 일을 찾을 수 없습니다.');
    return todo;
  },
  async create(owner, body) { return repo.create(owner, todoInput(body)); },
  async update(owner, value, body) {
    const todo = await repo.update(owner, idOf(value), todoInput(body, true));
    if (!todo) throw fail(404, 'TODO_NOT_FOUND', '할 일을 찾을 수 없습니다.');
    return todo;
  },
  async remove(owner, value) {
    if (!await repo.remove(owner, idOf(value))) throw fail(404, 'TODO_NOT_FOUND', '할 일을 찾을 수 없습니다.');
  },
};
'''

CONTROLLER = r'''
import { Router } from 'express';
import { todoService as service } from './todo.service.js';
// 컨트롤러는 HTTP 상태코드/헤더/본문 변환만 담당한다.
export const todoRouter = Router();
todoRouter.get('/', async (req, res) => res.json(await service.list(req.userId, req.query)));
todoRouter.post('/', async (req, res) => {
  const todo = await service.create(req.userId, req.body);
  res.location(`/api/todos/${todo.id}`).status(201).json(todo);
});
todoRouter.get('/:id', async (req, res) => res.json(await service.get(req.userId, req.params.id)));
todoRouter.patch('/:id', async (req, res) => res.json(await service.update(req.userId, req.params.id, req.body)));
todoRouter.delete('/:id', async (req, res) => { await service.remove(req.userId, req.params.id); res.status(204).end(); });
'''

AUTH = r'''
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
'''

OAUTH = r'''
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
'''

ENV = '''# .env로 복사 후 채운다. 실제 비밀값은 Git에 커밋하지 않는다.
PORT=3000
DB_HOST=localhost
DB_PORT=3306
DB_NAME=todo_course
DB_USER=todo_app
DB_PASSWORD=ReplaceWithYourDatabasePassword
# v03 이상 필수: node -e "console.log(require('crypto').randomBytes(48).toString('base64url'))"
JWT_SECRET=
# v04 이상 선택: Google 콘솔의 웹 애플리케이션 OAuth 클라이언트
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:3000/api/auth/google/callback
NODE_ENV=development
'''

for i, name in enumerate(VERSIONS, 1):
    base = ROOT / 'versions' / name
    deps = {'dotenv': '^16.4.7', 'express': '^5.1.0', 'express-rate-limit': '^7.5.0', 'helmet': '^8.1.0', 'mysql2': '^3.14.0'}
    if i >= 3: deps['jsonwebtoken'] = '^9.0.2'
    if i >= 4: deps.update({'cookie-parser': '^1.4.7', 'google-auth-library': '^9.15.1'})
    if i >= 5: deps['swagger-ui-express'] = '^5.0.1'
    write(base/'package.json', json.dumps({'name':name, 'version':f'{i}.0.0', 'private':True, 'type':'module',
        'engines':{'node':'>=22'}, 'scripts':{'start':'node src/server.js','dev':'node --watch src/server.js'}, 'dependencies':deps}, indent=2))
    write(base/'.env.example', ENV)
    write(base/'src/common.js', COMMON)
    if i >= 3: write(base/'src/auth.js', AUTH)
    if i >= 4: write(base/'src/oauth.js', OAUTH)
    imports = "import { makeApp, finish } from './common.js';\n"
    if i >= 3: imports += "import { authRouter, requireAuth } from './auth.js';\n"
    if i >= 4: imports += "import { oauthRouter } from './oauth.js';\n"
    setup = 'const app = makeApp();\n'
    if i >= 3: setup += "app.use('/api/auth', authRouter);\n"
    if i >= 4: setup += "app.use('/api/auth', oauthRouter);\n"
    guard = 'requireAuth' if i >= 3 else '(_req, _res, next) => next()'
    if i >= 5:
        write(base/'src/todo.repository.js', REPO)
        write(base/'src/todo.service.js', SERVICE)
        write(base/'src/todo.controller.js', CONTROLLER)
        imports += "import { todoRouter } from './todo.controller.js';\nimport swaggerUi from 'swagger-ui-express';\nimport { readFileSync } from 'node:fs';\n"
        setup += "// OpenAPI 파일은 명세의 단일 원본이다. Swagger UI는 이 파일을 읽어 자동 렌더링한다.\nconst spec = JSON.parse(readFileSync(new URL('../openapi.json', import.meta.url)));\napp.get('/openapi.json', (_req,res) => res.json(spec));\napp.use('/docs', swaggerUi.serve, swaggerUi.setup(spec));\n"
    else:
        # 앞 버전에서는 라우팅/업무/SQL을 한 파일에 놓고 v05에서 동일 동작을 계층별로 이동한다.
        write(base/'src/todos.js', "import { Router } from 'express';\nimport { pool, fail, idOf, todoInput } from './common.js';\n" +
          REPO.split("const map",1)[1].join(['const map','']) .replace('export const todoRepository', 'const todoRepository') + '\n' +
          SERVICE.split('// 서비스',1)[1].join(['// 서비스','']).replace('export const todoService', 'const todoService').replace('repo.', 'todoRepository.') + '\n' +
          CONTROLLER.split('// 컨트롤러',1)[1].join(['// 컨트롤러','']).replace('service.', 'todoService.'))
        imports += "import { todoRouter } from './todos.js';\n"
    if i < 3: setup += '// 인증 도입 전 전용 실습 계정(1번)으로 고정한다. 이 버전은 로컬 학습 전용이다.\napp.use((req,_res,next) => { req.userId=1; next(); });\n'
    setup += f"app.use('/api/todos', {guard}, todoRouter);\nexport default finish(app);"
    write(base/'src/app.js', imports+setup)
    write(base/'src/server.js', "// 앱 구성과 서버 시작을 분리하여 통합 테스트에서 앱을 직접 불러올 수 있다.\nimport app from './app.js';\nimport { start } from './common.js';\nawait start(app);")
    write(base/'README.md', f'''# {name}

{i}단계 독립 실행 스냅샷. 공통 실행/DB 준비는 루트 README.md와 docs/02-database.md를 먼저 읽으세요.

```powershell
cd versions/{name}
npm install
Copy-Item .env.example .env
# .env의 DB 비밀번호와 v03 이상 JWT_SECRET을 설정
npm start
```

이전 서버를 Ctrl+C로 종료하고 다음 버전을 실행하세요. 포트는 공통으로 3000입니다.
v01~v02는 owner_id=1 고정, v03부터는 회원가입한 사용자의 JWT로만 접근합니다.
v01~v02에서 만든 데이터가 v03 신규 사용자에게 보이지 않는 것은 소유권 분리의 정상 결과입니다.
공통 DB 스키마는 모든 버전을 지원합니다. DB 초기화는 한 번만 수행하세요.
''')

print('Generated six independent versions.')
