import os

import pymysql
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel, Field


# ── DB 연결 ─────────────────────────────────────────
# 접속 정보는 코드에 적지 않고 환경 변수로 받는다.
def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "app"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "guestbook"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,  # 결과를 dict로 받기
        autocommit=True,
    )


# ── 요청 데이터 형식 ────────────────────────────────
class MessageIn(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=500)


app = FastAPI(
    title="방명록 API",
    docs_url="/api/docs",            # Swagger 화면 주소
    openapi_url="/api/openapi.json",
)
router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1")
        return {"status": "ok", "db": "ok"}
    except pymysql.MySQLError as e:
        raise HTTPException(status_code=503, detail=f"DB 연결 실패: {e}")


@router.get("/messages")
def list_messages():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, content, created_at "
            "FROM messages ORDER BY id DESC LIMIT 50"
        )
        return cur.fetchall()


@router.post("/messages", status_code=201)
def create_message(msg: MessageIn):
    with get_conn() as conn, conn.cursor() as cur:
        # %s 자리표시자를 쓰면 PyMySQL이 값을 안전하게 처리한다 (SQL 인젝션 방지)
        cur.execute(
            "INSERT INTO messages (name, content) VALUES (%s, %s)",
            (msg.name, msg.content),
        )
        cur.execute(
            "SELECT id, name, content, created_at FROM messages WHERE id = %s",
            (cur.lastrowid,),
        )
        return cur.fetchone()


@router.delete("/messages/{message_id}", status_code=204)
def delete_message(message_id: int):
    with get_conn() as conn, conn.cursor() as cur:
        deleted = cur.execute("DELETE FROM messages WHERE id = %s", (message_id,))
        if deleted == 0:
            raise HTTPException(status_code=404, detail="없는 메시지입니다")


app.include_router(router)
