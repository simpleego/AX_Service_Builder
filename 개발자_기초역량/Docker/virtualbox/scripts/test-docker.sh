#!/usr/bin/env bash
# ============================================================
#  Docker 동작 확인 (VM 안에서 실행: bash test-docker.sh)
# ============================================================
set -e

echo "==> hello-world"
docker run --rm hello-world | head -n 3

echo "==> nginx 를 VM 80 포트로 실행 (Windows 에서 http://localhost:8080 으로 접속)"
docker rm -f lab-nginx >/dev/null 2>&1 || true
docker run -d --name lab-nginx -p 80:80 nginx:alpine >/dev/null
sleep 2
curl -s -o /dev/null -w "VM 내부 응답코드: %{http_code}\n" http://localhost:80

echo
echo "Windows 브라우저에서 http://localhost:8080 을 열어 'Welcome to nginx!' 가 보이면 성공입니다."
echo "정리: docker rm -f lab-nginx"
