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

# CORS 설정: 프런트엔드(Live Server :5500)와 백엔드(:8000)는 포트가 달라 서로 다른 출처(origin)로 취급된다.
# 허용할 출처를 명시해야 브라우저가 교차 출처 요청의 응답을 JS에 넘겨준다.
# allow_credentials=True 는 Cookie 실습(12번)에 필요하며, 이 경우 allow_origins 에 "*" 를 쓸 수 없어 출처를 직접 나열한다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScoreInput(BaseModel):
    """성적 계산 요청 본문(JSON) 모델.

    Field 제약 조건을 어기면 FastAPI가 자동으로 422 응답을 반환한다.

    Attributes:
        name: 학생 이름 (1~40자)
        kor: 국어 점수 (0~100)
        eng: 영어 점수 (0~100)
        math: 수학 점수 (0~100)
    """
    name: str = Field(min_length=1, max_length=40)
    kor: int = Field(ge=0, le=100)
    eng: int = Field(ge=0, le=100)
    math: int = Field(ge=0, le=100)

class StudentInput(BaseModel):
    """학생 등록/수정 요청 본문(JSON) 모델.

    Attributes:
        name: 학생 이름 (1~40자)
    """
    name: str = Field(min_length=1, max_length=40)

# 메모리 저장소(실습용 DB 대체). 서버를 재시작하면 초기 상태로 돌아간다.
students = {1: {"id": 1, "name": "홍길동"}, 2: {"id": 2, "name": "김철수"}}
next_id = 3              # 다음에 생성될 학생 id (자동 증가)
status_counter = 0       # Polling 실습용 진행률 값
long_poll_version = 0    # Long Polling 확장용 버전 값 (현재 예제에서는 사용하지 않음)

@app.get("/hello")
def hello():
    """서버 동작 확인용 인사 메시지를 반환한다.

    Returns:
        dict: {"message": 인사 문자열}
    """
    return {"message": "안녕하세요! FastAPI 서버입니다."}

# 1. Path Parameter
@app.get("/students/{student_id}")
def student_by_id(student_id: int):
    """URL 경로에 포함된 id로 학생 한 명을 조회한다. (예: GET /students/1)

    Args:
        student_id: 경로 변수로 전달된 학생 id. 타입 힌트(int)에 따라 자동 변환되며,
            숫자가 아니면 422 오류가 발생한다.

    Returns:
        dict: {"id": 학생 id, "name": 이름}

    Raises:
        HTTPException(404): 해당 id의 학생이 없을 때
    """
    if student_id not in students:
        raise HTTPException(404, "해당 학생이 없습니다.")
    return students[student_id]

# 2. Query String
@app.get("/search")
def search(keyword: str = "", page: int = 1):
    """쿼리 스트링 값을 받아 그대로 돌려준다. (예: GET /search?keyword=python&page=2)

    경로 변수에 없는 함수 매개변수는 FastAPI가 쿼리 스트링으로 해석한다.

    Args:
        keyword: 검색어 (생략 시 빈 문자열)
        page: 페이지 번호 (생략 시 1)

    Returns:
        dict: 전달받은 keyword, page 와 안내 메시지
    """
    return {"keyword": keyword, "page": page, "message": f"'{keyword}' 검색 (페이지 {page})"}

# 3. 전통 HTML Form: HTML 문서 응답으로 페이지 이동 체험
@app.post("/traditional-login", response_class=HTMLResponse)
def traditional_login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    """<form> 태그의 기본 submit 으로 전송된 로그인 정보를 받아 HTML 페이지를 응답한다.

    JSON이 아닌 HTML 문서를 반환하므로 브라우저는 결과 페이지로 이동(새로고침)한다.

    Args:
        username: 폼 필드 username 값
        password: 폼 필드 password 값 (화면에는 출력하지 않음)

    Returns:
        str: 전송 결과를 보여주는 HTML 문자열
    """
    from html import escape
    # 사용자 입력을 HTML에 그대로 넣으면 <script> 등이 실행될 수 있으므로(XSS) escape 로 특수문자를 치환한다.
    return f"<html lang='ko'><meta charset='utf-8'><title>Form 응답</title><body style='font-family:sans-serif;padding:40px'><h2>전통 Form 전송 결과</h2><p>사용자: {escape(username)}</p><p>비밀번호는 표시하지 않습니다.</p><a href='http://127.0.0.1:5500'>돌아가기 (Live Server 주소)</a></body></html>"

# 4~5. XHR & Fetch GET
@app.get("/student")
def one_student():
    """XMLHttpRequest / fetch GET 실습용 고정 학생 데이터를 반환한다.

    Returns:
        dict: {"name": 이름, "score": 점수}
    """
    return {"name": "홍길동", "score": 95}

# 6. JSON POST
@app.post("/scores")
def calculate_scores(data: ScoreInput):
    """JSON 본문으로 받은 세 과목 점수의 총점·평균·학점을 계산한다.

    Args:
        data: 요청 본문 JSON을 검증·변환한 ScoreInput 객체

    Returns:
        dict: {"name", "total": 총점, "average": 평균(소수 둘째 자리), "grade": A~F 학점}
    """
    total = data.kor + data.eng + data.math
    average = round(total / 3, 2)
    # 조건부 표현식을 연쇄한 형태: 90 이상 A, 80 이상 B, 70 이상 C, 60 이상 D, 그 외 F
    grade = "A" if average >= 90 else "B" if average >= 80 else "C" if average >= 70 else "D" if average >= 60 else "F"
    return {"name": data.name, "total": total, "average": average, "grade": grade}

# 7. REST CRUD
@app.get("/students")
def list_students():
    """전체 학생 목록을 조회한다. (Read)

    Returns:
        list[dict]: 학생 객체 목록
    """
    return list(students.values())

@app.post("/students", status_code=201)
def create_student(data: StudentInput):
    """새 학생을 등록한다. (Create) 성공 시 201 Created 를 응답한다.

    Args:
        data: 등록할 학생 이름이 담긴 StudentInput

    Returns:
        dict: 새로 생성된 학생 객체 {"id", "name"}
    """
    # 모듈 전역 변수 next_id 의 값을 변경하므로 global 선언이 필요하다.
    global next_id
    item = {"id": next_id, "name": data.name}
    students[next_id] = item
    next_id += 1
    return item

@app.put("/students/{student_id}")
def update_student(student_id: int, data: StudentInput):
    """지정한 학생의 이름을 수정한다. (Update)

    Args:
        student_id: 수정할 학생 id (경로 변수)
        data: 변경할 이름이 담긴 StudentInput (요청 본문)

    Returns:
        dict: 수정된 학생 객체

    Raises:
        HTTPException(404): 해당 id의 학생이 없을 때
    """
    if student_id not in students:
        raise HTTPException(404, "해당 학생이 없습니다.")
    students[student_id]["name"] = data.name
    return students[student_id]

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    """지정한 학생을 삭제한다. (Delete)

    Args:
        student_id: 삭제할 학생 id (경로 변수)

    Returns:
        dict: 삭제 완료 메시지

    Raises:
        HTTPException(404): 해당 id의 학생이 없을 때
    """
    if student_id not in students:
        raise HTTPException(404, "해당 학생이 없습니다.")
    del students[student_id]
    return {"message": f"{student_id}번 학생 삭제 완료"}

# 8. URLSearchParams
@app.post("/urlencoded")
def urlencoded(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    """JS의 URLSearchParams 로 보낸 application/x-www-form-urlencoded 데이터를 받는다.

    Form() 으로 선언한 매개변수는 JSON 본문이 아닌 폼 인코딩 본문에서 값을 읽는다.

    Args:
        username: 폼 필드 username 값
        password: 폼 필드 password 값 (응답에는 포함하지 않음)

    Returns:
        dict: 수신한 username 과 안내 메시지
    """
    return {"username": username, "message": "application/x-www-form-urlencoded 수신 완료"}

# 9. FormData
@app.post("/formdata")
def form_data(username: Annotated[str, Form()]):
    """JS의 FormData 로 보낸 multipart/form-data 데이터를 받는다.

    Args:
        username: 폼 필드 username 값

    Returns:
        dict: 수신한 username 과 안내 메시지
    """
    return {"username": username, "message": "multipart/form-data 수신 완료"}

# 10. 파일 업로드: 저장하지 않고 파일 이름/크기만 반환, 최대 5MB
@app.post("/upload")
async def upload(name: Annotated[str, Form()], file: Annotated[UploadFile, File()]):
    """multipart/form-data 로 업로드된 파일의 정보(이름·형식·크기)를 반환한다.

    파일은 디스크에 저장하지 않으며, 5MB 를 초과하면 거부한다.

    Args:
        name: 함께 전송된 텍스트 폼 필드 값
        file: 업로드된 파일 객체

    Returns:
        dict: {"name", "filename": 파일명, "content_type": MIME 형식, "size_bytes": 파일 크기}

    Raises:
        HTTPException(413): 파일 크기가 5MB 를 초과할 때
    """
    try:
        # 최대 크기보다 1바이트만 더 읽는다. 전체 파일을 메모리에 올리지 않고도
        # 읽은 길이가 5MB 를 넘는지만 보면 초과 여부를 판단할 수 있다.
        payload = await file.read(5 * 1024 * 1024 + 1)
        if len(payload) > 5 * 1024 * 1024:
            raise HTTPException(413, "파일은 5MB 이하만 허용합니다.")
        # Path(...).name 으로 "../../etc/passwd" 같은 경로 문자를 제거하고 순수 파일명만 남긴다.
        return {"name": name, "filename": Path(file.filename or "unknown").name, "content_type": file.content_type, "size_bytes": len(payload)}
    finally:
        # 예외 발생 여부와 관계없이 업로드 임시 파일을 닫아 자원을 해제한다.
        await file.close()

# 11. Header
@app.get("/header-user")
def header_user(x_api_key: Annotated[str | None, Header()] = None):
    """요청 헤더 X-API-Key 값을 확인하는 간단한 인증 실습.

    FastAPI는 매개변수 이름의 밑줄(_)을 하이픈(-)으로 바꿔 헤더를 찾으므로
    x_api_key 는 "X-API-Key" 헤더와 매칭된다(대소문자 구분 없음).

    Args:
        x_api_key: X-API-Key 헤더 값 (없으면 None)

    Returns:
        dict: 인증 성공 메시지

    Raises:
        HTTPException(401): 키가 없거나 "demo-key-123" 과 다를 때
    """
    if x_api_key != "demo-key-123":
        raise HTTPException(401, "실습용 API 키가 올바르지 않습니다.")
    return {"message": "Header 인증 실습 성공", "key_received": True}

# 12. Cookie: 인증 수단이 아닌 단순 상태 전달 데모
@app.post("/cookie-login")
def cookie_login(response: Response):
    """응답에 Set-Cookie 헤더를 추가해 브라우저에 실습용 Cookie 를 저장시킨다.

    Args:
        response: FastAPI가 주입하는 응답 객체 (헤더·Cookie 설정용)

    Returns:
        dict: Cookie 설정 완료 메시지
    """
    # httponly: JS(document.cookie)에서 읽을 수 없게 해 XSS 탈취를 방지
    # samesite="lax": 다른 사이트에서 시작된 POST 등에는 Cookie 를 보내지 않아 CSRF 위험을 줄임
    # max_age=3600: 1시간 후 만료
    response.set_cookie(key="demo_username", value="hong", httponly=True, samesite="lax", max_age=3600)
    return {"message": "실습용 Cookie가 설정되었습니다."}

@app.get("/mypage")
def mypage(demo_username: Annotated[str | None, Cookie()] = None):
    """요청에 포함된 demo_username Cookie 를 읽어 반환한다.

    프런트엔드에서 fetch 시 credentials: "include" 를 지정해야 Cookie 가 함께 전송된다.

    Args:
        demo_username: demo_username Cookie 값 (없으면 None)

    Returns:
        dict: Cookie 에서 읽은 사용자명과 메시지

    Raises:
        HTTPException(401): Cookie 가 없을 때
    """
    if not demo_username:
        raise HTTPException(401, "Cookie가 없습니다. 먼저 Cookie 설정을 실행하세요.")
    return {"username": demo_username, "message": "Cookie를 서버에서 확인했습니다."}

@app.post("/cookie-logout")
def cookie_logout(response: Response):
    """demo_username Cookie 를 삭제한다.

    Args:
        response: FastAPI가 주입하는 응답 객체

    Returns:
        dict: Cookie 삭제 완료 메시지
    """
    # 삭제는 만료된 같은 이름의 Cookie 를 덮어써서 이뤄지므로, 설정할 때와 같은 속성(samesite)을 맞춰 준다.
    response.delete_cookie("demo_username", samesite="lax")
    return {"message": "Cookie 삭제 완료"}

# 13. Polling
@app.get("/status")
def status():
    """Polling 실습: 호출될 때마다 진행률을 10씩 올려 반환한다.

    클라이언트가 setInterval 등으로 주기적으로 호출하는 상황을 가정한다.

    Returns:
        dict: {"progress": 진행률(0~100), "checked_at": 조회 시각 HH:MM:SS}
    """
    global status_counter
    # % 110 으로 0, 10, ..., 100 까지 증가한 뒤 다시 0 으로 순환한다.
    status_counter = (status_counter + 10) % 110
    return {"progress": status_counter, "checked_at": datetime.now().strftime("%H:%M:%S")}

# 14. Long Polling: 조건 신호 대신 timeout을 보여주는 학습 예제
@app.get("/long-poll")
async def long_poll():
    """Long Polling 실습: 응답을 5초 동안 보류했다가 반환한다.

    실제 Long Polling 은 새 데이터가 생길 때까지 대기하지만, 여기서는 고정 시간 대기로 흉내 낸다.

    Returns:
        dict: 대기 완료 메시지와 응답 시각
    """
    # time.sleep 과 달리 asyncio.sleep 은 이벤트 루프를 막지 않아, 대기 중에도 다른 요청을 처리할 수 있다.
    await asyncio.sleep(5)
    return {"message": "5초 동안 대기한 후 응답", "time": datetime.now().strftime("%H:%M:%S")}

# 15. SSE
@app.get("/events")
async def events():
    """SSE(Server-Sent Events) 실습: 1초 간격으로 진행률 이벤트를 5회 보낸 뒤 종료 이벤트를 보낸다.

    클라이언트는 EventSource 로 연결해 onmessage / addEventListener("finished") 로 수신한다.

    Returns:
        StreamingResponse: text/event-stream 형식의 스트리밍 응답
    """
    async def event_generator():
        """SSE 형식 문자열을 하나씩 생성하는 비동기 제너레이터."""
        for i in range(1, 6):
            # SSE 메시지 형식: "data: 내용" 줄 뒤에 빈 줄(\n\n)이 와야 한 개의 이벤트로 인식된다.
            yield f"data: 진행률 {i * 20}%\n\n"
            await asyncio.sleep(1)
        # "event:" 필드로 이벤트 이름을 지정하면 클라이언트에서 해당 이름으로 따로 리스닝할 수 있다.
        yield "event: finished\ndata: SSE 전송 완료\n\n"
    # Cache-Control: no-cache → 중간 캐시가 스트림을 저장하지 않도록 함
    # X-Accel-Buffering: no → Nginx 같은 프록시가 응답을 모아서 보내지(버퍼링) 않고 즉시 전달하도록 함
    return StreamingResponse(event_generator(), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

# 16. WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket 에코 서버: 클라이언트가 보낸 텍스트에 접두어를 붙여 되돌려준다.

    HTTP 와 달리 연결이 유지되는 동안 양방향으로 자유롭게 메시지를 주고받는다.

    Args:
        websocket: 클라이언트와 연결된 WebSocket 객체
    """
    # 핸드셰이크를 수락해야 연결이 성립된다.
    await websocket.accept()
    try:
        # 연결이 끊길 때까지 메시지 수신 → 응답을 반복한다.
        while True:
            message = await websocket.receive_text()
            await websocket.send_text(f"서버 수신: {message}")
    except WebSocketDisconnect:
        # 클라이언트가 연결을 닫으면 receive_text() 에서 예외가 발생하므로 정상 종료로 처리한다.
        pass

# 17. Streaming Response
@app.get("/stream")
async def stream():
    """Streaming Response 실습: 문장을 여러 조각으로 나눠 0.6초 간격으로 순차 전송한다.

    클라이언트는 fetch 의 response.body.getReader() 로 조각이 도착할 때마다 읽을 수 있다.

    Returns:
        StreamingResponse: text/plain 형식의 청크 스트리밍 응답
    """
    async def stream_text():
        """텍스트 조각을 UTF-8 바이트로 하나씩 생성하는 비동기 제너레이터."""
        for chunk in ["안녕하세요. ", "FastAPI와 ", "JavaScript의 ", "스트리밍 ", "예제입니다."]:
            # 한글이 포함되므로 명시적으로 UTF-8 바이트로 인코딩해 전송한다.
            yield chunk.encode("utf-8")
            await asyncio.sleep(0.6)
    # 헤더 의미는 /events 와 동일: 캐시·프록시 버퍼링을 막아 조각이 즉시 전달되게 한다.
    return StreamingResponse(stream_text(), media_type="text/plain; charset=utf-8", headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})
