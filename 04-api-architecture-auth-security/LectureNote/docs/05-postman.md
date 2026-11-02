# Postman 실습

## 환경 설정

Postman 데스크톱 앱에서 Import를 눌러 `postman/Todo-Course.postman_collection.json`과 `postman/local.postman_environment.json`을 불러옵니다. 환경 `Todo local`을 선택하고 baseUrl이 `http://localhost:8000`인지 확인합니다. 웹 앱이라면 localhost 접근이 가능한 Desktop Agent가 필요할 수 있습니다. JSON 본문은 raw → JSON으로 설정되어 있습니다.

|변수|용도|
|---|---|
|baseUrl|서버 URL, 끝에 /를 붙이지 않음|
|password|공개된 수업용 비밀번호, 실제 비밀번호 사용 금지|
|emailA/emailB|Runner 시작 시 매번 새로 생성|
|todoId|생성 응답에서 자동 저장|
|accessToken/refreshToken|A 또는 수동 Google 로그인 응답|
|accessTokenB/refreshTokenB|소유권 검증용 B 사용자|
|oldRefreshToken|회전 전 토큰, 재사용 공격 확인용|

토큰 값은 로컬 환경에만 두고 공유/동기화/내보내기에 주의합니다. 배포된 환경 파일에는 실제 토큰과 비밀값이 없습니다.

## 버전에 맞는 폴더만 실행

- v01~v02: `01 Public CRUD (v01-v02 only)`의 10개 요청.
- v03~v06: `02 Authenticated scenario (v03-v06)`의 25개 요청.
- v04~v06: Google 브라우저 로그인 완료 후 `03 Google manual follow-up (v04-v06)`의 4개 요청.

폴더의 Run folder/Runner를 사용해 1회, 표시된 순서대로 실행합니다. **컬렉션 전체를 한 번에 실행하면 버전별 인증 조건이 달라 실패합니다.** 먼저 첫 요청부터 개별 Send로 실행해 본문·상태·헤더를 관찰한 뒤 Runner를 사용하세요. 인증 폴더는 첫 요청에서 매번 새 이메일을 만들기 때문에 반복 실행할 수 있습니다. 실습 사용자는 DB에 남습니다.

## 반드시 관찰할 항목

1. 생성의 201/Location, 삭제의 204/빈 본문, 없는 리소스의 404.
2. 입력 검증 422: 빈 제목, completed 문자열, owner_id 주입, page=0.
3. 로그인 응답의 TokenPair를 환경변수에 저장하는 Post-response 스크립트.
4. Authorization 헤더에 `Bearer {{accessToken}}`가 들어가는지 확인.
5. A의 Todo ID로 B가 상세·수정·삭제 요청을 보내도 404인지 확인.
6. refresh 후 새 토큰 값과 oldRefreshToken의 차이 확인.
7. 이전 refresh 재사용 401 → 새 refresh도 401로 family 전체 폐기 확인.
8. 재로그인 → 삭제 → 로그아웃 → refresh 401 → 기존 access는 만료 전 유효.

예시 응답 검증 스크립트:

```javascript
// 성공 응답에서만 값을 저장한다. 실패 응답으로 기존 정상 토큰을 덮어쓰지 않는다.
pm.test('HTTP 200', () => pm.response.to.have.status(200));
if (pm.response.code === 200) {
  const tokens = pm.response.json();
  pm.environment.set('accessToken', tokens.accessToken);
  pm.environment.set('refreshToken', tokens.refreshToken);
}
```

## 추가 수동 테스트

- JWT 서명을 바꾸어 Todo 조회 → 401. 원본 토큰으로 복구합니다.
- 15분 후 원래 access로 요청 → 401. 시간 경과 테스트는 pytest에서 만료 JWT를 생성해 별도 검증합니다.
- 제목 201자, null PATCH, 빈 PATCH, limit=101 → 422.
- SQL 형태 문자열을 제목에 넣어도 데이터로 저장되는지 확인하고 삭제합니다.
- v02 이상에서 `/openapi.json`, v05 이상에서 `/docs`를 조회합니다.
- Google callback에 쿠키 없이 잘못된 state를 전달하면 400. Google 설정이 비어 있으면 먼저 설정하거나 503을 예상합니다.

## Newman CLI 선택 실행

인터넷 접근 가능한 Node.js 환경에서 다음과 같이 같은 컬렉션을 실행할 수 있습니다. API 서버는 별도로 실행 중이어야 합니다.

```powershell
npx newman run postman/Todo-Course.postman_collection.json -e postman/local.postman_environment.json --folder "02 Authenticated scenario (v03-v06)" --bail
```

CLI 설치/실행은 필수가 아닙니다. 실제 Postman Runner 결과와 실패 요청/응답을 제출하면 됩니다. 학생별 제출물은 API 계약, 버전별 소스 변경, DB 테이블 캡처(비밀 제외), Runner 결과, 소유권 차단과 refresh 재사용 검증 결과입니다.
