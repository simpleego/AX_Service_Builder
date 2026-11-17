#!/usr/bin/env bash
# ============================================================
#  VM(Ubuntu) 안에서 Docker Engine 설치
#  - Docker 공식 apt 저장소 사용 (docker-ce, compose plugin, buildx)
#  - Ubuntu 를 직접 설치한 경우에도 이 스크립트만 실행하면 됩니다:
#      sudo bash install-docker.sh
# ============================================================
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "root 권한이 필요합니다: sudo bash $0" >&2
  exit 1
fi
TARGET_USER="${SUDO_USER:-$(logname 2>/dev/null || echo root)}"

echo "==> 기존/충돌 패키지 제거"
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do
  apt-get remove -y "$pkg" >/dev/null 2>&1 || true
done

echo "==> 필수 패키지"
apt-get update
apt-get install -y ca-certificates curl gnupg

echo "==> Docker 공식 GPG 키 / 저장소 등록"
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
. /etc/os-release
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu ${UBUNTU_CODENAME:-$VERSION_CODENAME} stable" \
  > /etc/apt/sources.list.d/docker.list

echo "==> Docker Engine 설치"
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

systemctl enable --now docker containerd

echo "==> '$TARGET_USER' 사용자를 docker 그룹에 추가 (sudo 없이 docker 사용)"
if [ "$TARGET_USER" != "root" ]; then
  usermod -aG docker "$TARGET_USER"
fi

# 공유 폴더(/media/sf_*) 접근 권한
if getent group vboxsf >/dev/null && [ "$TARGET_USER" != "root" ]; then
  usermod -aG vboxsf "$TARGET_USER"
fi

echo
docker --version
docker compose version
echo
echo "설치 완료. 그룹 변경을 적용하려면 로그아웃 후 다시 접속하세요 (exit 후 재접속)."
