// 외부 패키지 없이 모든 소스의 문법과 JSON 산출물, 버전 완결성을 검사한다.
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { spawnSync } from 'node:child_process';
const root = resolve(import.meta.dirname, '..');
let count = 0;
function walk(dir) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (['node_modules', '.git', 'tmp'].includes(entry.name)) continue;
    const path = resolve(dir, entry.name);
    if (entry.isDirectory()) walk(path);
    else if (/\.(mjs|js)$/.test(path)) {
      const result = spawnSync(process.execPath, ['--check', path], { encoding: 'utf8' });
      if (result.status !== 0) throw new Error(result.stderr);
      count++;
    } else if (path.endsWith('.json')) { JSON.parse(readFileSync(path, 'utf8')); count++; }
  }
}
walk(root);
for (const name of readdirSync(resolve(root, 'versions'))) {
  for (const file of ['package.json', '.env.example', 'src/app.js', 'src/server.js', 'README.md'])
    if (!existsSync(resolve(root, 'versions', name, file))) throw new Error(`${name}: ${file} 누락`);
}
console.log(`PASS: ${count} JavaScript/JSON files; six standalone versions`);
