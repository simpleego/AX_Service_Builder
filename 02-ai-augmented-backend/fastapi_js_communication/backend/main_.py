"""FastAPI ↔ Vanilla JS 통신 방식 17종 통합 실습 서버.
실습 전용 예제입니다. 데이터는 서버 재시작 시 초기화됩니다.
"""
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import Cookie, FastAPI, File, Form, Header, HTTPException, Response, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field

app = FastAPI(title="클라이언트 ↔ 서버 통신방식 17종 실습", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScoreInput(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    kor: int = Field(ge=0, le=100)
    eng: int = Field(ge=0, le=100)
    math: int = Field(ge=0, le=100)

class StudentInput(BaseModel):
    name: str = Field(min_length=1, max_length=40)

students = {1: {"id": 1, "name": "홍길동"}, 2: {"id": 2, "name": "김철수"}}
next_id = 3
status_counter = 0
long_poll_version = 0

@app.get("/hello")
def hello():
    return {"message": "안녕하세요! FastAPI 서버입니다."}

# 1. Path Parameter
@app.get("/students/{student_id}")
def student_by_id(student_id: int):
    if student_id not in students:
        raise HTTPException(404, "해당 학생이 없습니다.")
    return students[student_id]

# 2. Query String
@app.get("/search")
def search(keyword: str = "", page: int = 1):
    return {"keyword": keyword, "page": page, "message": f"'{keyword}' 검색 (페이지 {page})"}

# 3. 전통 HTML Form: HTML 문서 응답으로 페이지 이동 체험
@app.post("/traditional-login", response_class=HTMLResponse)
def traditional_login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    from html import escape
    return f"<html lang='ko'><meta charset='utf-8'><title>Form 응답</title><body style='font-family:sans-serif;padding:40px'><h2>전통 Form 전송 결과</h2><p>사용자: {escape(username)}</p><p>비밀번호는 표시하지 않습니다.</p><a href='http://127.0.0.1:5500'>돌아가기 (Live Server 주소)</a></body></html>"

# 4~5. XHR & Fetch GET
@app.get("/student")
def one_student():
    return {"name": "홍길동", "score": 95}

# 6. JSON POST
@app.post("/scores")
def calculate_scores(data: ScoreInput):
    total = data.kor + data.eng + data.math
    average = round(total / 3, 2)
    grade = "A" if average >= 90 else "B" if average >= 80 else "C" if average >= 70 else "D" if average >= 60 else "F"
    return {"name": data.name, "total": total, "average": average, "grade": grade}

# 7. REST CRUD
@app.get("/students")
def list_students():
    return list(students.values())

@app.post("/students", status_code=201)
def create_student(data: StudentInput):
    global next_id
    item = {"id": next_id, "name": data.name}
    students[next_id] = item
    next_id += 1
    return item

@app.put("/students/{student_id}")
def update_student(student_id: int, data: StudentInput):
    if student_id not in students:
        raise HTTPException(404, "해당 학생이 없습니다.")
    students[student_id]["name"] = data.name
    return students[student_id]

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        raise HTTPException(404, "해당 학생이 없습니다.")
    del students[student_id]
    return {"message": f"{student_id}번 학생 삭제 완료"}

# 8. URLSearchParams
@app.post("/urlencoded")
def urlencoded(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username, "message": "application/x-www-form-urlencoded 수신 완료"}

# 9. FormData
@app.post("/formdata")
def form_data(username: Annotated[str, Form()]):
    return {"username": username, "message": "multipart/form-data 수신 완료"}

# 10. 파일 업로드: 저장하지 않고 파일 이름/크기만 반환, 최대 5MB
@app.post("/upload")
async def upload(name: Annotated[str, Form()], file: Annotated[UploadFile, File()]):
    try:
        payload = await file.read(5 * 1024 * 1024 + 1)
        if len(payload) > 5 * 1024 * 1024:
            raise HTTPException(413, "파일은 5MB 이하만 허용합니다.")
        return {"name": name, "filename": Path(file.filename or "unknown").name, "content_type": file.content_type, "size_bytes": len(payload)}
    finally:
        await file.close()

# 11. Header
@app.get("/header-user")
def header_user(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key != "demo-key-123":
        raise HTTPException(401, "실습용 API 키가 올바르지 않습니다.")
    return {"message": "Header 인증 실습 성공", "key_received": True}

# 12. Cookie: 인증 수단이 아닌 단순 상태 전달 데모
@app.post("/cookie-login")
def cookie_login(response: Response):
    response.set_cookie(key="demo_username", value="hong", httponly=True, samesite="lax", max_age=3600)
    return {"message": "실습용 Cookie가 설정되었습니다."}

@app.get("/mypage")
def mypage(demo_username: Annotated[str | None, Cookie()] = None):
    if not demo_username:
        raise HTTPException(401, "Cookie가 없습니다. 먼저 Cookie 설정을 실행하세요.")
    return {"username": demo_username, "message": "Cookie를 서버에서 확인했습니다."}

@app.post("/cookie-logout")
def cookie_logout(response: Response):
    response.delete_cookie("demo_username", samesite="lax")
    return {"message": "Cookie 삭제 완료"}

# 13. Polling
@app.get("/status")
def status():
    global status_counter
    status_counter = (status_counter + 10) % 110
    return {"progress": status_counter, "checked_at": datetime.now().strftime("%H:%M:%S")}

# 14. Long Polling: 조건 신호 대신 timeout을 보여주는 학습 예제
@app.get("/long-poll")
async def long_poll():
    await asyncio.sleep(5)
    return {"message": "5초 동안 대기한 후 응답", "time": datetime.now().strftime("%H:%M:%S")}

# 15. SSE
@app.get("/events")
async def events():
    async def event_generator():
        for i in range(1, 6):
            yield f"data: 진행률 {i * 20}%\n\n"
            await asyncio.sleep(1)
        yield "event: finished\ndata: SSE 전송 완료\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

# 16. WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"서버 수신: {message}")
    except WebSocketDisconnect:
        pass

# 17. Streaming Response
@app.get("/stream")
async def stream():
    async def stream_text():
        for chunk in ["안녕하세요. ", "FastAPI와 ", "JavaScript의 ", "스트리밍 ", "예제입니다."]:
            yield chunk.encode("utf-8")
            await asyncio.sleep(0.6)
    return StreamingResponse(stream_text(), media_type="text/plain; charset=utf-8", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
