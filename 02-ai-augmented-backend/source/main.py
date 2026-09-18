from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# HTML과 FastAPI 서버의 주소가 다르므로 CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hi")
def home():
    return {"message": "안녕 파이썬."}

@app.get("/add")
def add(num1: int, num2: int):
    # num1=10
    # num2=20
    sum = num1+num2
    return {"합계": sum}

@app.get("/sub")
def add(num1: int, num2: int):
    # num1=10
    # num2=20
    result = num1-num2
    return {"결과": result}