"""
FastAPI 쿠키 / 세션 인증 실습 서버

실행:  uvicorn app.main:app --reload
문서:  http://localhost:8000/docs   (Swagger UI에서 바로 테스트 가능)
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import cookie_auth, session_auth, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 테이블이 없으면 생성 (sql/schema.sql 로 직접 만들어도 됨)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="웹 인증 실습 - 쿠키 & 세션",
    description="JWT 학습 전, 쿠키 인증과 세션 인증의 동작 원리를 백엔드만으로 실습합니다.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users.router)
app.include_router(cookie_auth.router)
app.include_router(session_auth.router)


@app.get("/", tags=["안내"])
def root():
    return {
        "docs": "/docs",
        "실습 순서": [
            "0) POST /users/signup         회원가입",
            "1-1) /cookie/v1/*             평문 쿠키 (위조 가능 체험)",
            "1-2) /cookie/v2/*             서명 쿠키 (위조 방지, 서버 측 무효화 불가)",
            "2) /session/*                 서버 세션 (MySQL 저장, 즉시 무효화 가능)",
        ],
    }
