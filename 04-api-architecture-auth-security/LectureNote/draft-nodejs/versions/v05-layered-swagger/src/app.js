import { makeApp, finish } from './common.js';
import { authRouter, requireAuth } from './auth.js';
import { oauthRouter } from './oauth.js';
import { todoRouter } from './todo.controller.js';
import swaggerUi from 'swagger-ui-express';
import { readFileSync } from 'node:fs';
const app = makeApp();
app.use('/api/auth', authRouter);
app.use('/api/auth', oauthRouter);
// OpenAPI 파일은 명세의 단일 원본이다. Swagger UI는 이 파일을 읽어 자동 렌더링한다.
const spec = JSON.parse(readFileSync(new URL('../openapi.json', import.meta.url)));
app.get('/openapi.json', (_req,res) => res.json(spec));
app.use('/docs', swaggerUi.serve, swaggerUi.setup(spec));
app.use('/api/todos', requireAuth, todoRouter);
export default finish(app);
