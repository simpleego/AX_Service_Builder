# Postman 입문자용 실습 가이드 · v03-jwt

Postman 데스크톱 앱을 처음 쓰는 분을 기준으로 **실행 → 파일 불러오기 → 요청 하나 보내 보기 → 실습 진행 → 한 번에 실행** 순서로 안내합니다.

- 실습 소스: `D:\jwt\AX\04-api-architecture-auth-security\LectureNote\versions\v03-jwt`
- Postman 파일: `D:\jwt\postman` (02 폴더만 따로 분리한 컬렉션 + 환경 파일)
- 서버 주소: `http://localhost:8000`

---

## 0단계: 서버 실행 확인

Postman으로 요청을 보내기 전에 API 서버가 켜져 있어야 합니다. 서버가 꺼져 있으면 PowerShell에서 아래 명령으로 실행합니다.

```powershell
cd D:\jwt\AX\04-api-architecture-auth-security\LectureNote\versions\v03-jwt
.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

브라우저에서 `http://localhost:8000/health`에 접속해 `{"status":"ok"}`가 나오면 준비된 것입니다. 서버를 끌 때는 그 터미널에서 Ctrl + C를 누릅니다.

## 1단계: Postman 실행과 화면 익히기

1. 시작 메뉴에서 **Postman**을 실행합니다. 로그인 화면이 나오면 계정으로 로그인하거나, 아래쪽의 건너뛰기 링크로 넘어가도 됩니다. 실습은 로그인 없이도 됩니다.
2. 화면은 크게 네 부분으로 나뉩니다.

| 위치 | 이름 | 하는 일 |
|---|---|---|
| 왼쪽 | **사이드바(Collections)** | 요청 목록. 폴더처럼 펼쳐 봅니다 |
| 가운데 위 | **요청 영역** | 메서드(GET/POST), 주소, Body, Headers |
| 가운데 아래 | **응답 영역** | 서버가 돌려준 결과, 상태 코드, 테스트 결과 |
| 오른쪽 위 | **환경 선택 상자** | `No environment`라고 적힌 드롭다운 |

## 2단계: 컬렉션과 환경 불러오기

1. 왼쪽 위 **Import** 버튼을 누릅니다.
2. 탐색기에서 아래 폴더를 엽니다.

   ```text
   D:\jwt\postman
   ```

3. `02_Authenticated_scenario.postman_collection.json`과 `local.postman_environment.json` 두 파일을 Import 창으로 **끌어다 놓고** **Import**를 누릅니다.
4. 오른쪽 위 환경 선택 상자에서 **Todo local**을 고릅니다. ← **가장 많이 놓치는 단계**입니다. 이걸 안 하면 `{{baseUrl}}`이 빨간색으로 표시되고 요청이 실패합니다. `{{baseUrl}}`을 직접 주소로 바꿔 입력하지 마세요. 토큰과 `todoId`도 환경 변수에 저장되기 때문에 환경을 선택해야 뒤 요청들이 동작합니다.

> **⚠️ 확인**
>
> 왼쪽 사이드바에 **`02 Authenticated scenario (v03-jwt)`** 컬렉션이 보이고, 펼쳤을 때 01~25번 요청이 바로 나오면 성공입니다.
>
> 컬렉션이 안 보이면 맨 왼쪽 세로 메뉴에서 **Collections**를 누르고, 컬렉션 이름 왼쪽의 **▶** 를 눌러 펼칩니다. 그래도 없으면 Import가 되지 않은 것이니 2단계를 다시 합니다.
>
> 참고: 원본 컬렉션(`Todo API · 4과목 단계별 실습`)에는 01·02·03 폴더가 모두 들어 있습니다. 이 가이드는 v03 실습에 필요한 02 폴더만 분리한 파일을 씁니다.

## 3단계: 요청 하나 보내 보기 (연습)

1. 사이드바에서 `02 Authenticated scenario (v03-jwt)` 컬렉션을 펼칩니다.
2. **01 A 가입 / 시나리오 초기화**를 클릭합니다.
3. 요청 영역에서 다음을 살펴봅니다.
   - 위쪽 줄: `POST` + `{{baseUrl}}/api/auth/register`. 중괄호 두 개 `{{ }}`는 **환경 변수**이고, 마우스를 올리면 실제 값(`http://localhost:8000`)이 보입니다.
   - **Body** 탭: 서버로 보내는 JSON(이메일, 비밀번호)
   - **Scripts** 탭: `Pre-request`는 보내기 전에 실행되는 코드(새 이메일 생성), `Post-response`는 응답을 받은 뒤 실행되는 코드(결과 검사, 값 저장)
4. 파란색 **Send** 버튼을 누릅니다.
5. 아래 응답 영역에서 확인합니다.
   - 오른쪽 위 상태 코드: **201 Created**
   - **Body** 탭: `{"id": ..., "email": "..."}`
   - **Test Results** 탭: 초록색 **PASS**

> **⚠️ 서버가 꺼져 있으면**
>
> `Could not send request`가 나옵니다. 0단계의 서버가 실행 중인지 확인하세요.

## 4단계: 01번부터 25번까지 차례로 Send하며 실습하기

01~25번은 컬렉션 안 요청 이름 앞에 붙은 번호입니다. **반드시 번호 순서대로** 보내야 합니다. 앞 요청이 저장한 토큰과 ID를 뒤 요청이 쓰기 때문입니다.

| 번호 | 요청 이름 | 하는 일 | 기대 결과 |
|---|---|---|---|
| 01 | A 가입 / 시나리오 초기화 | 사용자 A를 새 이메일로 회원가입 | 201 |
| 02 | 중복 가입 | 같은 이메일로 다시 가입 | 409 |
| 03 | 잘못된 비밀번호 | 틀린 비밀번호로 로그인 | 401 |
| 04 | A 로그인 / 토큰 저장 | A 로그인, 토큰을 환경 변수에 저장 | 200 |
| 05 | A Todo 생성 | A의 할 일 생성, `todoId` 저장 | 201 |
| 06 | 인증 없이 접근 | 토큰 없이 목록 조회 | 401 |
| 07 | A 목록 필터 | A의 미완료 목록 조회 | 200 |
| 08 | B 가입 | 사용자 B 회원가입 | 201 |
| 09 | B 로그인 | B 토큰 저장 | 200 |
| 10 | B로 A 상세 차단 | B가 A의 Todo 조회 | 404 |
| 11 | B로 A 수정 차단 | B가 A의 Todo 수정 | 404 |
| 12 | B로 A 삭제 차단 | B가 A의 Todo 삭제 | 404 |
| 13 | A 완료 수정 | A가 자기 Todo 수정 | 200 |
| 14 | 빈 제목 차단 | 제목 없이 생성 | 422 |
| 15 | completed 타입 차단 | completed에 문자열 입력 | 422 |
| 16 | page 범위 차단 | `page=0`으로 조회 | 422 |
| 17 | A refresh 회전 | refresh로 새 토큰 발급 | 200 |
| 18 | 이전 refresh 재사용 차단 | 17번 전의 토큰을 다시 사용 | 401 |
| 19 | 새 refresh도 family 폐기 확인 | 17번에서 받은 새 토큰 사용 | 401 |
| 20 | A 재로그인 | 다시 로그인해 새 토큰 받기 | 200 |
| 21 | A 삭제 | A가 자기 Todo 삭제 | 204 |
| 22 | 삭제 후 확인 | 지운 Todo 조회 | 404 |
| 23 | 로그아웃 | refresh 토큰 폐기 | 204 |
| 24 | 로그아웃 후 refresh 차단 | 폐기된 refresh 사용 | 401 |
| 25 | access는 만료 전까지 유효 | 로그아웃 후 access로 목록 조회 | 200 |

401, 404, 409, 422가 나오는 요청은 "막혀야 정상"인 보안 검사입니다. 기대 결과와 같은 코드가 나오면 Test Results 탭에 초록색 PASS가 표시됩니다.

**실습 단계와 연결**

| 요청 | 실습 단계 | 봐야 할 곳 |
|---|---|---|
| 01~04 | 2. 가입/로그인 | 04번 응답 Body의 `accessToken`, `refreshToken` → HeidiSQL에서 `users`, `refresh_tokens` 조회 |
| 08~13 | 4. A/B 소유권 | 10·11·12번이 모두 **404** |
| 17~19 | 5. refresh 회전 | 17번 200 → 18번 401 → 19번 401, 단계마다 HeidiSQL에서 `revoked_at` 확인 |
| 20~25 | 6. logout | 24번 refresh는 **401**, 25번 access는 **200** |

**순서가 특히 중요한 곳**

- **17번은 딱 한 번만** 보냅니다. 두 번 보내면 `oldRefreshToken`이 바뀌어 18·19번 결과가 달라집니다.
- 18번에서 토큰 family 전체가 폐기되므로 **20번에서 다시 로그인**해야 21번 이후가 동작합니다.
- 06번, 14~16번은 저장하는 값이 없어 다시 보내도 괜찮습니다.
- 중간에 꼬이면 **01번부터 다시** 시작합니다. 01번이 새 이메일로 사용자를 만들고 Postman 변수도 비웁니다.

**저장된 값 보는 법:** 오른쪽 위 환경 선택 상자 옆의 **눈 모양 아이콘**(또는 왼쪽 **Environments** 메뉴 > `Todo local`)을 누르면 `accessToken`, `todoId`, `oldRefreshToken` 같은 값이 요청을 보낼 때마다 바뀌는 것을 볼 수 있습니다.

**토큰이 헤더에 들어가는지 보는 법:** 05번 요청의 **Authorization** 탭(또는 Headers 탭)에서 `Bearer {{accessToken}}`을 확인합니다.

**HeidiSQL에서 함께 실행할 쿼리**

```sql
USE todo_course;
SELECT id, email, password_hash FROM users ORDER BY id DESC LIMIT 3;
SELECT id, user_id, family_id, expires_at, revoked_at FROM refresh_tokens ORDER BY id DESC LIMIT 5;
```

- `password_hash`는 `salt:해시` 형식이어야 하고, 비밀번호 원문은 어디에도 없어야 합니다.
- `refresh_tokens`에는 토큰 원문이 아니라 해시만 저장됩니다. access 토큰을 저장하는 테이블은 없습니다.

## 5단계: Runner로 한 번에 실행하기 (완료 기준)

1. 사이드바에서 `02 Authenticated scenario (v03-jwt)` 컬렉션에 마우스를 올리고 **…**(점 세 개) > **Run collection**을 누릅니다.
2. Runner 화면에서 환경이 **Todo local**인지 확인하고 **Run**을 누릅니다.
3. 결과 화면에서 25개 요청이 모두 초록색(Passed)인지 확인합니다. 이 화면을 캡처해 제출합니다.

> **⚠️ 주의**
>
> 원본 컬렉션(`Todo API · 4과목 단계별 실습`)을 쓸 때는 컬렉션 **전체**를 Run하지 마세요. `01` 폴더는 v01~v02용이라 v03에서는 실패합니다. 이 가이드의 분리된 컬렉션은 02 요청만 들어 있으므로 전체를 Run해도 됩니다.

명령줄로 실행할 수도 있습니다(설치된 Postman CLI 사용).

```powershell
cd D:\jwt\postman
postman collection run 02_Authenticated_scenario.postman_collection.json -e local.postman_environment.json --bail
```

## 테스트 데이터 정리 (선택)

실행할 때마다 `student-a-…`, `student-b-…` 사용자가 DB에 남지만, 01번이 매번 새 사용자로 시작하므로 **지우지 않아도 다시 테스트할 수 있습니다.** 실습을 모두 끝낸 뒤 정리하고 싶다면 HeidiSQL에서 실행합니다. Todo와 refresh 토큰은 외래 키(`ON DELETE CASCADE`)로 함께 지워집니다.

```sql
USE todo_course;
SELECT id, email FROM users WHERE email LIKE 'student-%@example.com';  -- 먼저 확인
DELETE FROM users WHERE email LIKE 'student-%@example.com';            -- 확인 후 삭제
```

---

## 막혔을 때

| 증상 | 해결 |
|---|---|
| 02 컬렉션이 안 보임 | `D:\jwt\postman`의 두 파일을 다시 Import |
| 주소의 `{{baseUrl}}`이 빨간색 | 오른쪽 위에서 환경 **Todo local**을 선택 |
| `Could not send request` | 서버가 꺼졌는지 확인하고 0단계 명령으로 다시 실행 |
| 중간 요청부터 401이 남 | 01번부터 다시 순서대로 Send (토큰이 꼬인 상태) |
| 18·19번에서 결과가 다름 | 17번을 **딱 한 번만** 보낸 뒤 18번으로 넘어가야 합니다 |
