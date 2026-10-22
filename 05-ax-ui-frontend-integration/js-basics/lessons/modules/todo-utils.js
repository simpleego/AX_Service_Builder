// 08강에서 불러다 쓰는 "모듈" 파일입니다.
// export 를 붙인 것만 다른 파일에서 import 할 수 있습니다.

// 이름 붙여 내보내기 (named export): 여러 개 가능
export const PRIORITY_LABEL = { high: '높음', medium: '보통', low: '낮음' };

export function countLeft(todos) {
  return todos.filter(t => !t.done).length;
}

export function formatTodo(todo) {
  return `${todo.done ? '[x]' : '[ ]'} ${todo.title} (${PRIORITY_LABEL[todo.priority]})`;
}

// export 를 붙이지 않은 것은 이 파일 안에서만 쓴다
function secret() {
  return '밖에서는 못 씀';
}
console.log('    (todo-utils.js가 처음 불러와질 때 한 번 실행됨)', secret().length > 0);

// 기본 내보내기 (default export): 파일당 하나
export default function createTodo(title, priority = 'medium') {
  return { id: Date.now(), title, done: false, priority };
}
