from fastapi import FastAPI, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

count = 0

# HTML과 FastAPI 서버의 주소가 다르므로 CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
    


@app.get("/count")
def get_count():
    global count

    count += 1

    return {
        "방문횟수": count
    }

@app.get("/login")
def login(response: Response):

    response.set_cookie(
        key="username",
        value="hong"
    )

    return {
        "message": "쿠키 저장 완료"
    }


@app.get("/mypage")
def mypage(username: str | None = Cookie(default=None)):

    return {
        "username": username
    }