// 연습문제 자동 채점 도구.
// 학생은 이 파일을 고칠 필요가 없습니다. 연습문제 파일 맨 위에서 불러와 씁니다.
//
// 사용법
//   check('문제 이름', () => 내가만든함수(입력), 기대하는결과);
//   summary(); // 맨 마지막에 한 번

import { inspect, isDeepStrictEqual } from 'node:util';

let passed = 0;
let failed = 0;

/** 두 값을 "내용"으로 비교한다. (객체·배열도 안의 값이 같으면 같다고 본다) */
function same(a, b) {
  return isDeepStrictEqual(a, b);
}

function show(value) {
  if (value === undefined) return 'undefined (아직 아무것도 돌려주지 않음)';
  return inspect(value, { depth: 4, breakLength: Infinity });
}

/**
 * @param {string} name 문제 이름
 * @param {() => unknown} run 결과를 계산하는 함수 (에러가 나도 채점이 멈추지 않도록 함수로 받는다)
 * @param {unknown} expected 기대하는 결과
 */
export function check(name, run, expected) {
  let actual;
  try {
    actual = run();
  } catch (error) {
    failed++;
    console.log(`❌ ${name}\n   에러 발생: ${error.message}`);
    return;
  }

  if (same(actual, expected)) {
    passed++;
    console.log(`✅ ${name}`);
  } else {
    failed++;
    console.log(`❌ ${name}\n   기대한 값: ${show(expected)}\n   실제 값  : ${show(actual)}`);
  }
}

/** 비동기(시간이 걸리는) 문제용. await checkAsync(...) 로 쓴다. */
export async function checkAsync(name, run, expected) {
  let actual;
  try {
    actual = await run();
  } catch (error) {
    failed++;
    console.log(`❌ ${name}\n   에러 발생: ${error.message}`);
    return;
  }
  if (same(actual, expected)) {
    passed++;
    console.log(`✅ ${name}`);
  } else {
    failed++;
    console.log(`❌ ${name}\n   기대한 값: ${show(expected)}\n   실제 값  : ${show(actual)}`);
  }
}

/** 마지막에 결과를 요약한다. */
export function summary() {
  const total = passed + failed;
  console.log('\n' + '─'.repeat(40));
  if (failed === 0) {
    console.log(`🎉 ${total}문제 모두 통과! 다음 단원으로 넘어가세요.`);
  } else {
    console.log(`${total}문제 중 ${passed}개 통과, ${failed}개 남음. ❌ 표시된 문제를 다시 풀어 보세요.`);
  }
  process.exitCode = failed === 0 ? 0 : 1;
}
