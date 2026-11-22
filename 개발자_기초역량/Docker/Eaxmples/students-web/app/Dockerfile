FROM python:3.12-slim

WORKDIR /app

# 라이브러리 먼저 설치 → 코드만 바뀌면 이 단계는 캐시를 재사용한다
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY static ./static

EXPOSE 8000

# 0.0.0.0: 컨테이너 밖(포트 포워딩)에서 오는 요청도 받는다
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
