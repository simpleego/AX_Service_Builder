# Google OAuth 클라이언트 생성 방법

socialAuth 서버의 Google 로그인(`/api/auth/google`)에 필요한 **클라이언트 ID / Secret**을 발급받는 절차입니다. (소요 약 10분)

## 1. 프로젝트 만들기

1. https://console.cloud.google.com 에 Google 계정으로 로그인합니다.
2. 상단의 프로젝트 선택 메뉴에서 **새 프로젝트**를 누릅니다.
3. 이름(예: `social-auth-practice`)을 입력하고 **만들기**를 누른 뒤, 만든 프로젝트를 선택합니다.

## 2. 동의 화면 구성 (Google Auth Platform)

1. 왼쪽 메뉴에서 **API 및 서비스 → OAuth 동의 화면**으로 들어갑니다. **Google Auth Platform** 화면으로 이동합니다.
2. **시작하기**를 누르고 다음 값을 입력합니다.
   - **앱 정보:** 앱 이름(예: `Social Auth Practice`), 사용자 지원 이메일(본인 이메일)
   - **대상(Audience):** **외부(External)**
   - **연락처 정보:** 본인 이메일
   - 약관에 동의한 뒤 **만들기**
3. 왼쪽의 **대상(Audience)** 메뉴로 갑니다. **테스트 사용자 → Add users**에서 로그인에 쓸 Gmail 주소를 추가합니다.
   - 앱이 "테스트" 상태일 때는 여기에 등록한 계정만 로그인할 수 있습니다.

> 범위(Scope)는 따로 추가하지 않아도 됩니다. 서버가 요청하는 `openid email profile`은 기본 범위입니다.

## 3. OAuth 클라이언트 만들기

1. 왼쪽의 **클라이언트(Clients)** 메뉴에서 **+ 클라이언트 만들기**를 누릅니다.
2. **애플리케이션 유형:** **웹 애플리케이션**
3. **이름:** 아무거나 입력합니다(예: `socialAuth local`).
4. **승인된 리디렉션 URI**에 **+ URI 추가**를 누르고 아래 값을 정확히 입력합니다.

   ```
   http://localhost:8000/api/auth/google/callback
   ```

   - `127.0.0.1`이 아니라 `localhost`, 포트 `8000`, 끝에 `/` 없이 입력해야 합니다.
   - "승인된 JavaScript 원본"은 비워 둬도 됩니다.
5. **만들기**를 누르면 **클라이언트 ID**와 **클라이언트 보안 비밀번호(Secret)**가 표시됩니다.
   - Secret은 이 창에서만 전체가 보일 수 있으니 바로 복사하거나 **JSON 다운로드**를 눌러 두세요.

## 4. 서버에 적용

`.env` 파일에 두 값을 넣습니다.

```
GOOGLE_CLIENT_ID=1234567890-xxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxxxxx
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
```

서버를 8000번 포트로 다시 시작합니다.

```powershell
.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

브라우저에서 `http://localhost:8000/api/auth/google`에 접속합니다. 계정을 선택하고 동의하면 콜백 화면에 앱 토큰 JSON(`accessToken`, `refreshToken`)이 표시됩니다.

## 참고

- 클라이언트를 막 만들었거나 리디렉션 URI를 고친 직후에는 반영까지 몇 분 걸릴 수 있습니다. 그 사이에는 `redirect_uri_mismatch` 오류가 날 수 있습니다.
- 로그인할 때 "Google에서 확인하지 않은 앱"이라는 경고가 나오면 **계속**을 누르면 됩니다. 테스트 모드에서는 정상입니다.
- 브라우저 주소와 콜백 주소에 `localhost`와 `127.0.0.1`을 섞어 쓰지 마세요. 쿠키와 redirect_uri가 정확히 일치해야 합니다.
- 콜백 URL을 복사해 다시 호출하면 `400 INVALID_STATE`가 나옵니다. state는 한 번만 쓸 수 있으므로 정상입니다.
