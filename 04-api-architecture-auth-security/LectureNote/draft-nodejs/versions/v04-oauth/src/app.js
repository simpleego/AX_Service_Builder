import { makeApp, finish } from './common.js';
import { authRouter, requireAuth } from './auth.js';
import { oauthRouter } from './oauth.js';
import { todoRouter } from './todos.js';
const app = makeApp();
app.use('/api/auth', authRouter);
app.use('/api/auth', oauthRouter);
app.use('/api/todos', requireAuth, todoRouter);
export default finish(app);
