# 성적 관리 서비스 VM 배포 테스트

**목적:** 수업 전에 완성본(`sungjuk-service`)을 VirtualBox 우분투 VM에 올려 전체 서비스가 정상 동작하는지 확인한다.
**소요 시간:** 약 15분
**관련 문서:** [fullstack_service_for_docker.md](fullstack_service_for_docker.md) (수업 진행 문서)
**완성본 위치:** `E:\AX_FullStack_Builder\Docker\sungjuk-service\`

---

## 0. 사전 조건

| 항목 | 확인 방법 |
|---|---|
| SSH 접속 가능 | `ssh -p 2222 vboxuser@127.0.0.1` |
| Docker·Compose 설치 | `docker --version`, `docker compose version` |
| 포트 포워딩 규칙 | `ssh` 2222→22, `web` 8080→8080, `sungjuk-db` 3307→3307 |

> 설치·설정 방법은 [fullstack_service_for_docker.md의 2장](fullstack_service_for_docker.md#2-강사-사전-준비-환경-점검)을 참고합니다.

---

## 1. 완성본 복사 (Windows PowerShell 새 창)

SSH로 접속한 창이 아니라 **Windows PowerShell 창**에서 실행합니다.

```powershell
scp -P 2222 -r E:\AX_FullStack_Builder\Docker\sungjuk-service vboxuser@127.0.0.1:~
```

---

## 2. 실행 (SSH로 접속한 우분투 창)

```bash
cd ~/sungjuk-service
ls -la                      # .env, compose.yaml, db, backend, frontend 확인
docker compose up -d --build
```

- 처음에는 이미지를 받고 빌드하느라 **2~5분** 정도 걸립니다.
- `permission denied`가 나오면 docker 그룹이 아직 적용되지 않은 것입니다. 명령 앞에 `sudo`를 붙이세요.

---

## 3. 상태 확인

```bash
docker compose ps
```

| 서비스 | 정상 상태 |
|---|---|
| `db` | `Up ... (healthy)` |
| `backend` | `Up` |
| `frontend` | `Up` |

하나라도 `Restarting`이나 `Exited`면 그 서비스의 로그를 확인합니다.

```bash
docker compose logs backend
```

---

## 4. API 자동 점검

아래 블록을 **통째로 붙여넣으면** CRUD와 오류 응답을 한 번에 점검합니다.

```bash
A=localhost:8000/api/scores; H="Content-Type: application/json"
c(){ curl -s -o /dev/null -w "%{http_code}" "$@"; }
echo "health   $(c localhost:8000/api/health)  기대값 200"
echo "list     $(c $A)  기대값 200"
echo "create   $(c -X POST $A -H "$H" -d '{"hakbun":"T001","name":"테스트","kor":90,"eng":80,"math":70}')  기대값 201"
ID=$(curl -s "$A?q=T001" | grep -o '"id":[0-9]*' | head -1 | cut -d: -f2)
echo "get      $(c $A/$ID)  기대값 200 (id=$ID)"
echo "update   $(c -X PUT $A/$ID -H "$H" -d '{"hakbun":"T001","name":"테스트","kor":100,"eng":100,"math":100}')  기대값 200"
echo "dup      $(c -X POST $A -H "$H" -d '{"hakbun":"T001","name":"중복","kor":1,"eng":1,"math":1}')  기대값 409"
echo "invalid  $(c -X POST $A -H "$H" -d '{"hakbun":"T002","name":"x","kor":150,"eng":0,"math":0}')  기대값 422"
echo "delete   $(c -X DELETE $A/$ID)  기대값 204"
echo "notfound $(c $A/$ID)  기대값 404"
```

**판정:** 각 줄의 왼쪽 숫자가 오른쪽 `기대값`과 같으면 정상입니다.

| 항목 | 점검 내용 | 기대값 |
|---|---|---|
| health | 백엔드 → DB 연결 | 200 |
| list | 목록 조회 | 200 |
| create | 등록 | 201 |
| get | 한 명 조회 | 200 |
| update | 수정 | 200 |
| dup | 학번 중복 등록 차단 | 409 |
| invalid | 점수 범위(0~100) 검증 | 422 |
| delete | 삭제 | 204 |
| notfound | 삭제된 데이터 조회 | 404 |

> 테스트 데이터(`T001`)는 점검 과정에서 삭제되므로 샘플 데이터는 그대로 남습니다.

### 한글 데이터 확인

```bash
curl -s localhost:8000/api/scores | head -c 300; echo
```

`"name":"홍길동"`처럼 보이면 정상입니다. `???`나 깨진 글자가 보이면 `init.sql`의 `SET NAMES utf8mb4`를 확인합니다.

---

## 5. 브라우저 확인 (Windows)

| 주소 | 확인할 내용 |
|---|---|
| `http://localhost:8080` | 오른쪽 위 🟢 서버 정상, 샘플 5명 목록 |
| `http://localhost:8080/api/docs` | Swagger 화면 |

**기능 체크리스트**

- [ ] 목록에 총점·평균·학점이 계산되어 나온다
- [ ] 새 학생 **등록** → 목록에 바로 추가된다
- [ ] **수정** 버튼 → 폼에 값이 채워지고, 저장하면 목록에 반영된다
- [ ] **삭제** 버튼 → 확인 창 → 목록에서 사라진다
- [ ] 이름이나 학번으로 **검색**된다
- [ ] 이미 있는 학번으로 등록하면 "이미 등록된 학번입니다"가 나온다

---

## 6. HeidiSQL 확인

| 항목 | 값 |
|---|---|
| 네트워크 유형 | MySQL (TCP/IP) |
| 호스트 / 포트 | `127.0.0.1` / `3307` |
| 사용자 / 암호 | `simple` / `pjc0129` |
| 데이터베이스 | `sungjuk` |

`score` 테이블에서 브라우저에 보이는 것과 같은 데이터가 보이면 정상입니다.

---

## 7. 테스트 후 정리

| 상황 | 명령 |
|---|---|
| 수업 때 수강생과 **처음부터 다시** 만들 예정 | `docker compose down -v` (컨테이너 + 데이터 삭제) |
| 수업 때 **바로 시연**할 예정 | 그대로 둔다 |
| 잠시 멈춰 둘 예정 (데이터 유지) | `docker compose down` |

---

## 8. 문제가 생겼을 때

| 증상 | 확인할 것 |
|---|---|
| `docker compose ps`에서 backend가 `Restarting` | `docker compose logs --tail 30 backend` → DB 접속 정보, `.env` 값 |
| db가 `healthy`가 되지 않음 | `docker compose logs --tail 30 db`, `free -h`로 메모리 확인 |
| health가 `503` | db 컨테이너 상태 확인 (`docker compose ps`) |
| health가 `000` | backend가 떠 있지 않음 → `docker compose logs backend` |
| 브라우저 접속 안 됨 | 포트 포워딩 8080 규칙, `docker compose ps`의 frontend 상태 |
| 브라우저에 `502 Bad Gateway` | backend 중지 → `docker compose logs backend` |
| HeidiSQL 접속 안 됨 | 포트 포워딩 3307 규칙, 기존 `mysql-lab`(3306)과 포트를 혼동하지 않았는지 |
| `port is already allocated` | `docker ps`로 같은 포트를 쓰는 컨테이너 확인, `.env` 포트 변경 |

원인을 찾을 때는 아래 명령의 결과가 가장 도움이 됩니다.

```bash
docker compose ps
docker compose logs --tail 30 backend
docker compose logs --tail 30 db
```
