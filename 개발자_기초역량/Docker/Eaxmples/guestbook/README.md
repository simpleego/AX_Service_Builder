# Docker 방명록 실습 파일

[docker_mysql_fastapi_실습.md](../docker_mysql_fastapi_실습.md) 교안의 완성 코드입니다.
브라우저 → Nginx(web) → FastAPI(api) → MySQL 8.4(db)

```
guestbook/
├── .env.example     # 복사해서 .env로 사용
├── compose.yaml
├── db/init.sql
├── api/  Dockerfile, requirements.txt, main.py
└── web/  Dockerfile, nginx.conf, index.html
```

## 1. Ubuntu VM으로 복사 (Windows PowerShell에서)

```powershell
scp -r .\guestbook student01@<VM_IP>:~/docker-lab/
```

NAT + 포트 포워딩 환경이라면:

```powershell
scp -P 2222 -r .\guestbook student01@127.0.0.1:~/docker-lab/
```

## 2. 실행 (Ubuntu에서)

```bash
cd ~/docker-lab/guestbook
cat > .env <<EOF
COMPOSE_PROJECT_NAME=$USER
MYPORT=$MYPORT
DB_ROOT_PASSWORD=root1234
DB_NAME=guestbook
DB_USER=app
DB_PASSWORD=app1234
EOF

docker compose up -d --build
docker compose ps
curl http://localhost:$MYPORT/api/health
```

브라우저: `http://<VM_IP>:<내 포트>` (Swagger: `/api/docs`)

## 3. 정리

```bash
docker compose down      # 데이터 유지
docker compose down -v   # 데이터까지 삭제
```

> 이 파일들은 교안의 4단계(Compose 배포) 완성본입니다. 1~3단계는 교안을 보며 직접 작성하는 것을 권합니다.
