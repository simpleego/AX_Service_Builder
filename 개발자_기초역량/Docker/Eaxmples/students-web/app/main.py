import os

import pymysql
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles


# ── DB 연결 ─────────────────────────────────────────
# 접속 정보는 코드에 적지 않고 환경 변수로 받는다 (docker run -e ...)
def get_conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "student"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "classdb"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,  # 결과를 dict로 받기
        autocommit=True,
    )


app = FastAPI(
    title="학생 조회 API",
    docs_url="/api/docs",            # Swagger 화면 주소
    openapi_url="/api/openapi.json",
)
router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    """WAS와 DB가 모두 살아 있는지 확인"""
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT 1")
        return {"status": "ok", "db": "ok"}
    except pymysql.MySQLError as e:
        raise HTTPException(status_code=503, detail=f"DB 연결 실패: {e}")


@router.get("/students")
def list_students(major: str | None = None):
    """전체 학생 목록. ?major=AI융합 처럼 전공으로 거를 수 있다"""
    sql = "SELECT id, name, major, created_at FROM students"
    params = ()
    if major:
        # %s 자리표시자를 쓰면 PyMySQL이 값을 안전하게 처리한다 (SQL 인젝션 방지)
        sql += " WHERE major LIKE %s"
        params = (f"%{major}%",)
    sql += " ORDER BY id"

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


@router.get("/students/{student_id}")
def get_student(student_id: int):
    """학생 한 명 조회"""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, major, created_at FROM students WHERE id = %s",
            (student_id,),
        )
        row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="없는 학생입니다")
    return row


app.include_router(router)

# ── 화면(HTML/JS) ───────────────────────────────────
# /api 로 시작하지 않는 요청은 static 폴더의 파일로 응답한다.
# html=True: "/" 로 접속하면 index.html 을 보여 준다.
# 반드시 include_router 뒤에 둔다 (먼저 두면 /api 요청까지 가로챈다).
app.mount("/", StaticFiles(directory="static", html=True), name="static")
