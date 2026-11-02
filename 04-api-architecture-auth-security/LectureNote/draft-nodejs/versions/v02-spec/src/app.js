import { makeApp, finish } from './common.js';
import { todoRouter } from './todos.js';
const app = makeApp();
// 인증 도입 전 전용 실습 계정(1번)으로 고정한다. 이 버전은 로컬 학습 전용이다.
app.use((req,_res,next) => { req.userId=1; next(); });
app.use('/api/todos', (_req, _res, next) => next(), todoRouter);
export default finish(app);
