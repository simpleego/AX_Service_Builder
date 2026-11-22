# Windows PowerShell에서 VirtualBox Ubuntu로 접속하기

SSH로 접속합니다. **같은 PC에서 접속하는 경우**에는 VirtualBox 네트워크 설정에 따라 방법이 달라집니다.

---

## 1단계: Ubuntu에서 SSH 서버 확인

VirtualBox 화면 안의 Ubuntu 터미널에서 실행합니다.

```bash
sudo apt install -y openssh-server   # 설치 안 했다면
sudo systemctl status ssh            # active (running) 확인
whoami                               # 접속할 계정 이름 확인
ip a                                 # IP 주소 확인
```

---

## 2단계: VirtualBox 네트워크 방식 확인

VM 설정 → **네트워크** → "다음에 연결됨" 항목을 보고, 아래 경우 중 하나를 따라 하세요.

### 경우 ① NAT (기본값) → 포트 포워딩이 필요합니다

1. VM 설정 → 네트워크 → **고급** → **포트 포워딩** → `+` 버튼
2. 다음과 같이 입력합니다.

   | 이름 | 프로토콜 | 호스트 IP | 호스트 포트 | 게스트 IP | 게스트 포트 |
   |---|---|---|---|---|---|
   | ssh | TCP | (비움) | 2222 | (비움) | 22 |

3. PowerShell에서 접속합니다. 같은 PC이므로 주소는 `127.0.0.1`입니다.

```powershell
ssh -p 2222 계정이름@127.0.0.1
```

### 경우 ② 어댑터에 브리지 → Ubuntu IP로 바로 접속

`ip a`에서 확인한 IP(예: `192.168.0.50`)로 접속합니다. 수강생도 같은 방식으로 들어올 수 있습니다.

```powershell
ssh 계정이름@192.168.0.50
```

### 경우 ③ 호스트 전용 어댑터 → 이 PC에서만 접속 가능

보통 `192.168.56.x` 대역의 IP가 잡힙니다.

```powershell
ssh 계정이름@192.168.56.101
```

> 💡 **수업용으로 추천:** 수강생이 각자 자기 PC에서 접속해야 하면 **브리지**를 쓰세요. NAT로 운영하려면 수강생은 `127.0.0.1` 대신 **강사 PC의 IP**와 포트 2222로 접속해야 하고, Windows 방화벽에서 2222 포트를 열어 줘야 합니다.

---

## 3단계: 처음 접속할 때 나오는 화면

```
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

→ `yes`를 입력하고 Ubuntu 계정의 비밀번호를 입력합니다. 비밀번호는 입력해도 화면에 표시되지 않는 것이 정상입니다.

접속을 끝낼 때는 `exit`를 입력합니다.

---

## 문제가 생기면

| 증상 | 원인 / 해결 |
|---|---|
| `ssh : 'ssh' 용어가 ... 인식되지 않습니다` | Windows 설정 → 시스템 → 선택적 기능 → **OpenSSH 클라이언트** 설치 |
| `Connection refused` | Ubuntu에서 SSH 서버가 꺼져 있음 → `sudo systemctl start ssh`. NAT라면 포트 포워딩 설정 확인 |
| `Connection timed out` | IP가 틀렸거나 네트워크 방식이 맞지 않음. `ip a`로 다시 확인 |
| `Permission denied` | 계정 이름이나 비밀번호 오류, 또는 SSH 비밀번호 로그인이 막혀 있음 (`PasswordAuthentication yes` 설정) |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | VM을 다시 설치해서 서버 키가 바뀐 경우. 아래 명령으로 예전 키를 지운 뒤 다시 접속 |

예전 키를 지우는 명령입니다. NAT 포트 포워딩이라면 다음과 같이 실행합니다.

```powershell
ssh-keygen -R "[127.0.0.1]:2222"
```

브리지라면 해당 IP를 지정합니다.

```powershell
ssh-keygen -R 192.168.0.50
```

---

접속되면 `create_users.sh` 같은 스크립트도 이 PowerShell 창 안에서 바로 실행할 수 있습니다.
