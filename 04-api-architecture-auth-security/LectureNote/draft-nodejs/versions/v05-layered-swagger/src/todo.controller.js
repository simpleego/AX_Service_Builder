import { Router } from 'express';
import { todoService as service } from './todo.service.js';
// 컨트롤러는 HTTP 상태코드/헤더/본문 변환만 담당한다.
export const todoRouter = Router();
todoRouter.get('/', async (req, res) => res.json(await service.list(req.userId, req.query)));
todoRouter.post('/', async (req, res) => {
  const todo = await service.create(req.userId, req.body);
  res.location(`/api/todos/${todo.id}`).status(201).json(todo);
});
todoRouter.get('/:id', async (req, res) => res.json(await service.get(req.userId, req.params.id)));
todoRouter.patch('/:id', async (req, res) => res.json(await service.update(req.userId, req.params.id, req.body)));
todoRouter.delete('/:id', async (req, res) => { await service.remove(req.userId, req.params.id); res.status(204).end(); });
