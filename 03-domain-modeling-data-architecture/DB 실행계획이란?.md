네, 가능합니다. HeidiSQL로 MariaDB의 실행계획(EXPLAIN)을 직접 확인하면서 실습할 수 있습니다. SQL을 실행하고 인덱스 적용 전후의 실행계획을 비교하는 방식으로 학습하면 좋습니다.

MariaDB 실행계획 실습에서 주로 사용하는 명령은 `EXPLAIN`과 `ANALYZE`입니다.

- `EXPLAIN`: 쿼리를 실제로 실행하지 않고 옵티마이저가 예상한 실행계획을 확인합니다.
- `ANALYZE`: 쿼리를 실제로 실행하면서 실제 행 처리량 등의 실행 통계를 확인합니다. 데이터 변경 쿼리가 아니라 조회 쿼리로 먼저 실습하는 것이 안전합니다.

## 1. HeidiSQL에서 실행계획 확인하기

Best MySQL GUI Tools in 2025: Top 7 Picks for Database Management | Medium

① MariaDB 접속

HeidiSQL에서 MariaDB 서버에 접속한 뒤 데이터베이스를 선택합니다.

HeidiSQL 12.15 for Windows, Linux and macOS

② SQL 실행

SQL 편집 창에서 `EXPLAIN SELECT ...`를 실행합니다. 결과 그리드에서 테이블 접근 방식과 인덱스 사용 여부를 확인합니다.

실행계획을 확인하는 별도의 그래픽 실행계획 창이 없어도 SQL 명령만으로 충분히 실습할 수 있습니다.

## 2. 직접 따라 하는 실행계획 실습

아래 SQL을 HeidiSQL 쿼리 편집기에 붙여 넣고 순서대로 실행해 보세요.

### ① 테스트 테이블 생성

sql
```
CREATE DATABASE IF NOT EXISTS explain_lab;
USE explain_lab;

CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    department VARCHAR(30),
    salary INT
) ENGINE=InnoDB;

INSERT INTO employees (name, department, salary)
VALUES
('Kim', 'DEV', 5000),
('Lee', 'HR', 4000),
('Park', 'DEV', 6000),
('Choi', 'SALES', 4500),
('Jung', 'DEV', 5500);
```

### ② 인덱스가 없는 조회 확인

sql
```
EXPLAIN
SELECT *
FROM employees
WHERE department = 'DEV';
```

결과에서 다음 항목을 확인합니다.

| 컬럼 | 의미 |
| --- | --- |
| `type` | 테이블 접근 방식 |
| `possible_keys` | 사용 가능한 인덱스 후보 |
| `key` | 실제 선택된 인덱스 |
| `rows` | 옵티마이저가 예상하는 읽기 행 수 |
| `Extra` | 추가 처리 정보 |

이 예제에서는 `department`에 인덱스가 없으므로 일반적으로 `type`이 `ALL`, `key`가 `NULL`로 표시됩니다. 다만 데이터가 적으면 실행계획의 선택이 달라질 수 있습니다.

MariaDB Documentation

### ③ 인덱스 생성 후 비교

sql
```
CREATE INDEX idx_employees_department
ON employees(department);

EXPLAIN
SELECT *
FROM employees
WHERE department = 'DEV';
```

인덱스 생성 전후의 `type`, `key`, `rows`를 비교하세요. 단, 테이블에 데이터가 5건뿐이어서 옵티마이저가 여전히 전체 테이블 조회를 선택할 수도 있습니다. 인덱스 효과를 확실히 관찰하려면 데이터를 수천\~수만 건으로 늘려 실습하는 것이 좋습니다.

### ④ 실제 실행 통계 확인

sql
```
ANALYZE
SELECT *
FROM employees
WHERE department = 'DEV';
```

MariaDB 버전이 지원한다면 `ANALYZE FORMAT=JSON`으로 더 상세한 통계도 확인할 수 있습니다. `ANALYZE`는 쿼리를 실제 실행하므로, 처음에는 `SELECT` 문으로 연습하세요.

MariaDB Documentation

+1

## 3. 추천 실습 순서

- 1단계: `EXPLAIN`의 `type`, `key`, `rows` 이해하기
- 2단계: 인덱스 생성 전후 비교하기
- 3단계: `WHERE`, `ORDER BY`, `GROUP BY` 실행계획 확인하기
- 4단계: 두 테이블 `JOIN`과 복합 인덱스 실습하기
- 5단계: `EXPLAIN`의 예상치와 `ANALYZE`의 실제 통계 비교하기

참고로 HeidiSQL에는 과거 MariaDB의 EXPLAIN Analyzer로 결과를 보내는 기능이 소개된 적이 있지만, 해당 온라인 분석기는 현재 비활성화되어 있습니다. 따라서 HeidiSQL에서 SQL을 실행하고 결과를 직접 해석하는 방식을 중심으로 공부하는 것을 추천합니다.

MariaDB Documentation

원하시면 다음 단계로 MariaDB + HeidiSQL 전용 실행계획 실습 자료를 만들어 드릴 수 있습니다. 데이터 생성부터 인덱스, 조인, 복합 인덱스까지 단계별 SQL과 정답 해설을 포함할 수 있습니다.
