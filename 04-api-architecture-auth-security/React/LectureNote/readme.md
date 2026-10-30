# 처음 만난 React v18 — Chapter 08–15 강의 패키지

대상: JSX, 컴포넌트, props, useState 기초를 배운 입문자. 목표: 이벤트에서 Context와 스타일링까지 연결하여 작은 React 화면을 설계한다.

요청의 `chapter_08부터 끝까지`를 실제 저장소의 마지막 폴더인 `chapter_15`까지로 해석했다. 잘못 연결된 `https://github.chapter_0` 대신 처음 제공한 GitHub 저장소의 실제 폴더를 확인했다.

## 자료 구성

- [통합 강의안](강의안.md): 8개 챕터의 학습 목표, 원본 파일별 해설, 이론, 코드, 실습, 확인 문제와 해설.
- [강사 운영안 및 평가](강사운영안.md): 진행 시간, 시연 순서, 통합 과제, 평가 기준.
- [실행 안내](examples/README.md): 독립 실행 가능한 추가 예제 앱.
- `reference/`: 분석에 사용한 원본 13개 JSX와 package.json, index.js, README.md 스냅샷. 원저작자의 소스이며 추가 제작 예제와 구분한다.
- `examples/src/chapter_08.jsx`부터 `chapter_15.jsx`: 강의용으로 새로 작성한 개선·확장 예제.
- [검증 기록](검증기록.md): 실행한 검사와 남은 확인 범위.

## 차시 구성

| 챕터 | 주제 | 원본 진입 컴포넌트 | 권장 시간 |
|---|---|---|---|
| 08 | 이벤트 처리 | ConfirmButton | 60분 |
| 09 | 조건부 렌더링 | LandingPage | 60분 |
| 10 | 리스트와 key | AttendanceBook | 75분 |
| 11 | 제어 폼과 제출 | SignUp | 90분 |
| 12 | 상태 끌어올리기 | Calculator | 90분 |
| 13 | 컴포넌트 합성 | ProfileCard | 60분 |
| 14 | Context | DarkOrLight | 90분 |
| 15 | styled-components | Blocks | 75분 |

총 600분, 휴식과 별도 통합 과제 시간 제외. 각 차시는 원본 관찰 → 개념 설명 → 개선 코드 실행 → 과제 → 확인 문제 순서다.

## 출처와 버전

분석 기준일: 2026-10-30. 원본: [soaple/first-met-react-practice-v18](https://github.com/soaple/first-met-react-practice-v18/tree/master/src). 고정 커밋: `3adbe9bf8a01109abb0b675ace9ae1e0eaf8af41`.

원본 package.json은 React `^18.2.0`, react-dom `^18.2.0`, react-scripts `5.0.1`, styled-components `^5.3.5`다. 추가 예제는 React/ReactDOM `18.2.0`, styled-components `5.3.5`를 명시하며 Vite로 실행한다. 원본 CRA의 실행 방식과 추가 예제의 실행 방식을 혼동하지 않는다. 현재 React 공식 문서는 더 최신 버전이므로 이 강의는 React 18에서도 사용 가능한 API와 `<ThemeContext.Provider>` 문법을 쓴다.

원본 README의 앱 생성 안내는 저자의 안내로 보존했다. 이 강의의 추가 예제는 앱을 새로 생성하는 명령 없이 제공된 프로젝트를 설치해 실행한다. 원본 저장소의 라이선스 파일은 조회한 트리에 없었다. 원본 스냅샷을 외부 재배포할 때는 저작권자의 이용 조건을 별도로 확인한다.
