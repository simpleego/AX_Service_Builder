// 한 폴더의 .js 파일을 차례로 모두 실행해 본다. (강사용 점검 도구)
// 예) npm run check-solutions → 정답 파일이 모두 통과하는지 확인
import { readdirSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { join } from 'node:path';

const folder = process.argv[2] ?? 'solutions';
const files = readdirSync(folder)
  .filter(f => f.endsWith('.js'))
  .sort();

let bad = 0;
for (const file of files) {
  const result = spawnSync(process.execPath, [join(folder, file)], { encoding: 'utf8' });
  const ok = result.status === 0;
  if (!ok) bad++;
  console.log(`${ok ? '통과' : '실패'}  ${folder}/${file}`);
  if (!ok && folder !== 'exercises') console.log(result.stdout + result.stderr);
}
console.log(`\n${files.length}개 파일 중 ${files.length - bad}개 통과`);
process.exitCode = bad === 0 ? 0 : 1;
