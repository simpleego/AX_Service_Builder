from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Todo
class TodoRepository:
    def __init__(self, db: Session):
        self.db = db
    def list(self, owner: int, page: int, limit: int, completed: bool | None):
        query = select(Todo).where(Todo.owner_id == owner)
        if completed is not None:
            query = query.where(Todo.completed == completed)
        # SQLAlchemy가 입력값을 바인딩하므로 문자열 결합 SQL을 작성하지 않는다.
        return self.db.scalars(query.order_by(Todo.id.desc()).offset((page-1)*limit).limit(limit)).all()
    def find(self, owner: int, todo_id: int):
        # 상세/수정/삭제 모두 소유권을 SQL 조건에 넣어 IDOR를 방지한다.
        return self.db.scalar(select(Todo).where(Todo.id == todo_id, Todo.owner_id == owner))
    def add(self, owner: int, values: dict):
        todo = Todo(owner_id=owner, **values)
        self.db.add(todo)
        return todo
