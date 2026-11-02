import { pool } from './common.js';
const map = row => row && ({ ...row, completed: Boolean(row.completed) });
// 모든 쿼리는 바인딩 파라미터를 사용한다. owner 조건이 타인 데이터 접근을 막는다.
export const todoRepository = {
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
