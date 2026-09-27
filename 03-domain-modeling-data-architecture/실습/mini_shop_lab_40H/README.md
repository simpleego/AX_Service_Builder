
# Mini Shop Lab - 40H 실습 키트

## 파일 설명
- day2_starter.dbml : Day2 오전용 최소 ERD
- day2_full.dbml : Day2 오후~Day5 최종 ERD (dbdiagram.io import)
- day3_models_starter.py : 학생용 ORM 뼈대 (User/Product만)
- day3_models_complete.py : 교강사용 정답
- seed_faker_100k.py : 10만건 faker 시드
- day4_queries.sql : Day4 핵심 쿼리 8선
- day5_index_lab.sql : Day5 인덱스/성능 실습

## 실행 순서
1. dbdiagram.io 에 day2_starter.dbml 붙여넣고 팀별 ERD 확장
2. MySQL DB 생성: CREATE DATABASE mini_shop CHARACTER SET utf8mb4;
3. python -m venv venv && pip install sqlalchemy pymysql alembic faker tqdm
4. Base.metadata.create_all() or alembic upgrade head
5. python seed_faker_100k.py --total 100000 --reset --users 5000 --orders 20000
   (10만건은 약 2~3분 소요, batch 처리됨)

## Day5 인덱스 실습 힌트
- EXPLAIN ANALYZE SELECT ... 
- 10만건에서 OFFSET 50000 vs 커서 페이징 비교
