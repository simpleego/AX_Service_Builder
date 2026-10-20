# FastAPI ↔ Vanilla JS 통신 방식 17종 통합 실습

GitHub 문서 `02-ai-augmented-backend/08. 클라이언트_서버 통신방식.md`를 바탕으로 제작한 교육용 실습 코드입니다.

## 설치와 실행 (Windows 11, VS Code)

1. 폴더를 열고 VS Code 터미널에서 다음 명령을 실행합니다.

```powershell
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

2. VS Code에서 `frontend/index.html`을 **Live Server로 열기(Open with Live Server)** 하여 `http://127.0.0.1:5500`으로 접속합니다.
3. `http://127.0.0.1:8000/docs`에서 API를 개별 실습할 수도 있습니다.

**주의:** VS Code Live Server가 5500이 아닌 다른 포트를 쓰면, `backend/main.py`의 `allow_origins`에 해당 주소를 추가하세요. 전통 HTML Form 결과의 '돌아가기' 링크는 5500 포트로 고정되어 있습니다.

## 실습 목록

1. Path Parameter · 2. Query String · 3. HTML Form · 4. XMLHttpRequest/AJAX · 5. Fetch GET · 6. JSON POST(성적 계산) · 7. REST CRUD · 8. URLSearchParams · 9. FormData · 10. File Upload · 11. Header · 12. Cookie · 13. Polling · 14. Long Polling · 15. SSE · 16. WebSocket · 17. Streaming Response

## 개발자 도구 실습

- F12 → Network → Fetch/XHR: 메서드/URL/Status/Payload/Response 확인
- SSE: `events` 요청 선택 후 이벤트 메시지 확인
- WebSocket: `ws` 요청의 Messages에서 송수신 확인
- Cookie: Application → Cookies에서 `demo_username` 확인

## 교육용 설계 및 유의사항

- REST 학생 데이터는 메모리에 저장되므로 서버 재시작 시 초기화됩니다. DB는 연결하지 않았습니다.
- 파일 업로드는 최대 5MB까지만 읽으며 실제 파일을 저장하지 않습니다.
- Cookie 데모는 단순 상태 유지 예제이며, **실제 로그인 인증에 사용해서는 안 됩니다**.
- Header의 `demo-key-123`은 공개된 교육용 문자열이며 실제 API 키가 아닙니다.
- Polling은 전체 학습자가 같은 서버 프로세스를 사용할 경우 카운터를 공유합니다.
- Long Polling은 실제 변경 이벤트가 아닌 5초 대기 방식으로 개념만 재현합니다.
- SSE는 완료 후 연결을 닫으며 자동 재연결을 막습니다.
- HTML Form은 HTML 페이지 이동을 보여주고 나머지 대부분의 예제는 페이지 이동 없이 응답을 결과 모니터에 출력합니다.
- 로컬 `127.0.0.1` 사용 기준입니다. 배포 시 HTTPS, WSS, 인증, DB, 입력 검증, CORS 정책을 재설계해야 합니다.
