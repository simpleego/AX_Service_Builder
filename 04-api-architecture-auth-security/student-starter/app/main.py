"""
TagTodo API — 학생용 스타터
실행: uvicorn app.main:app --reload

core/security.py, repositories/*, services/*, dependencies.py, routers/*
의 TODO를 모두 채우면 이 서버가 정상 동작합니다.
"""
from fastapi import FastAPI

from app.db.database import Base, engine
from app.models import user, tag, todo, session  # noqa: F401
from app.routers import auth, oauth, todos, tags

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TagTodo API (학생용)",
    description="태그 기반 스마트 할일 관리 서비스 — 과목4 실습",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(oauth.router)
app.include_router(todos.router)
app.include_router(tags.router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "TagTodo (student)"}
