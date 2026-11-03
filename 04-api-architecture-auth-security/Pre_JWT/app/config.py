"""
환경설정 모듈
- .env 파일의 값을 읽어 애플리케이션 전역에서 사용합니다.
"""
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "webauth")
DB_PASSWORD = os.getenv("DB_PASSWORD", "webauth1234")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "webauth_db")

# MySQL 접속 URL (비밀번호에 특수문자가 있어도 안전하도록 quote_plus 처리)
# DATABASE_URL 환경변수를 직접 지정하면 그 값이 우선합니다. (예: sqlite:///./test.db)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4",
)

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
SESSION_EXPIRE_MINUTES = int(os.getenv("SESSION_EXPIRE_MINUTES", "30"))
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "False").lower() == "true"
