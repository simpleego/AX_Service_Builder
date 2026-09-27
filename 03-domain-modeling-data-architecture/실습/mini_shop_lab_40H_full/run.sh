#!/bin/bash
# Day3~5 실행 스크립트
echo "1. venv 생성 & 설치"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "2. .env 생성"
cp .env.example .env
echo "DATABASE_URL 수정 필요하면 .env 편집"

echo "3. Alembic 초기화 (최초 1회)"
# alembic 폴더가 이미 있으면 스킵
if [ ! -f "alembic/versions/.gitkeep" ]; then
  alembic revision --autogenerate -m "init mini shop"
fi
alembic upgrade head

echo "4. 10만건 시드"
python seed_faker_100k.py --total 100000 --reset --users 5000 --orders 20000

echo "5. FastAPI 실행"
uvicorn app.main:app --reload --port 8000
