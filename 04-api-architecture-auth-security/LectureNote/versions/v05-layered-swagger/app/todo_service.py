from fastapi import HTTPException
from .todo_repository import TodoRepository
from .schemas import TodoCreate, TodoPatch
class TodoService:
    def __init__(self, db):
        self.db, self.repo = db, TodoRepository(db)
    def list(self, owner, page, limit, completed):
        return {'data': self.repo.list(owner, page, limit, completed), 'page': page, 'limit': limit}
    def get(self, owner, todo_id):
        todo = self.repo.find(owner, todo_id)
        if todo is None:
            # 타인의 Todo와 없는 Todo에 같은 404를 주어 존재 여부를 숨긴다.
            raise HTTPException(404, 'TODO_NOT_FOUND')
        return todo
    def create(self, owner, data: TodoCreate):
        todo = self.repo.add(owner, data.model_dump())
        self.db.commit()
        self.db.refresh(todo)
        return todo
    def update(self, owner, todo_id, data: TodoPatch):
        todo = self.get(owner, todo_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(todo, key, value)
        self.db.commit()
        self.db.refresh(todo)
        return todo
    def remove(self, owner, todo_id):
        self.db.delete(self.get(owner, todo_id))
        self.db.commit()
