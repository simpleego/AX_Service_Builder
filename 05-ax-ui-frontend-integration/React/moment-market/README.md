# 모먼트 마켓 — React Hooks 미니 쇼핑몰

## 실행

```bash
npm install
npm run dev
```

빌드: `npm run build` (dist 출력)

## 데이터

- GET https://jsonplaceholder.typicode.com/posts?_limit=12 : 상품 원본 id, title, body
- POST https://jsonplaceholder.typicode.com/posts : 모의 주문
- JSONPlaceholder는 실제 상품 API가 아닙니다. 예시 상품명·가격·카테고리·Unsplash 이미지를 결합합니다.
- 주문은 서버에 영구 저장되지 않고 실제 결제나 배송이 없습니다.
- 장바구니·찜·테마는 브라우저 localStorage에 저장합니다.

## 훅 사용 안내

| 훅                  | 적용 기능                                                             |
| ------------------- | --------------------------------------------------------------------- |
| useState            | 검색어, 카테고리, 정렬, 모달, 알림, 주문 상태                         |
| useEffect           | API fetch/AbortController 정리, localStorage 동기화, 단축키 등록/해제 |
| useReducer          | 장바구니 추가·수량 조정·비우기, API 재시도                            |
| useContext          | Provider에서 장바구니·찜·테마 공유                                    |
| useMemo             | 검색/필터/정렬된 상품 및 합계 계산                                    |
| useCallback         | 상품 추가·찜·알림 함수 참조 유지                                      |
| useRef              | 검색 input, 모달 DOM, 알림 타이머                                     |
| useId               | 검색 label과 dialog 제목 연결                                         |
| useDeferredValue    | 검색 입력과 결과 업데이트 우선순위 분리                               |
| useTransition       | 카테고리/정렬 업데이트 우선순위 분리                                  |
| useLayoutEffect     | 모달 표시 시 포커스 및 스크롤 잠금, 닫을 때 복원                      |
| useImperativeHandle | SearchBox의 focus 메서드 공개                                         |
| useDebugValue       | useLocalStorage의 저장 키를 DevTools에 표시                           |

커스텀 훅: `useProducts`, `useLocalStorage`.
useMemo/useCallback은 학습 예시이며 12개 상품에서는 성능 차이가 크지 않습니다.
useDeferredValue는 디바운스가 아니며 API 호출 횟수를 줄이지 않습니다.
React 19의 ref prop 대신 React 18에서도 익숙한 forwardRef 패턴을 사용합니다.

## 파일

- src/main.jsx: Provider, 커스텀 훅, 상품·장바구니·모달 컴포넌트 (학습용 주제별 함수)
- src/style.css: 반응형 화면 및 다크 테마

## 수동 확인

검색(/ 키), 카테고리, 가격 정렬, 상세 보기, 찜, 장바구니 수량/삭제,
새로고침 유지, 테마 전환, API 실패 시 재시도, 모의 주문 성공/실패,
모달 Escape/Tab 포커스 순환을 확인합니다.
