import { Router } from 'express';
import { pool, fail, idOf, todoInput } from './common.js';
const map = row => row && ({ ...row, completed: Boolean(row.completed) });
// 모든 쿼리는 바인딩 파라미터를 사용한다. owner 조건이 타인 데이터 접근을 막는다.
const todoRepository = {
  async list(owner, limit, offset, completed) {
    const args = [owner];
    let where = 'owner_id = ?';
    if (completed !== undefined) { where += ' AND completed = ?'; args.push(completed); }
    const [rows] = await pool.query(`SELECT id, title, completed, created_at, updated_at FROM todos
      WHERE ${where} ORDER BY id DESC LIMIT ? OFFSET ?`, [...args, limit, offset]);
    return rows.map(map);
  },
  async find(owner, id) {
    const [rows] = await pool.execute('SELECT id, title, completed, created_at, updated_at FROM todos WHERE id=? AND owner_id=?', [id, owner]);
    return map(rows[0]);
  },
  async create(owner, data) {
    const [r] = await pool.execute('INSERT INTO todos(owner_id,title,completed) VALUES(?,?,?)', [owner, data.title, data.completed ?? false]);
    return this.find(owner, r.insertId);
  },
  async update(owner, id, data) {
    // SQL 필드명은 검증된 고정 목록에서만 생성한다. 사용자 문자열을 SQL에 삽입하지 않는다.
    const keys = Object.keys(data);
    await pool.execute(`UPDATE todos SET ${keys.map(k => `${k}=?`).join(',')} WHERE id=? AND owner_id=?`, [...keys.map(k => data[k]), id, owner]);
    return this.find(owner, id);
  },
  async remove(owner, id) {
    const [r] = await pool.execute('DELETE FROM todos WHERE id=? AND owner_id=?', [id, owner]);
    return r.affectedRows > 0;
  },
};

// 서비스는 HTTP 응답 객체를 몰라도 된다. 입력 규칙과 업무 규칙을 담당한다.
const todoService = {
  async list(owner, query) {
    const page = query.page === undefined ? 1 : idOf(query.page);
    const limit = query.limit === undefined ? 20 : idOf(query.limit);
    if (limit > 100 || page > 1000000) throw fail(400, 'INVALID_PAGE', 'limit<=100, page<=1000000이어야 합니다.');
    if (query.completed !== undefined && !['true', 'false'].includes(query.completed))
      throw fail(400, 'VALIDATION_ERROR', 'completed 필터는 true 또는 false입니다.');
    return { data: await todoRepository.list(owner, limit, (page - 1) * limit,
      query.completed === undefined ? undefined : query.completed === 'true'), page, limit };
  },
  async get(owner, value) {
    const todo = await todoRepository.find(owner, idOf(value));
    if (!todo) throw fail(404, 'TODO_NOT_FOUND', '할 일을 찾을 수 없습니다.');
    return todo;
  },
  async create(owner, body) { return todoRepository.create(owner, todoInput(body)); },
  async update(owner, value, body) {
    const todo = await todoRepository.update(owner, idOf(value), todoInput(body, true));
    if (!todo) throw fail(404, 'TODO_NOT_FOUND', '할 일을 찾을 수 없습니다.');
    return todo;
  },
  async remove(owner, value) {
    if (!await todoRepository.remove(owner, idOf(value))) throw fail(404, 'TODO_NOT_FOUND', '할 일을 찾을 수 없습니다.');
  },
};

// 컨트롤러는 HTTP 상태코드/헤더/본문 변환만 담당한다.
export const todoRouter = Router();
todoRouter.get('/', async (req, res) => res.json(await todoService.list(req.userId, req.query)));
todoRouter.post('/', async (req, res) => {
  const todo = await todoService.create(req.userId, req.body);
  res.location(`/api/todos/${todo.id}`).status(201).json(todo);
});
todoRouter.get('/:id', async (req, res) => res.json(await todoService.get(req.userId, req.params.id)));
todoRouter.patch('/:id', async (req, res) => res.json(await todoService.update(req.userId, req.params.id, req.body)));
todoRouter.delete('/:id', async (req, res) => { await todoService.remove(req.userId, req.params.id); res.status(204).end(); });
