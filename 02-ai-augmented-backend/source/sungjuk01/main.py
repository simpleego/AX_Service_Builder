from pathlib import Path
from typing import Annotated

from fastapi import Body, FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()


# 학생 한 명의 입력 형식: 공백 이름 및 0~100 범위 밖 점수 차단
class Student(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=30)
    department: str = Field(min_length=1, max_length=50)
    korean: int = Field(ge=0, le=100, strict=True)
    english: int = Field(ge=0, le=100, strict=True)
    math: int = Field(ge=0, le=100, strict=True)


@app.get("/")
def home():
    return FileResponse(Path(__file__).with_name("index.html"))


@app.post("/scores")
def calculate(students: Annotated[list[Student], Body(min_length=1, max_length=10)]):
    results = []
    for student in students:
        total = student.korean + student.english + student.math
        average = total / 3

        if average >= 90:
            grade = "A"
        elif average >= 80:
            grade = "B"
        elif average >= 70:
            grade = "C"
        elif average >= 60:
            grade = "D"
        else:
            grade = "F"

        results.append({
            **student.model_dump(),
            "total": total,
            "average": round(average, 2),
            "grade": grade,
        })
    return results
