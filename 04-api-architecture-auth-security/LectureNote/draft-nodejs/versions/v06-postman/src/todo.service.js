import { todoRepository as repo } from './todo.repository.js';
import { fail, idOf, todoInput } from './common.js';
// 서비스는 HTTP 응답 객체를 몰라도 된다. 입력 규칙과 업무 규칙을 담당한다.
export const todoService = {
  async list(owner, query) {
    const page = query.page === undefined ? 1 : idOf(query.page);
    const limit = query.limit === undefined ? 20 : idOf(query.limit);
    if (limit > 100 || page > 1000000) throw fail(400, 'INVALID_PAGE', 'limit<=100, page<=1000000이어야 합니다.');
    if (query.completed !== undefined && !['true', 'false'].includes(query.completed))
      throw fail(400, 'VALIDATION_ERROR', 'completed 필터는 true 또는 false입니다.');
    return { data: await repo.list(owner, limit, (page - 1) * limit,
      query.completed === undefined ? undefined : query.completed === 'true'), page, limit };
  },
  async get(owner, value) {
    const todo = await repo.find(owner, idOf(value));
    if (!todo) throw fail(404, 'TODO_NOT_FOUND', '할 일을 찾을 수 없습니다.');
    return todo;
  },
  async create(owner, body) { return repo.create(owner, todoInput(body)); },
  async update(owner, value, body) {
    const todo = await repo.update(owner, idOf(value), todoInput(body, true));
    if (!todo) throw fail(404, 'TODO_NOT_FOUND', '할 일을 찾을 수 없습니다.');
    return todo;
  },
  async remove(owner, value) {
    if (!await repo.remove(owner, idOf(value))) throw fail(404, 'TODO_NOT_FOUND', '할 일을 찾을 수 없습니다.');
  },
};
