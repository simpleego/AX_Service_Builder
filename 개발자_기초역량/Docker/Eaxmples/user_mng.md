# Ubuntu 수강생 계정 생성 가이드

VirtualBox에 설치한 Ubuntu에 수강생이 원격(SSH)으로 접속할 수 있도록 사용자 계정을 만드는 절차입니다.

---

## 1. 사전 준비: SSH 서버 설치

수강생이 원격으로 접속하려면 SSH 서버가 필요합니다.

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
sudo systemctl status ssh        # active (running) 확인
ip a                             # 서버 IP 확인 (예: enp0s3의 inet 주소)
```

방화벽(ufw)을 쓰고 있다면 SSH 포트를 열어 줍니다.

```bash
sudo ufw allow ssh
```

---

## 2. 사용자 계정 1개 만들기

```bash
sudo adduser student01           # 대화형: 비밀번호와 이름 입력 (권장)
```

비대화형으로 만들 때:

```bash
sudo useradd -m -s /bin/bash student01      # -m: 홈 디렉터리 생성, -s: 기본 셸
sudo passwd student01                        # 비밀번호 설정
```

첫 로그인 때 비밀번호를 바꾸도록 강제:

```bash
sudo chage -d 0 student01
```

---

## 3. 권한 관련 설정 (선택)

```bash
# 수강생 그룹을 만들고 사용자를 넣기
sudo groupadd students
sudo usermod -aG students student01

# sudo 권한 주기 (실습에 관리자 권한이 필요할 때만)
sudo usermod -aG sudo student01

# Docker 수업이라면 docker 그룹에 추가 (sudo 없이 docker 명령 사용)
sudo usermod -aG docker student01

# 다른 수강생의 홈 디렉터리를 볼 수 없게 막기
sudo chmod 750 /home/student01
```

> ⚠️ `docker` 그룹은 사실상 root 권한과 같습니다. 이 점을 알고 부여하세요.

---

## 4. 여러 명을 한 번에 만들기

### 방법 A: 반복문 (student01 ~ student20, 초기 비밀번호는 모두 같게)

```bash
sudo groupadd students   # 그룹이 없다면 먼저 생성

for i in $(seq -w 1 20); do
  u="student$i"
  sudo useradd -m -s /bin/bash -G students "$u"
  echo "$u:Init1234!" | sudo chpasswd
  sudo chage -d 0 "$u"           # 첫 로그인 때 비밀번호 변경 강제
  sudo chmod 750 "/home/$u"
done
```

### 방법 B: 파일 목록으로 만들기

`users.txt` 파일을 `아이디:비밀번호` 형식으로 작성합니다.

```
kim:Pass1234!
lee:Pass1234!
park:Pass1234!
```

```bash
while IFS=: read -r u p; do
  sudo useradd -m -s /bin/bash "$u"
  echo "$u:$p" | sudo chpasswd
  sudo chage -d 0 "$u"
done < users.txt
```

---

## 5. 확인과 관리 명령어

| 명령어 | 설명 |
|---|---|
| `getent passwd \| grep student` | 생성된 계정 목록 |
| `id student01` | UID와 소속 그룹 확인 |
| `groups student01` | 소속 그룹 확인 |
| `who` | 현재 접속 중인 사용자 |
| `last` | 로그인 기록 |
| `sudo passwd student01` | 비밀번호 재설정 |
| `sudo usermod -L student01` | 계정 잠금 |
| `sudo usermod -U student01` | 잠금 해제 |
| `sudo deluser --remove-home student01` | 계정 삭제 (홈 디렉터리 포함) |

---

## 6. VirtualBox 네트워크 설정 (중요)

기본값인 NAT 모드에서는 외부에서 VM으로 접속할 수 없습니다. 둘 중 하나를 설정하세요.

| 방식 | 설정 위치 | 수강생 접속 방법 |
|---|---|---|
| **브리지 어댑터** (권장) | VM 설정 → 네트워크 → 다음에 연결됨: *어댑터에 브리지* | `ssh student01@<VM의 IP>` |
| **NAT + 포트 포워딩** | 네트워크 → 고급 → 포트 포워딩: 호스트 포트 `2222` → 게스트 포트 `22` | `ssh -p 2222 student01@<호스트 PC의 IP>` |

포트 포워딩을 쓰면 Windows 방화벽에서 호스트 PC의 2222 포트도 열어야 합니다.

---

## 7. 수강생 접속 테스트

수강생은 Windows PowerShell에서 이렇게 접속합니다.

```powershell
ssh student01@192.168.0.50
```

SSH 비밀번호 로그인이 막혀 있다면 `/etc/ssh/sshd_config` 파일(또는 `/etc/ssh/sshd_config.d/` 아래 파일)에서 `PasswordAuthentication yes`로 바꾼 뒤 SSH를 재시작합니다.

```bash
sudo systemctl restart ssh
```
