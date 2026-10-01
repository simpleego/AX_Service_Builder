"""학생별 계산은 Python, 과목별 집계는 MariaDB SQL로 처리합니다."""
import logging
from pathlib import Path
from typing import Annotated

import pymysql
from fastapi import Body, FastAPI, HTTPException, Query, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, ConfigDict, Field, field_validator

from database import connect_db

app = FastAPI(title='MariaDB 학생 성적 관리')
logger = logging.getLogger(__name__)


class Scores(BaseModel):
    korean: int = Field(default=0, ge=0, le=100, strict=True)
    english: int = Field(default=0, ge=0, le=100, strict=True)
    math: int = Field(default=0, ge=0, le=100, strict=True)

    @field_validator('korean', 'english', 'math', mode='before')
    @classmethod
    def empty_to_zero(cls, value):
        if value is None or (isinstance(value, str) and not value.strip()):
            return 0
        return value


class Student(Scores):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    name: str = Field(min_length=1, max_length=30)
    department: str = Field(min_length=1, max_length=50)


def calculate_result(student: dict) -> dict:
    """반올림 전 평균으로 학점을 판정합니다. 파생값은 DB에 저장하지 않습니다."""
    total = student['korean'] + student['english'] + student['math']
    average = total / 3
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
    return {'total': total, 'average': round(average, 2), 'grade': grade}


def student_result(row: dict) -> dict:
    return {**row, **calculate_result(row)}


@app.exception_handler(pymysql.MySQLError)
def database_error(request: Request, exc: pymysql.MySQLError):
    logger.exception('MariaDB 작업 실패', exc_info=exc)
    return JSONResponse(status_code=503, content={
        'detail': 'DB 작업에 실패했습니다. MariaDB 실행 상태, .env 설정, schema.sql 실행 여부를 확인하세요.'
    })


@app.get('/', include_in_schema=False)
def home():
    return FileResponse(Path(__file__).with_name('index.html'))


@app.post('/scores')
def calculate(students: Annotated[list[Student], Body(min_length=1, max_length=10)]):
    """기존 학생별 계산 API 유지. 저장하지 않고 계산만 합니다."""
    return [calculate_result(student.model_dump()) for student in students]


@app.get('/students')
def list_students(q: str = Query(default='', max_length=50)):
    # LOCATE: %, _도 와일드카드가 아닌 검색 문자로 취급합니다.
    keyword = q.strip()
    with connect_db() as connection, connection.cursor() as cursor:
        cursor.execute('''
            SELECT id, name, department, korean, english, math
            FROM students
            WHERE LOCATE(%s, name) > 0 OR LOCATE(%s, department) > 0
            ORDER BY id DESC
        ''', (keyword, keyword))
        return [student_result(row) for row in cursor.fetchall()]


@app.get('/students/{student_id}')
def get_student(student_id: int):
    with connect_db() as connection, connection.cursor() as cursor:
        cursor.execute('SELECT * FROM students WHERE id = %s', (student_id,))
        row = cursor.fetchone()
        if row is None:
            raise HTTPException(404, '학생을 찾을 수 없습니다.')
        return student_result(row)


@app.post('/students', status_code=201)
def create_student(student: Student):
    values = student.model_dump()
    with connect_db() as connection, connection.cursor() as cursor:
        cursor.execute('''
            INSERT INTO students (name, department, korean, english, math)
            VALUES (%s, %s, %s, %s, %s)
        ''', (student.name, student.department, student.korean, student.english, student.math))
        result = student_result({'id': cursor.lastrowid, **values})
    return result


@app.put('/students/{student_id}')
def update_student(student_id: int, student: Student):
    with connect_db() as connection, connection.cursor() as cursor:
        # 같은 값으로 수정하면 UPDATE rowcount가 0일 수 있으므로 존재 여부를 별도로 확인
        cursor.execute('SELECT id FROM students WHERE id = %s FOR UPDATE', (student_id,))
        if cursor.fetchone() is None:
            raise HTTPException(404, '학생을 찾을 수 없습니다.')
        cursor.execute('''
            UPDATE students SET name=%s, department=%s, korean=%s, english=%s, math=%s
            WHERE id=%s
        ''', (student.name, student.department, student.korean, student.english,
              student.math, student_id))
    return student_result({'id': student_id, **student.model_dump()})


@app.delete('/students/{student_id}', status_code=204)
def delete_student(student_id: int):
    with connect_db() as connection, connection.cursor() as cursor:
        cursor.execute('DELETE FROM students WHERE id = %s', (student_id,))
        if cursor.rowcount == 0:
            raise HTTPException(404, '학생을 찾을 수 없습니다.')
    return Response(status_code=204)


# 가로형 점수를 UNION ALL로 세로로 펼친 다음 과목별로 그룹화합니다.
# 과목 목록과 LEFT JOIN하므로 학생이 0명이어도 항상 세 과목이 반환됩니다.
SUBJECT_STATS_SQL = '''
    SELECT subjects.subject,
           COUNT(scores.score) AS student_count,
           COALESCE(SUM(scores.score), 0) AS total,
           ROUND(AVG(scores.score), 2) AS average,
           MIN(scores.score) AS minimum,
           MAX(scores.score) AS maximum
    FROM (
        SELECT 'korean' AS subject, 1 AS sort_order
        UNION ALL SELECT 'english', 2
        UNION ALL SELECT 'math', 3
    ) AS subjects
    LEFT JOIN (
        SELECT 'korean' AS subject, korean AS score FROM students
        UNION ALL
        SELECT 'english', english FROM students
        UNION ALL
        SELECT 'math', math FROM students
    ) AS scores ON scores.subject = subjects.subject
    GROUP BY subjects.subject, subjects.sort_order
    ORDER BY subjects.sort_order
'''


@app.get('/subjects')
def subject_statistics():
    """검색 조건과 관계없이 DB에 저장된 전체 학생의 통계입니다."""
    with connect_db() as connection, connection.cursor() as cursor:
        cursor.execute(SUBJECT_STATS_SQL)
        return cursor.fetchall()
