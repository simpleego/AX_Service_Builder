import { useCallback, useEffect, useMemo, useReducer } from 'react';
import { todoApi } from '../api/endpoints';
import { messageOf } from '../api/messages';
import { useToast } from './useToast';

/**
 * useTodos — Todo 목록의 조회/추가/수정/삭제를 담당하는 커스텀 Hook
 *
 * 사용 Hook
 * - useReducer: 목록 상태를 action(LOADED, ADDED, UPDATED, REMOVED ...)으로 변경
 * - useEffect: 화면이 열릴 때 목록 조회, cleanup에서 AbortController로 요청 취소
 * - useCallback: 컴포넌트에 내려보내는 함수 참조 고정 (React.memo와 함께 사용)
 * - useMemo: 필터링된 목록과 통계를 items/filter가 바뀔 때만 다시 계산
 * - useContext(useToast): 실패 시 알림
 *
 * 완료 토글과 삭제는 "낙관적 업데이트": 화면을 먼저 바꾸고, 서버가 실패하면 되돌린다.
 */
const initialState = { items: [], status: 'loading', error: null, filter: 'all' };

function todosReducer(state, action) {
  switch (action.type) {
    case 'LOADING':
      return { ...state, status: 'loading', error: null };
    case 'LOADED':
      return { ...state, status: 'ready', items: action.items };
    case 'FAILED':
      return { ...state, status: 'error', error: action.error };
    case 'ADDED':
      return { ...state, items: [action.todo, ...state.items] };
    case 'UPDATED':
      return { ...state, items: state.items.map((t) => (t.id === action.todo.id ? action.todo : t)) };
    case 'REMOVED':
      return { ...state, items: state.items.filter((t) => t.id !== action.id) };
    case 'REINSERTED': // 삭제 실패 시 되돌리기 (목록은 id 내림차순)
      return { ...state, items: [...state.items, action.todo].sort((a, b) => b.id - a.id) };
    case 'SET_FILTER':
      return { ...state, filter: action.filter };
    default:
      throw new Error(`알 수 없는 action: ${action.type}`);
  }
}

export function useTodos() {
  const [state, dispatch] = useReducer(todosReducer, initialState);
  const { showToast } = useToast();

  const load = useCallback(async (signal) => {
    dispatch({ type: 'LOADING' });
    try {
      const page = await todoApi.list({ signal });
      dispatch({ type: 'LOADED', items: page.data });
    } catch (error) {
      if (error.name !== 'AbortError') dispatch({ type: 'FAILED', error: messageOf(error) });
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    load(controller.signal);
    return () => controller.abort(); // 화면을 떠나면 진행 중인 요청 취소
  }, [load]);

  const addTodo = useCallback(
    async (title) => {
      try {
        const todo = await todoApi.create(title);
        dispatch({ type: 'ADDED', todo });
        return true;
      } catch (error) {
        showToast(messageOf(error), 'error');
        return false;
      }
    },
    [showToast],
  );

  // 되돌릴 때는 인자로 받은 원래 todo를 사용하므로 items에 의존하지 않는다.
  // → 함수 참조가 고정되어 React.memo로 감싼 TodoItem이 불필요하게 다시 그려지지 않는다.
  const toggleTodo = useCallback(
    async (todo) => {
      dispatch({ type: 'UPDATED', todo: { ...todo, completed: !todo.completed } });
      try {
        dispatch({ type: 'UPDATED', todo: await todoApi.update(todo.id, { completed: !todo.completed }) });
      } catch (error) {
        dispatch({ type: 'UPDATED', todo });
        showToast(messageOf(error), 'error');
      }
    },
    [showToast],
  );

  const renameTodo = useCallback(
    async (todo, title) => {
      try {
        dispatch({ type: 'UPDATED', todo: await todoApi.update(todo.id, { title }) });
        return true;
      } catch (error) {
        showToast(messageOf(error), 'error');
        return false;
      }
    },
    [showToast],
  );

  const removeTodo = useCallback(
    async (todo) => {
      dispatch({ type: 'REMOVED', id: todo.id });
      try {
        await todoApi.remove(todo.id);
        showToast(`"${todo.title}" 삭제됨`, 'info');
      } catch (error) {
        dispatch({ type: 'REINSERTED', todo });
        showToast(messageOf(error), 'error');
      }
    },
    [showToast],
  );

  const setFilter = useCallback((filter) => dispatch({ type: 'SET_FILTER', filter }), []);

  const visibleItems = useMemo(() => {
    if (state.filter === 'active') return state.items.filter((t) => !t.completed);
    if (state.filter === 'done') return state.items.filter((t) => t.completed);
    return state.items;
  }, [state.items, state.filter]);

  const stats = useMemo(() => {
    const done = state.items.filter((t) => t.completed).length;
    return { total: state.items.length, done, active: state.items.length - done };
  }, [state.items]);

  return {
    ...state,
    visibleItems,
    stats,
    reload: load,
    addTodo,
    toggleTodo,
    renameTodo,
    removeTodo,
    setFilter,
  };
}
