# TagTodo — 학생용 스타터 코드 (과목 4: API 아키텍처 & 인증 보안 설계)

강의안(`04-lecture-plan-tagtodo.md`) 1~7일차 실습용 스타터입니다.
**TODO 주석이 있는 함수를 직접 구현하세요. AI 도구(Copilot·ChatGPT·Claude 등)는 사용하지 않습니다.**

## 실행 방법
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## 채워야 할 파일 순서 (일차 순서와 동일)

| 일차 | 파일 | 구현할 내용 |
|---|---|---|
| 2 | `app/repositories/*.py` | DB 접근 함수 |
| 3 | `app/core/security.py` | 해싱, JWT 발급/검증 |
| 3 | `app/services/auth_service.py` (signup, login) | 회원가입·로그인 |
| 3 | `app/dependencies.py` | 현재 사용자 추출 |
| 3 | `app/routers/auth.py` (signup, login) | 라우터 연결 |
| 4 | `app/services/auth_service.py` (issue_tokens, refresh, logout) | 토큰 재발급·폐기 |
| 4 | `app/routers/auth.py` (refresh, logout) | 라우터 연결 |
| 5 | `app/routers/oauth.py` | 소셜 로그인 |
| 6 | `app/services/todo_service.py`, `app/services/tag_service.py` | 소유권 검증, 태그 |
| 6 | `app/routers/todos.py`, `app/routers/tags.py` | 라우터 연결 |

## 막혔을 때
1. 먼저 강의안의 해당 일차 섹션(비유 + 다이어그램)을 다시 읽기
2. 함수 docstring의 TODO 힌트 다시 읽기
3. 에러 메시지를 처음부터 끝까지 직접 읽기 (마지막 줄만 보지 말기)
4. 그래도 안 되면 강사에게 질문 — **AI 도구에 묻지 않기**

## 검증
막히지 않고 끝까지 구현했다면 `/docs`(Swagger)에서 모든 엔드포인트를 눈으로 확인하고,
7일차에 Postman Collection으로 전체 시나리오를 직접 검증합니다.
