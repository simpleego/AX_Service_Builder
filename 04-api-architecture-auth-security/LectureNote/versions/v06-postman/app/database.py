import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
load_dotenv()
# URL.create는 비밀번호의 @, / 등 특수문자를 안전하게 인코딩한다.
url = URL.create('mysql+pymysql', username=os.getenv('DB_USER', 'todo_app'),
    password=os.getenv('DB_PASSWORD', ''), host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', '3306')), database=os.getenv('DB_NAME', 'todo_course'),
    query={'charset': 'utf8mb4'})
engine = create_engine(url, pool_pre_ping=True, pool_recycle=1800)
@event.listens_for(engine, 'connect')
def set_utc(connection, _record):
    # DB/서버의 로컬 시간대가 달라도 토큰 만료 계산은 UTC로 통일한다.
    with connection.cursor() as cursor:
        cursor.execute("SET time_zone = '+00:00'")
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
def get_db():
    # 요청마다 세션을 만들고 예외 시 롤백한다. 트랜잭션 경계는 서비스에서 결정한다.
    with SessionLocal() as db:
        try:
            yield db
        except Exception:
            db.rollback()
            raise
