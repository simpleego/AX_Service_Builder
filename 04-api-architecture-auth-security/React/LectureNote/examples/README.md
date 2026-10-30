# 추가 예제 실행 안내

이 디렉터리는 원본을 수정하지 않고 만든 별도 학습용 앱이다. API, 데이터베이스, 실제 로그인 기능은 없다. 새로고침하면 상태가 초기화된다.

## 실행

Node.js 22 LTS 계열과 npm을 권장한다. PowerShell에서 다음 순서로 실행한다.

```powershell
cd D:\working\React\react-ch08-15-course\examples
npm install
npm run dev
```

터미널이 표시하는 로컬 주소로 접속한다. 종료는 Ctrl+C. 배포용 번들은 `npm run build`로 만들며 결과는 `dist`에 생성된다.

## 파일과 강의 연결

| 파일 | 학습 내용 | 확인할 행동 |
|---|---|---|
| src/chapter_08.jsx | 클릭과 상태 전환 | 확인 후 비활성화, 다시 확인으로 복구 |
| src/chapter_09.jsx | 조건과 콜백 props | 체험 로그인/로그아웃으로 화면 전환 |
| src/chapter_10.jsx | map/filter, 불변 업데이트 | 출석 체크 후 검색·순서 변경 |
| src/chapter_11.jsx | value/checked, 검증 | 공백 이름·미체크 거부, 유효 정보 표시 |
| src/chapter_12.jsx | 공통 부모 상태 | 섭씨와 화씨 동기화, 잘못된 입력 안내 |
| src/temperature.js | 순수 함수 | 변환·엄격한 문자열 검사·표시 반올림 |
| src/chapter_13.jsx | children, footer 슬롯 | 카드 내부 저장 상태 전환 |
| src/chapter_14.jsx | Provider와 소비자 | 중간 Layout에 테마 props 없이 변경 |
| src/chapter_15.jsx | 동적 스타일 | compact 상태로 모든 블록 여백 변경 |

각 JSX는 React를 import한다. Vite 기본 JSX 변환으로 실행하도록 구성했다. 챕터를 바꾸면 컴포넌트가 교체되어 실습 상태가 초기화된다.

## 원본을 직접 실행하려면

별도 위치에 원본 저장소를 clone하고 해당 저장소에서 의존성을 설치한 뒤 `npm start`를 사용한다. 원본 `src/index.js`는 현재 `<Blocks />`를 렌더링한다. 다른 원본 예제를 보려면 그 JSX를 `<ConfirmButton />`, `<LandingPage />` 등으로 교체한다. 추가 예제의 `npm run dev`와 다른 명령이다.

## 수업 중 오류 해결

- `Cannot find package`: examples 폴더에서 `npm install`을 완료했는지 확인한다.
- 포트 사용 중: Vite가 출력한 다른 포트를 사용한다.
- 빈 화면: 브라우저 콘솔에서 첫 오류를 확인하고 import 파일명·대소문자를 점검한다.
- 입력이 바뀌지 않음: `value`만 설정하고 `onChange`를 빠뜨렸는지 확인한다.
- CSS용 prop 경고: 15장에서는 `$padding`, `$backgroundColor`를 사용한다.
