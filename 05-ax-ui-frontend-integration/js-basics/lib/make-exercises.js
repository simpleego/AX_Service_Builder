// 강사용 도구: solutions 폴더의 정답 파일에서 "▼ ~ ▲" 사이의 답을 지워 exercises 폴더를 만든다.
// 정답을 고친 뒤에는 이 명령으로 문제 파일을 다시 만들면 둘이 항상 일치한다.
//   node lib/make-exercises.js
// ※ exercises 폴더의 같은 이름 파일을 덮어쓴다. 학생이 푼 파일이 있다면 먼저 백업할 것.
import { readdirSync, readFileSync, writeFileSync, mkdirSync, statSync } from 'node:fs';
import { join, relative, dirname } from 'node:path';

const SRC = 'solutions';
const OUT = 'exercises';

function walk(dir) {
  return readdirSync(dir).flatMap(name => {
    const path = join(dir, name);
    return statSync(path).isDirectory() ? walk(path) : [path];
  });
}

function blank(text) {
  const lines = text.split(/\r?\n/);
  const out = [];
  let inside = false;
  for (const line of lines) {
    if (line.trim() === '// ▼') {
      inside = true;
      out.push(line);
      out.push(line.replace('// ▼', '// 여기에 코드를 작성하세요'));
      continue;
    }
    if (line.trim() === '// ▲') {
      inside = false;
      out.push(line);
      continue;
    }
    if (!inside) out.push(line);
  }
  if (inside) throw new Error('▼ 와 ▲ 의 짝이 맞지 않습니다.');
  return out.join('\n');
}

let count = 0;
for (const file of walk(SRC)) {
  if (!/\.(js|html)$/.test(file)) continue;
  const target = join(OUT, relative(SRC, file));
  mkdirSync(dirname(target), { recursive: true });
  writeFileSync(target, blank(readFileSync(file, 'utf8')));
  count++;
  console.log(`만듦: ${target}`);
}
console.log(`\n문제 파일 ${count}개를 만들었습니다.`);
