**전체 검색 → 인덱스 생성 → 실행계획 변화 → 복합 인덱스 → 잘못 만든 인덱스**

순서로 진행하는 것이 좋습니다.

---

# 1. 먼저 EXPLAIN에서 볼 항목

HeidiSQL 쿼리 탭에서 다음처럼 실행하면 됩니다.

```sql
EXPLAIN
SELECT *
FROM customer
WHERE name = '홍길동';
```

MariaDB에서 처음에는 아래 항목 정도만 보면 충분합니다.

| 항목 | 의미 | 학생이 기억할 내용 |
|---|---|---|
| `type` | 데이터를 찾는 방법 | **ALL이면 전체 검색** |
| `possible_keys` | 사용할 수 있는 인덱스 | 후보 인덱스 |
| `key` | 실제 사용한 인덱스 | `NULL`이면 인덱스 미사용 |
| `rows` | 읽을 것으로 예상하는 행 | 작을수록 좋음 |
| `Extra` | 추가 작업 | 정렬, 필터링 등 확인 |

특히 수업에서는 `type`, `key`, `rows`, `Extra` 네 개에 집중하면 됩니다.

---

# 2. 실습용 테이블 만들기

학생들이 직접 비교하기 좋도록 회원 테이블 하나를 만들겠습니다.

```sql
CREATE DATABASE IF NOT EXISTS explain_test;

USE explain_test;

DROP TABLE IF EXISTS members;

CREATE TABLE members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    age INT,
    city VARCHAR(50),
    department VARCHAR(50),
    salary INT,
    join_date DATE
);
```

데이터는 어느 정도 많아야 차이가 보입니다.

간단한 테스트는 20~30건이어도 되지만, `rows` 변화까지 보려면 **수천~수만 건**이 좋습니다.

---

# 3. 실습 1 — 가장 중요한 `ALL` 확인

먼저 인덱스가 없는 `name` 컬럼을 검색합니다.

```sql
EXPLAIN
SELECT *
FROM members
WHERE name = '홍길동';
```

예상 결과:

```text
type : ALL
key  : NULL
rows : 10000
```

핵심은 다음입니다.

> `ALL` = 테이블의 데이터를 처음부터 끝까지 찾아본다는 의미

즉,

```text
회원 10,000명
↓
홍길동을 찾기 위해
↓
최대 10,000행 검사
```

이것이 **Full Table Scan**입니다.

---

# 4. 실습 2 — 인덱스를 만들면 어떻게 바뀌는가

이번에는 `name`에 인덱스를 만듭니다.

```sql
CREATE INDEX idx_members_name
ON members(name);
```

다시 실행합니다.

```sql
EXPLAIN
SELECT *
FROM members
WHERE name = '홍길동';
```

예상 변화:

```text
type : ref
key  : idx_members_name
rows : 1
```

학생들에게는 두 결과를 비교하게 하면 좋습니다.

| 구분 | 인덱스 전 | 인덱스 후 |
|---|---:|---:|
| type | ALL | ref |
| key | NULL | idx_members_name |
| rows | 10000 | 1 |

이 실습 하나만 제대로 이해해도 인덱스의 필요성을 상당 부분 이해할 수 있습니다.

---

# 5. 실습 3 — PK 검색

`PRIMARY KEY`는 기본적으로 인덱스입니다.

```sql
EXPLAIN
SELECT *
FROM members
WHERE id = 100;
```

일반적으로:

```text
type : const
key  : PRIMARY
rows : 1
```

이때 다음처럼 설명하면 이해하기 쉽습니다.

```text
name 검색
홍길동 어디 있지?
→ 여러 위치 가능

id 검색
100번 회원 어디 있지?
→ 정확한 한 위치
```

따라서 PK 검색은 매우 효율적입니다.

---

# 6. 실습 4 — 범위 검색

이번에는 나이를 검색합니다.

```sql
CREATE INDEX idx_members_age
ON members(age);
```

실행:

```sql
EXPLAIN
SELECT *
FROM members
WHERE age BETWEEN 30 AND 39;
```

보통:

```text
type : range
key  : idx_members_age
```

여기서 `range`를 설명할 수 있습니다.

```text
age = 30
age = 31
age = 32
...
age = 39
```

특정 한 값이 아니라 **인덱스의 일정 범위**를 읽는 것입니다.

다음 조건도 같은 개념입니다.

```sql
WHERE age > 50
```

```sql
WHERE join_date >= '2026-01-01'
```

---

# 7. 실습 5 — ORDER BY와 인덱스

이번 실습은 매우 교육 효과가 좋습니다.

먼저:

```sql
EXPLAIN
SELECT *
FROM members
ORDER BY salary;
```

`salary` 인덱스가 없다면 `Extra`에서 다음과 같은 내용이 나타날 수 있습니다.

```text
Using filesort
```

의미는:

> MariaDB가 결과를 별도로 정렬해야 한다.

이제 인덱스를 생성합니다.

```sql
CREATE INDEX idx_members_salary
ON members(salary);
```

다시:

```sql
EXPLAIN
SELECT *
FROM members
ORDER BY salary;
```

실행계획 변화를 비교하게 하면 됩니다.

여기서는 학생들에게:

> 인덱스는 검색만 빠르게 하는 것이 아니라 정렬에도 영향을 줄 수 있다.

라는 점을 강조하면 좋습니다.

---

# 8. 실습 6 — 복합 인덱스

DB 최적화 수업에서 가장 중요한 실습 중 하나입니다.

먼저 복합 인덱스를 만듭니다.

```sql
CREATE INDEX idx_city_age
ON members(city, age);
```

다음 세 쿼리를 비교합니다.

### ① city만 검색

```sql
EXPLAIN
SELECT *
FROM members
WHERE city = '대전';
```

인덱스 사용 가능성이 높습니다.

---

### ② city + age

```sql
EXPLAIN
SELECT *
FROM members
WHERE city = '대전'
AND age = 30;
```

복합 인덱스를 매우 효과적으로 사용할 수 있습니다.

---

### ③ age만 검색

```sql
EXPLAIN
SELECT *
FROM members
WHERE age = 30;
```

`(city, age)` 인덱스만 있다고 가정하면 기대만큼 사용되지 않을 수 있습니다.

이를 통해 **복합 인덱스의 컬럼 순서**를 설명합니다.

```text
INDEX(city, age)

city
○

city + age
○

age
△ 또는 X
```

이 개념은 흔히 **Leftmost Prefix Rule**로 설명합니다.

---

# 9. 실습 7 — 함수 사용으로 인덱스가 무력화되는 사례

이 실습도 아주 좋습니다.

```sql
CREATE INDEX idx_join_date
ON members(join_date);
```

정상적인 쿼리:

```sql
EXPLAIN
SELECT *
FROM members
WHERE join_date = '2026-10-01';
```

이번에는:

```sql
EXPLAIN
SELECT *
FROM members
WHERE YEAR(join_date) = 2026;
```

컬럼에 함수를 적용하면 인덱스를 효율적으로 사용하지 못하는 경우가 많습니다.

그래서 일반적으로는 다음처럼 범위 조건으로 바꾸는 것이 좋습니다.

```sql
EXPLAIN
SELECT *
FROM members
WHERE join_date >= '2026-01-01'
AND join_date < '2027-01-01';
```

학생들에게 다음 차이를 보여주면 됩니다.

```text
YEAR(join_date) = 2026
        ↓
컬럼 값 가공
        ↓
인덱스 활용 불리


join_date >= ...
AND join_date < ...
        ↓
인덱스 범위 검색
```

---

# 10. 실습 8 — LIKE 검색과 인덱스

이 예제도 매우 직관적입니다.

```sql
CREATE INDEX idx_email
ON members(email);
```

먼저:

```sql
EXPLAIN
SELECT *
FROM members
WHERE email LIKE 'kim%';
```

앞부분이 고정되어 있기 때문에 인덱스를 활용할 가능성이 있습니다.

하지만 다음은 다릅니다.

```sql
EXPLAIN
SELECT *
FROM members
WHERE email LIKE '%gmail.com';
```

앞에 `%`가 붙으면 일반적인 B-Tree 인덱스를 활용하기 어렵습니다.

따라서:

```text
'kim%'
○ 비교적 인덱스 사용 가능

'%kim'
X 어려움

'%kim%'
X 어려움
```

으로 정리할 수 있습니다.

---

# 11. 실습 9 — OR 때문에 실행계획이 바뀌는 경우

```sql
CREATE INDEX idx_city
ON members(city);

CREATE INDEX idx_department
ON members(department);
```

실행:

```sql
EXPLAIN
SELECT *
FROM members
WHERE city = '대전'
OR department = '개발팀';
```

MariaDB 버전과 데이터 분포에 따라 `index_merge` 등이 나타날 수 있습니다.

학생들에게는:

> 인덱스가 있다고 항상 하나의 인덱스만 사용하는 것은 아니다.

정도로 설명하면 충분합니다.

---

# 12. 실습 10 — SELECT *와 Covering Index 개념

조금 고급 과정으로 넘어가면 좋은 예제입니다.

```sql
CREATE INDEX idx_city_name
ON members(city, name);
```

먼저:

```sql
EXPLAIN
SELECT *
FROM members
WHERE city = '대전';
```

그리고:

```sql
EXPLAIN
SELECT city, name
FROM members
WHERE city = '대전';
```

두 번째 쿼리에서는 상황에 따라:

```text
Using index
```

가 나타날 수 있습니다.

즉, 테이블까지 가지 않고 **인덱스 안에 있는 데이터만으로 결과를 반환**할 수 있습니다.

이것이 Covering Index의 핵심입니다.

---

# 13. 학생 실습으로 가장 좋은 비교 문제

저라면 실제 수업에서는 다음 7문제를 순서대로 시킵니다.

| 단계 | 실습 | 핵심 |
|---|---|---|
| 1 | `WHERE name=...` | Full Table Scan |
| 2 | name 인덱스 생성 | `ALL → ref` |
| 3 | PK 검색 | `const`, `PRIMARY` |
| 4 | age BETWEEN | `range` |
| 5 | `(city, age)` | 복합 인덱스 |
| 6 | `YEAR(join_date)` | 함수와 인덱스 |
| 7 | `LIKE 'kim%' / '%kim'` | LIKE와 인덱스 |

이 정도면 **EXPLAIN 1~2시간 실습**으로 매우 적당합니다.

---

# 14. 학생들에게 이렇게 읽도록 지도하면 좋습니다

`EXPLAIN` 결과를 너무 복잡하게 가르치면 어렵습니다.

처음에는 아래 순서로만 읽게 하십시오.

```text
① type을 본다
       ↓
ALL인가?

② key를 본다
       ↓
인덱스를 사용했나?

③ rows를 본다
       ↓
얼마나 많은 데이터를 읽나?

④ Extra를 본다
       ↓
filesort 같은 추가 작업이 있나?
```

즉,

> **ALL → key → rows → Extra**

정도로 읽기 습관을 만들어주는 것이 좋습니다.

---

# 15. EXPLAIN에서 type은 이 정도만 기억하면 됩니다

초보자 과정이라면 모든 `type`을 암기시킬 필요는 없습니다.

대략 다음 순서만 알려줘도 충분합니다.

```text
좋음
 ↑

const
eq_ref
ref
range
index
ALL

 ↓
나쁨
```

특히:

```text
ALL
```

을 만나면

> "전체 데이터를 읽고 있구나."

라고 생각하도록 지도하면 됩니다.

다만 **`ALL`이 항상 잘못된 것은 아닙니다.**

테이블 데이터가 아주 적거나 조회 결과가 대부분의 행인 경우에는 MariaDB 옵티마이저가 의도적으로 Full Scan을 선택하는 것이 더 빠를 수도 있습니다.

---

## 강의에서 가장 효과적인 핵심 메시지

학생들에게 마지막에 이렇게 정리해주면 좋습니다.

```text
SQL 작성
   ↓
MariaDB Optimizer
   ↓
어떤 방법으로 데이터를 찾을지 결정
   ↓
Execution Plan
   ↓
EXPLAIN으로 확인
```

즉,

**EXPLAIN은 "내 SQL을 MariaDB가 실제로 어떻게 실행하려고 하는지 엿보는 도구"**입니다.

그리고 인덱스 수업에서 가장 중요한 것은 단순히

```sql
CREATE INDEX ...
```

를 외우는 것이 아니라,

```text
인덱스 생성
→ EXPLAIN 확인
→ 실제 사용 여부 확인
→ rows 비교
```
