// 앱 구성과 서버 시작을 분리하여 통합 테스트에서 앱을 직접 불러올 수 있다.
import app from './app.js';
import { start } from './common.js';
await start(app);
