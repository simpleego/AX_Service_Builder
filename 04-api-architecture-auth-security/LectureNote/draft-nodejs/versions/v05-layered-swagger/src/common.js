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
