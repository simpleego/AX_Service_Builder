from pathlib import Path
from typing import Annotated, Literal

from fastapi import Body, FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

app = FastAPI()


class Scores(BaseModel):
    korean: int = Field(default=0, ge=0, le=100, strict=True)
    english: int = Field(default=0, ge=0, le=100, strict=True)
    math: int = Field(default=0, ge=0, le=100, strict=True)

    # 직접 API를 호출해도 빈 문자열/null/누락 점수는 0점 처리
    @field_validator('korean', 'english', 'math', mode='before')
    @classmethod
    def empty_to_zero(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            return 0
        return value


class Student(Scores):
    model_config = ConfigDict(str_strip_whitespace=True)
    name: str = Field(min_length=1, max_length=30)
    department: str = Field(min_length=1, max_length=50)


@app.get('/')
def home():
    return FileResponse(Path(__file__).with_name('index.html'))


@app.post('/scores')
def calculate(students: Annotated[list[Student], Body(min_length=1, max_length=10)]):
    results = []
    for student in students:
        total = student.korean + student.english + student.math
        average = total / 3  # 빈 점수도 0점으로 포함, 항상 세 과목으로 나눔
        if average >= 90:
            grade = 'A'
        elif average >= 80:
            grade = 'B'
        elif average >= 70:
            grade = 'C'
        elif average >= 60:
            grade = 'D'
        else:
            grade = 'F'
        results.append({'total': total, 'average': round(average, 2), 'grade': grade})
    return results


@app.post('/subjects/{subject}')
def calculate_subject(
    subject: Literal['korean', 'english', 'math'],
    students: Annotated[list[Scores], Body(min_length=1, max_length=10)],
):
    # 이름/학과와 무관하게 현재 화면의 모든 학생 행을 계산에 포함
    scores = [getattr(student, subject) for student in students]
    return {
        'total': sum(scores),
        'average': round(sum(scores) / len(scores), 2),
        'maximum': max(scores),
        'minimum': min(scores),
    }
