# Ubuntu SSH 설치부터 실무 활용까지

> **대상**: Ubuntu를 처음 설치한 입문 개발자  
> **실습 환경**: Ubuntu 22.04 / 24.04 / 26.04 LTS, Windows 10/11 PowerShell(또는 Linux/macOS 클라이언트)  
> **학습 목표**: SSH의 개념을 이해하고, 서버 설치·원격 접속·키 인증·보안 설정·파일 전송·개발 도구 연동까지 직접 수행한다.  
> **주의**: 아래 IP, 계정, 경로는 예시다. 실제 환경에 맞게 변경한다.

---

## 학습 순서

1. SSH 개념과 Client–Server 구조
2. 막 설치한 Ubuntu의 기초 점검
3. OpenSSH 서버 설치 및 실행 상태 확인
4. 네트워크 IP와 UFW 방화벽 설정
5. Windows/Linux/macOS에서 최초 원격 접속
6. 기본 원격 명령 실행 및 세션 관리
7. 공개키(SSH Key) 인증 설정
8. 안전한 SSH 서버 보안 설정
9. SCP/SFTP 파일 송수신
10. SSH config, 포트 포워딩, VS Code 활용
11. 자주 발생하는 오류와 점검 절차
12. 실습 과제 및 최종 체크리스트

---

## 1. SSH란 무엇인가?

**SSH(Secure Shell)**는 네트워크를 통해 다른 컴퓨터에 암호화된 채널로 접속해 명령을 실행하고 파일을 전송할 수 있게 하는 프로토콜이다. 과거의 Telnet과 달리 인증 및 세션 데이터가 암호화된다.

### 1.1 쉬운 비유

- **Ubuntu 서버**: 관리해야 하는 건물
- **SSH 서버(`sshd`)**: 건물의 출입을 관리하는 보안 담당자
- **SSH 클라이언트(`ssh`)**: 외부에서 출입을 요청하는 직원
- **IP 주소**: 건물 주소
- **포트 22**: 기본 출입구 번호
- **계정과 암호 또는 SSH 키**: 출입 자격을 확인하는 수단
- **암호화**: 이동 중 통신 내용이 노출되지 않도록 보호하는 장치

```text
[Windows 개발자 PC: SSH Client]          [Ubuntu 서버: SSH Server]
192.168.0.10                              192.168.0.100
       |                                         |
       |  TCP 연결 -> 서버의 포트 22              |
       |---------------------------------------->|
       |  서버 호스트 키 확인·키 교환·인증          |
       |<--------------------------------------->|
       |  암호화된 원격 명령 실행                  |
       |---------------------------------------->|
       |  실행 결과 반환                          |
       |<----------------------------------------|
```

> 실제 SSH 연결에서는 서버의 호스트 키 검증, 암호화 키 협상, 사용자 인증이 구분되어 진행된다. 서버에 등록하는 **사용자의 공개키**와 서버 자체를 식별하는 **호스트 키**는 서로 다른 것이다.

### 1.2 주요 프로그램

| 프로그램 | 역할 | 일반적으로 실행하는 컴퓨터 |
|---|---|---|
| `sshd` | SSH 연결 요청을 받는 서버 데몬 | Ubuntu 서버 |
| `ssh` | 서버에 원격 로그인 | Windows/Ubuntu 클라이언트 |
| `ssh-keygen` | 공개키·개인키 생성 | 클라이언트 |
| `ssh-copy-id` | 클라이언트 공개키를 서버에 등록 | Linux/macOS 등 |
| `scp` | SSH 기반 파일 복사 | 클라이언트 |
| `sftp` | SSH 기반 대화형 파일 전송 | 클라이언트 |

**핵심 구분**: 서버에 접속하는 컴퓨터에는 *SSH 클라이언트*, 접속을 받는 컴퓨터에는 *SSH 서버*가 필요하다. 최근 Windows에는 OpenSSH 클라이언트가 포함된 경우가 많다.

---

## 2. Ubuntu 설치 직후 기초 점검

**이 장의 명령은 모두 Ubuntu 컴퓨터의 터미널에서 실행한다.** Ubuntu Desktop은 `Ctrl+Alt+T`로 터미널을 열 수 있다. Ubuntu Server는 로그인 후 셸 프롬프트에서 실행한다.

### 2.1 Ubuntu 버전 확인

```bash
cat /etc/os-release
```

출력 예시:

```text
NAME="Ubuntu"
VERSION="24.04.3 LTS (Noble Numbat)"
ID=ubuntu
```

버전에 따라 출력은 다르다.

### 2.2 현재 로그인 계정 확인

```bash
whoami
id
```

예시로 계정명이 `ubuntuuser`라면 이후 `ssh ubuntuuser@서버IP` 형식으로 접속한다. **`ubuntuuser`라는 계정이 자동으로 만들어지는 것은 아니다.** 설치 당시 만든 계정명을 사용한다.

### 2.3 시스템 패키지 목록 최신화

```bash
sudo apt update
sudo apt upgrade -y
```

- `sudo`: 관리자 권한으로 실행한다.
- `apt`: Ubuntu/Debian 계열의 패키지 관리자다.
- `update`: 저장소의 최신 패키지 목록을 갱신한다. 설치된 패키지를 업그레이드하지는 않는다.
- `upgrade`: 설치된 패키지의 업데이트를 적용한다.
- `-y`: 패키지 관리자 질문에 자동으로 동의한다(학습 환경에서만 의미를 이해하고 사용).

업데이트 후 재부팅이 필요하다는 메시지가 있으면 콘솔에 접근할 수 있는 상황에서 적절한 시점에 재부팅한다. 원격 작업 중 무작정 재부팅하지 않는다.

---

## 3. OpenSSH 서버 설치

### 3.1 패키지 설치

**실행 위치: Ubuntu 서버**

```bash
sudo apt install -y openssh-server
```

Ubuntu 설치 과정에서 이미 OpenSSH Server를 선택했다면 설치되어 있을 수 있다. 다시 실행해도 패키지 관리자가 현재 상태를 확인한다.

설치 확인:

```bash
apt list --installed openssh-server
```

### 3.2 SSH 서버 실행 및 자동 시작

```bash
sudo systemctl enable --now ssh
sudo systemctl status ssh
```

- `systemctl`: systemd의 서비스 관리 명령어다.
- `enable`: 일반적인 서비스 구성에서 부팅 시 자동 시작하도록 설정한다.
- `--now`: 활성화와 함께 지금도 시작하도록 요청한다.
- `status`: 실행 상태를 확인한다.

전형적인 출력 예시:

```text
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (...; enabled; ...)
     Active: active (running) since ...
```

**버전 주의**: 최신 Ubuntu에는 `ssh.socket`을 활용한 *socket activation*이 적용될 수 있다. 따라서 `ssh.service`가 항상 `active (running)`으로 표시되지 않아도 실제 SSH 연결을 받을 수 있다. 함께 확인한다.

```bash
systemctl status ssh.socket
sudo ss -tlnp | grep ':22'
```

`ss`는 열려 있는 소켓을 확인한다. 설치·구성에 따라 `sshd` 또는 `systemd`가 22번 포트에서 대기 중으로 보일 수 있다.

### 3.3 관리 명령 모음

```bash
sudo systemctl start ssh      # 시작
sudo systemctl stop ssh       # 중지: 원격 접속 중에는 주의!
sudo systemctl restart ssh    # 재시작: 설정 오류가 있으면 접속 위험
sudo systemctl reload ssh     # 가능한 경우 설정 다시 읽기
sudo systemctl status ssh     # 상태 확인
journalctl -u ssh -n 50 --no-pager  # SSH 서비스 관련 최근 로그
```

> `ssh.socket` 기반 구성에서는 동작 방식이 다를 수 있으므로 서비스 상태뿐 아니라 실제 리스닝 포트와 연결 테스트를 함께 확인한다. 접속된 원격 세션에서 무턱대고 `stop`이나 `restart`를 실행하지 않는다.

---

## 4. 네트워크 주소와 방화벽

### 4.1 서버 IP 주소 확인

**Ubuntu 서버에서**:

```bash
hostname -I
ip -br addr
```

예시:

```text
192.168.0.100
```

여러 IP가 표시될 수 있다. Windows와 같은 사설망에 있는 Ubuntu의 **해당 네트워크 인터페이스 IPv4 주소**를 선택한다.

- `127.0.0.1`: 같은 컴퓨터 내부에서 사용하는 루프백 주소. 원격 Windows에서는 이 IP로 Ubuntu에 접속할 수 없다.
- `192.168.x.x`, `10.x.x.x`, `172.16.x.x`~`172.31.x.x`: 일반적인 사설 IP 대역.
- 공인 IP: 외부 인터넷 접속에 사용할 수 있으나 라우터·방화벽·클라우드 정책이 별도로 영향을 준다.

### 4.2 방화벽 UFW 점검

```bash
sudo ufw status verbose
```

`Status: inactive`이면 UFW는 비활성 상태다. UFW를 활성화하려면 **반드시 먼저 SSH를 허용**한다.

```bash
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status numbered
```

`OpenSSH`는 일반적으로 포트 `22/tcp`에 해당하는 UFW 애플리케이션 프로필이다. 동일한 기본 포트를 허용하려면 `sudo ufw allow 22/tcp`도 사용할 수 있다. 불필요하게 두 규칙을 중복 생성할 필요는 없다.

> **원격 서버 경고**: UFW를 활성화하기 전에 SSH 허용 규칙을 반드시 추가하고, 클라우드 환경이라면 공급자의 별도 보안 그룹/네트워크 방화벽도 점검한다. 기존 원격 세션을 유지하고 새 창에서 접속을 검증하라.

### 4.3 연결 가능한 네트워크 형태

| 상황 | 필요한 조건 |
|---|---|
| 같은 공유기 LAN의 Windows ↔ Ubuntu | 서버의 LAN IP, SSH 서버 작동, 방화벽 허용 |
| Ubuntu가 VirtualBox/VMware NAT 가상머신 | 일반적으로 호스트에서 VM으로 접속하려면 포트 포워딩 또는 브리지 구성 필요 |
| 가상머신 브리지 네트워크 | 같은 LAN에서 별도 IP를 받으면 그 IP로 접속 가능(네트워크 정책에 따라 달라짐) |
| 외부 인터넷에서 집/사무실 Ubuntu 접속 | 공인 접근 경로, 라우터/방화벽 정책 등 추가 설정 필요. 우선 VPN·Tailscale 등 안전한 접근 방식을 고려 |
| 클라우드 Ubuntu | 공인/사설 IP, 보안 그룹, SSH 키, 네트워크 ACL 등의 설정 확인 |

**초보자 실습은 반드시 같은 LAN부터 시작하자.** 외부에 SSH 포트를 노출할 필요가 없다.

---

## 5. Windows에서 Ubuntu로 최초 접속

### 5.1 Windows OpenSSH 클라이언트 확인

**실행 위치: Windows PowerShell**

```powershell
ssh -V
```

버전 문자열이 출력되면 SSH 클라이언트가 설치되어 있다. 명령을 찾지 못한다면 Windows의 *설정 → 선택적 기능*에서 OpenSSH 클라이언트를 추가하거나 Windows 관리 정책에 맞게 설치한다.

### 5.2 첫 SSH 접속

**Windows PowerShell**:

```powershell
ssh ubuntuuser@192.168.0.100
```

- `ssh`: 연결을 시작한다.
- `ubuntuuser`: Ubuntu에 존재하는 실제 로그인 계정이다.
- `@`: 계정과 호스트를 구분한다.
- `192.168.0.100`: Ubuntu 서버 IP다.

최초 접속 시 다음과 유사한 메시지가 나타날 수 있다.

```text
The authenticity of host '192.168.0.100 (...)' can't be established.
ED25519 key fingerprint is SHA256:...
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

**무조건 `yes`를 입력하지 않는다.** 서버 콘솔에서 아래 명령으로 호스트 키 지문을 별도 확인하고 비교한다.

```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

일치하고 서버가 신뢰할 수 있다면 `yes`를 입력한다. 클라이언트가 서버의 호스트 키를 `~/.ssh/known_hosts`에 기록한다. 이후 Ubuntu 계정 비밀번호를 요구할 수 있다. 입력 중 화면에 글자나 별표가 나오지 않는 것은 정상이다.

로그인 성공 후 확인:

```bash
whoami
hostname
pwd
```

예를 들어 `whoami`가 `ubuntuuser`, `hostname`이 Ubuntu 서버의 이름을 출력하면 원격 명령이 실행되고 있는 것이다.

### 5.3 연결 해제

```bash
exit
```

또는 `Ctrl+D`로 원격 셸을 종료한다. 그러면 Windows PowerShell 프롬프트로 복귀한다.

### 5.4 Linux/macOS에서 접속

터미널에서 같은 형식의 명령어를 사용한다.

```bash
ssh ubuntuuser@192.168.0.100
```

### 5.5 SSH 포트를 별도로 지정할 경우

기본 22번이 아니라 2222번을 사용하도록 서버를 설정한 **경우에만**:

```powershell
ssh -p 2222 ubuntuuser@192.168.0.100
```

초기 실습에서는 기본 포트 22를 유지한다. 포트 변경은 자동으로 강력한 보안을 제공하지 않으며, 최신 Ubuntu의 소켓 활성화 구성에서는 포트 변경 시 소켓 설정까지 검토해야 한다.

---

## 6. SSH로 원격 작업하기

### 6.1 접속 후 기본 명령

```bash
pwd                       # 현재 경로
ls -al                    # 파일 목록
mkdir -p ~/ssh-lab         # 실습 폴더 생성
cd ~/ssh-lab               # 해당 폴더로 이동
echo 'SSH 연결 성공' > hello.txt
cat hello.txt
uname -a                  # 시스템 정보
```

### 6.2 로그인하지 않고 단일 명령만 실행

**Windows PowerShell**:

```powershell
ssh ubuntuuser@192.168.0.100 "hostname"
ssh ubuntuuser@192.168.0.100 "uptime"
ssh ubuntuuser@192.168.0.100 "ls -al ~/ssh-lab"
```

클라이언트에서 명령을 보내고 Ubuntu에서 실행한 결과만 받아올 수 있다. 따옴표 안의 명령은 **원격 서버의 셸**에서 실행된다.

### 6.3 접속 기록 및 사용자 확인

**Ubuntu 서버**:

```bash
who
w
last -n 5
```

- `who`: 현재 로그인 사용자
- `w`: 사용자와 작업 상태
- `last`: 최근 로그인 기록(시스템 설정에 따라 기록 범위가 달라짐)

### 6.4 장시간 실행 작업 주의

SSH 터미널을 닫으면 셸에 종속된 작업이 종료될 수 있다. 장시간 작업에는 `tmux`, `screen`, `systemd` 서비스를 고려한다. 웹 서버를 단순히 `python app.py`로 SSH 세션에서 실행하는 방식은 실제 운영 서비스에 적합하지 않다.

---

## 7. SSH 키(공개키) 인증

### 7.1 비밀번호와 키 인증 비교

| 구분 | 비밀번호 인증 | SSH 키 인증 |
|---|---|---|
| 로그인 근거 | 계정 비밀번호 | 개인키 보유를 암호학적으로 증명 |
| 사용자 준비 | 비밀번호 기억 | 개인키 보관, 선택적으로 암호문구(passphrase) 사용 |
| 자동화 활용 | 비밀번호 입력 처리 필요 | 키 관리 정책에 따라 자동화에 적합 |
| 보안 주의 | 추측·유출·재사용 위험 | 개인키 유출, 키 권한, 폐기/교체 관리 필요 |

**비유**: 서버에 공개키로 확인할 수 있는 '자물쇠 검사 규칙'을 등록해 두고, 클라이언트는 외부로 보내지 않는 개인키로 자신이 적법한 소유자임을 증명한다. 실제로 개인키 파일을 서버에 전달하는 방식은 아니다.

```text
[Windows PC]                              [Ubuntu 서버]
~/.ssh/id_ed25519    (개인키: 비공개)       ~/.ssh/authorized_keys
~/.ssh/id_ed25519.pub(공개키) ------------> 등록된 공개키
       |
       | SSH 인증 시 개인키로 서명
       +----------------------------------> 서버가 공개키로 검증
       |<---------------------------------- 인증 성공 후 세션 개설

개인키 파일은 서버로 복사하지 않는다!
```

### 7.2 Windows에서 키 생성

**Windows PowerShell**:

```powershell
ssh-keygen -t ed25519 -C "my-windows-pc"
```

- `-t ed25519`: ED25519 알고리즘 사용
- `-C`: 키를 구분하기 위한 설명(comment). 이메일이 반드시 필요한 것은 아님.

파일 경로를 묻는다면 기본값을 사용해도 된다. 단, **이미 같은 경로에 키가 있다면 덮어쓰지 않는다.** 별도 파일명을 선택한다. 개인키 암호문구(passphrase)는 가능한 한 설정한다.

기본 경로 예시:

```text
C:\Users\사용자명\.ssh\id_ed25519        <- 개인키: 외부 공유 금지
C:\Users\사용자명\.ssh\id_ed25519.pub    <- 공개키: 서버 등록 가능
```

공개키 확인:

```powershell
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

### 7.3 공개키를 서버에 등록: Windows 수동 방식

Windows 기본 OpenSSH에는 `ssh-copy-id`가 보통 제공되지 않는다. 다음과 같이 **공개키 한 줄만** Ubuntu 사용자에게 등록한다.

1. Windows PowerShell에서 `Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub`로 `ssh-ed25519 AAAA...` 형식의 **공개키 한 줄 전체**를 복사한다.
2. 비밀번호 인증으로 Ubuntu에 SSH 로그인한다.
3. Ubuntu에서 다음 명령으로 `.ssh` 폴더를 만든다.

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
```

4. 편집기에 복사한 **공개키 한 줄**을 붙여 넣고 저장한다. 기존 내용이 있다면 **지우지 않고 새 줄에 추가**한다. nano 저장: `Ctrl+O` → Enter, 종료: `Ctrl+X`.
5. 권한을 설정한다.

```bash
chmod 600 ~/.ssh/authorized_keys
```

권한 의미: 디렉터리 `700`은 소유자만 접근 가능, 파일 `600`은 소유자만 읽기/쓰기 가능이다. `authorized_keys`는 서버에서 **로그인할 계정의 홈 디렉터리** 아래에 있어야 한다.

### 7.4 Linux/macOS 클라이언트라면

```bash
ssh-keygen -t ed25519 -C "my-linux-laptop"
ssh-copy-id -i ~/.ssh/id_ed25519.pub ubuntuuser@192.168.0.100
```

`ssh-copy-id`는 클라이언트에 설치되어 있어야 하며, 초기에는 서버의 비밀번호 로그인 등이 가능해야 한다.

### 7.5 키 인증 테스트

**Windows PowerShell(새 창)**:

```powershell
ssh -i "$env:USERPROFILE\.ssh\id_ed25519" ubuntuuser@192.168.0.100
```

- `-i`: 인증에 사용할 **클라이언트 개인키 파일** 지정
- 개인키에 passphrase를 설정했다면 로그인 시 해당 암호문구를 요구할 수 있다.

진단이 필요하면:

```powershell
ssh -v ubuntuuser@192.168.0.100
```

`-v`는 연결과 인증 상세 로그를 보여 준다. 로그에는 민감한 환경 정보가 포함될 수 있으므로 공개 공유에 주의한다.

> **다음 보안 단계로 넘어가기 전**: 클라이언트 새 창에서 키 인증으로 재로그인되는 것을 반드시 확인한다. 원격 세션을 유지한 상태로 테스트하면 문제 발생 시 복구가 쉽다.

---

## 8. SSH 보안 강화

### 8.1 계정 보호 원칙

- 운영 환경에서는 일반 사용자 계정으로 로그인하고 관리자 작업에만 `sudo`를 사용한다.
- SSH 개인키를 Git 저장소, 메신저, 공유 폴더 등에 업로드하지 않는다.
- 키 인증을 먼저 검증한 뒤 비밀번호 로그인을 비활성화한다.
- 실제 서버를 공용 인터넷에 노출하기 전에 접근 가능한 IP/VPN·방화벽 정책을 검토한다.
- SSH와 운영체제 보안 업데이트를 정기적으로 적용한다.

### 8.2 안전한 설정 변경 절차

Ubuntu의 `/etc/ssh/sshd_config`와 `/etc/ssh/sshd_config.d/*.conf` 파일에서 SSH 서버 설정을 관리한다. 단, OpenSSH는 **동일한 키워드가 여러 번 나타나면 먼저 읽힌 값을 사용하는 경우**가 있으므로 설정 파일의 로딩 순서를 알아야 한다. 또한 `Match` 블록에 따라 사용자/접속 조건별 값이 달라질 수 있다.

먼저 현재 적용된 값을 확인한다.

```bash
sudo sshd -T | grep -E '^(passwordauthentication|permitrootlogin|pubkeyauthentication) '
```

서버 구성의 포함 순서와 설정 파일을 확인한다.

```bash
grep -n '^Include' /etc/ssh/sshd_config
sudo grep -RniE '^[[:space:]]*(PasswordAuthentication|PermitRootLogin|PubkeyAuthentication)' \
  /etc/ssh/sshd_config /etc/ssh/sshd_config.d/ 2>/dev/null
```

예시로 **기존 관련 설정과 우선순위 충돌이 없음을 확인한 후**, 별도 파일을 만들어 관리할 수 있다.

```bash
sudo nano /etc/ssh/sshd_config.d/01-lab-hardening.conf
```

파일 내용:

```sshconfig
PubkeyAuthentication yes
PasswordAuthentication no
PermitRootLogin no
```

**중요**: 이 설정은 키 인증을 미리 성공적으로 마친 뒤에만 적용한다. `PasswordAuthentication no`만으로 모든 형태의 대화형 암호 인증이 무조건 차단된다고 단정할 수 없으므로, 필요하면 `KbdInteractiveAuthentication` 등 적용값과 PAM 설정도 검토한다. 클라우드 이미지에서는 `50-cloud-init.conf` 등에서 이미 값이 정의되어 있을 수 있다. 해당 파일을 무작정 삭제하지 말고 **설정 병합 순서와 최종 적용값**을 확인한다.

### 8.3 문법 검증 → 적용 → 확인

```bash
sudo sshd -t
```

오류 메시지가 없으면 일반적으로 문법 검사를 통과한 것이다. 가능하면 콘솔 접근 수단과 기존 SSH 세션을 확보한다.

```bash
sudo systemctl reload ssh
sudo sshd -T | grep -E '^(passwordauthentication|permitrootlogin|pubkeyauthentication) '
```

Ubuntu의 SSH 서비스 관리 방식에 따라 reload/소켓 활성화 동작이 다를 수 있다. 새 PowerShell 창에서 **키 인증으로 실제 로그인**되는지 시험한다. 로그인할 수 없다면 기존 세션/서버 콘솔로 되돌아가 설정을 복구한다.

> `sshd -T`는 일반적인 유효 설정을 보여 주지만 실제 접속자별 `Match` 규칙이 적용되면 달라질 수 있다. 그 경우 `sshd -T -C user=...,host=...,addr=...` 형식으로 조건을 넣어 확인한다.

### 8.4 포트 변경에 관한 오해

기본 포트 22를 다른 포트로 바꾸면 단순 스캔 노출이 일부 달라질 수 있지만, **키 인증·접근 제한·패치 관리의 대체 수단이 아니다.** 특히 최신 Ubuntu에서 `ssh.socket`이 리스닝 포트를 관리할 수 있으므로 `Port 2222` 한 줄만 바꾸는 것은 충분하지 않을 수 있다. 초급 실습은 22번을 유지한다.

---

## 9. 파일 전송: SCP와 SFTP

### 9.1 SCP: Windows → Ubuntu

**Windows PowerShell**에서 `C:\Users\Public\Documents\report.txt`라는 파일이 실제 존재한다고 가정한다.

```powershell
scp C:\Users\Public\Documents\report.txt ubuntuuser@192.168.0.100:/home/ubuntuuser/
```

원격 파일 경로는 `계정@호스트:/경로`로 구분한다. `scp`가 로컬 Windows 경로를 해석하기 어려운 특수한 상황에서는 따옴표를 적용하고 실제 경로를 점검한다.

### 9.2 SCP: Ubuntu → Windows

**Windows PowerShell**:

```powershell
scp ubuntuuser@192.168.0.100:/home/ubuntuuser/hello.txt "$env:USERPROFILE\Downloads\"
```

서버 `hello.txt`를 Windows의 Downloads 폴더로 다운로드한다. 먼저 원격에 파일이 존재하는지 확인한다.

### 9.3 폴더 전체 복사

**Windows PowerShell**:

```powershell
scp -r ubuntuuser@192.168.0.100:/home/ubuntuuser/ssh-lab "$env:USERPROFILE\Downloads\"
```

`-r`는 하위 폴더를 재귀적으로 복사한다.

> 최신 OpenSSH의 `scp`는 기본적으로 SFTP 프로토콜을 사용한다. 이름이 SCP라고 해서 내부 구현이 항상 과거의 SCP 프로토콜인 것은 아니다.

### 9.4 SFTP: 대화형 파일 관리

**Windows PowerShell**:

```powershell
sftp ubuntuuser@192.168.0.100
```

SFTP 프롬프트에서:

```text
sftp> pwd                 # 원격 현재 폴더
sftp> lpwd                # 로컬 현재 폴더
sftp> ls                  # 원격 파일 목록
sftp> put report.txt      # 로컬 -> 원격 업로드
sftp> get hello.txt       # 원격 -> 로컬 다운로드
sftp> bye                 # 종료
```

`put report.txt`를 실행하기 전에 로컬 작업 디렉터리에 해당 파일이 있는지 확인한다. 필요하면 `lcd` 명령으로 로컬 디렉터리를 이동한다.

### 9.5 SSH와 파일 전송 비교

| 명령 | 목적 | 예시 |
|---|---|---|
| `ssh` | 원격 명령·로그인 | `ssh user@host` |
| `scp` | 파일·폴더 복사 | `scp file user@host:/tmp/` |
| `sftp` | 대화형 파일 관리 | `sftp user@host` |

---

## 10. SSH 설정 파일로 접속 단순화

긴 IP, 계정, 개인키 경로를 매번 적지 않고 클라이언트에 별칭을 등록할 수 있다.

**Windows에서** `$env:USERPROFILE\.ssh\config` 파일을 편집한다(확장자 `.txt`가 붙지 않도록 주의).

```sshconfig
Host ubuntu-lab
    HostName 192.168.0.100
    User ubuntuuser
    Port 22
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

각 항목 의미:

- `Host`: 사용자가 정의한 접속 별칭
- `HostName`: 서버 IP 또는 도메인
- `User`: 서버 로그인 계정
- `Port`: SSH 서버 포트
- `IdentityFile`: 클라이언트의 개인키 경로
- `IdentitiesOnly`: 지정한 인증 ID 사용을 우선하는 설정

이제 다음과 같이 접속할 수 있다.

```powershell
ssh ubuntu-lab
scp "$env:USERPROFILE\Downloads\test.txt" ubuntu-lab:/home/ubuntuuser/
```

설정 검사:

```powershell
ssh -G ubuntu-lab
```

이 명령은 클라이언트가 계산한 접속 설정을 보여 주며, 실제 SSH 연결을 시작하지 않는다.

---

## 11. 실무 활용: VS Code와 SSH 포트 포워딩

### 11.1 VS Code Remote - SSH

Windows의 VS Code에서 **Remote - SSH** 확장을 설치한 뒤:

1. `Ctrl+Shift+P` → `Remote-SSH: Connect to Host...` 실행
2. `ubuntu-lab` 선택(앞 장의 SSH config가 존재한다고 가정)
3. Ubuntu에서 열 프로젝트 폴더 선택
4. 원격 서버의 파일을 편집하고, 터미널에서 Ubuntu 명령 실행

**개념**: Windows에는 VS Code 화면이 있고 소스 편집·명령 실행의 상당 부분은 Ubuntu 서버 환경에서 수행된다. 확장 기능 설치 위치나 원격 구성은 확장에 따라 다를 수 있다.

### 11.2 SSH 로컬 포트 포워딩

예: Ubuntu 서버의 `127.0.0.1:8000`에서 FastAPI 서버가 동작하고 있고, Windows 브라우저에서 이를 확인하려는 경우다.

Ubuntu 서버(원격에서 먼저 실행):

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

실습의 편의를 위한 간단한 정적 HTTP 서버이며 FastAPI가 없어도 테스트할 수 있다. 별도 서버 터미널이나 `tmux`에서 유지한다.

Windows PowerShell(별도 창):

```powershell
ssh -N -L 8000:127.0.0.1:8000 ubuntuuser@192.168.0.100
```

Windows 브라우저에서 접속:

```text
http://127.0.0.1:8000
```

```text
Windows 브라우저 -> Windows localhost:8000
                           |
                    암호화 SSH 터널
                           |
                           v
                Ubuntu localhost:8000
```

- `-L 로컬포트:목적지호스트:목적지포트`: 로컬 포트 포워딩
- `-N`: 원격 명령 또는 셸을 실행하지 않고 포워딩 연결 유지
- `127.0.0.1`은 각 구간의 컴퓨터에서 해석된다. 여기서 `-L`의 목적지 `127.0.0.1`은 **Ubuntu SSH 서버 측** 루프백을 가리킨다.
- Windows의 로컬 포트 8000이 이미 사용 중이라면 `-L 18000:127.0.0.1:8000`으로 변경하고 브라우저에서는 `http://127.0.0.1:18000`을 연다.

터널을 종료하려면 PowerShell에서 `Ctrl+C`를 누른다.

### 11.3 Git과 SSH 구분

`ssh ubuntu-lab`은 **원격 서버에 로그인**하는 것이고, `git@github.com:...` 형식의 Git SSH URL은 **Git 호스팅 서비스와 키 인증을 통해 데이터를 주고받는 것**이다. 둘 다 SSH 기술을 사용하지만 서버, 계정, 공개키 등록 위치가 다르다.

---

## 12. 자주 발생하는 오류 해결

| 오류·증상 | 유력 원인 | 우선 점검 |
|---|---|---|
| `Connection refused` | 서버가 포트에서 수신하지 않음, 대상 IP/포트 오류, 일부 방화벽 거절 | 서버 `ss -tlnp`, `systemctl status ssh.socket ssh`, IP 확인 |
| `Connection timed out` | 네트워크 경로·방화벽·NAT 문제 | IP, LAN, UFW, 클라우드 보안 그룹 점검 |
| `Permission denied (publickey)` | 공개키 미등록, 잘못된 계정/키, 파일 권한 문제, 비밀번호 인증 제한 | `ssh -v`, `authorized_keys`, 계정 및 권한 확인 |
| `Permission denied, please try again` | 비밀번호 오류 또는 인증 정책 | Ubuntu 계정·키보드 입력·서버 인증 설정 확인 |
| `Host key verification failed` | 저장된 서버 식별 정보와 현재 서버 키 불일치 등 | 서버 호스트 키를 독립적으로 검증. 공격 가능성도 고려 |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` | 서버 재설치/키 교체 또는 중간자 공격 가능성 | 서버 지문을 안전하게 검증한 후에만 기존 기록 변경 |
| `ssh: command not found` | 클라이언트 미설치/경로 문제 | OpenSSH 클라이언트 설치 확인 |
| `sudo: ...` 관련 오류 | 계정에 sudo 권한이 없거나 인증 실패 | 올바른 관리자 계정 및 권한 확인 |

### 12.1 권장 진단 순서

1. **Ubuntu 콘솔**에서 IP 확인: `hostname -I`
2. **Ubuntu 콘솔**에서 서버 설치 및 상태 확인: `systemctl status ssh.socket ssh`
3. **Ubuntu 콘솔**에서 리스닝 포트 확인: `sudo ss -tlnp | grep ':22'`
4. **Ubuntu 콘솔**에서 UFW 확인: `sudo ufw status verbose`
5. **Windows PowerShell**에서 TCP 22 연결 점검:

```powershell
Test-NetConnection 192.168.0.100 -Port 22
```

6. **Windows PowerShell**에서 SSH 디버그 출력:

```powershell
ssh -vvv ubuntuuser@192.168.0.100
```

7. **Ubuntu 서버**의 SSH 로그 확인:

```bash
sudo journalctl -u ssh -n 100 --no-pager
```

`ping`은 ICMP 설정에 따라 차단될 수 있어 실패만으로 SSH 연결 불가를 확정할 수 없다. Windows `Test-NetConnection`은 TCP 포트 도달 가능성 점검에 도움이 된다.

### 12.2 호스트 키 경고를 해결할 때

서버를 재설치했다면 호스트 키가 바뀌어 경고가 날 수 있다. 하지만 공격일 가능성도 있으므로 서버 콘솔에서 호스트 키 지문을 **다른 신뢰할 수 있는 경로로 검증한 뒤** 클라이언트의 오래된 정보를 수정한다.

```powershell
ssh-keygen -R 192.168.0.100
```

그 후 다시 접속하여 지문을 검증한다. **확인 없이 경고를 무시하거나 호스트 키 검증을 끄지 않는다.**

---

## 13. 초보자를 위한 실습 시나리오

### 실습 A. 기본 SSH 접속 (약 20분)

1. Ubuntu 계정과 IP 확인
2. `openssh-server` 설치
3. `ssh.service`/`ssh.socket` 상태 확인
4. UFW에서 SSH 허용
5. Windows에서 `ssh 계정@IP`로 로그인
6. `whoami`, `hostname`, `pwd` 명령 실행
7. `exit`로 종료

**성공 기준**: Windows에서 Ubuntu의 실제 계정과 호스트명이 출력된다.

### 실습 B. SSH 키 인증 (약 25분)

1. Windows에서 `ssh-keygen -t ed25519` 실행
2. 개인키/공개키 파일 식별
3. 서버의 `authorized_keys`에 공개키 등록
4. Windows에서 키 로그인 성공 확인
5. `~/.ssh/config`에 `ubuntu-lab` 별칭 등록
6. `ssh ubuntu-lab` 접속 확인

**성공 기준**: 계정 비밀번호를 사용하지 않고 개인키 인증으로 접속한다. 키의 passphrase를 요구하는 것은 정상이다.

### 실습 C. 파일 전송 (약 15분)

1. Windows에서 텍스트 파일 하나 준비
2. `scp`로 Ubuntu에 업로드
3. Ubuntu에서 `cat`으로 내용 확인
4. `sftp`로 파일 다운로드
5. 양쪽 파일 내용 비교

**성공 기준**: Windows↔Ubuntu 양방향 파일 이동 성공.

### 실습 D. 웹 개발 환경 접속 (약 25분)

1. Ubuntu에서 `python3 -m http.server 8000 --bind 127.0.0.1` 실행
2. Windows에서 `ssh -N -L 8000:127.0.0.1:8000 ubuntu-lab` 실행
3. Windows에서 `http://127.0.0.1:8000` 열기
4. 터널 종료 후 차이를 관찰
5. VS Code Remote - SSH로 프로젝트 폴더 열기(선택)

**성공 기준**: Ubuntu의 로컬 웹 서버를 SSH 터널을 통해 Windows 브라우저에서 열 수 있다.

### 실습 E. 보안 설정 검증 (약 20분)

1. 현재 `sshd -T` 적용 설정 확인
2. SSH 키 로그인 성공 여부 재확인
3. 별도 설정 파일을 만들고 비밀번호 인증 제한
4. `sudo sshd -t` 문법 검사
5. 설정 반영 후 새 창에서 키 인증 로그인 확인
6. 문제 시 기존 세션으로 복원

**성공 기준**: 키 로그인은 가능하고 서버의 보안 정책이 의도대로 적용된다.

---

## 14. 최종 체크리스트

- [ ] Ubuntu 버전·계정·IP를 확인했다.
- [ ] OpenSSH 서버를 설치했다.
- [ ] SSH 서비스 또는 소켓 리스닝 상태를 확인했다.
- [ ] UFW에서 SSH 접근을 허용했다.
- [ ] Windows에서 최초 원격 접속에 성공했다.
- [ ] 서버의 호스트 키 지문을 검증했다.
- [ ] SSH 공개키와 개인키의 차이를 설명할 수 있다.
- [ ] 공개키를 서버 `authorized_keys`에 등록했다.
- [ ] 새 창에서 키 인증 로그인을 검증했다.
- [ ] 설정 변경 전 `sshd -t` 검사를 수행했다.
- [ ] `scp` 또는 `sftp`로 파일을 전송했다.
- [ ] SSH config로 접속 별칭을 사용했다.
- [ ] 필요 시 로컬 포트 포워딩을 사용할 수 있다.
- [ ] 오류 발생 시 서버·네트워크·인증 순으로 진단할 수 있다.

---

## 15. 명령어 치트시트

| 구분 | 명령어 | 실행 위치 |
|---|---|---|
| 설치 | `sudo apt install -y openssh-server` | Ubuntu 서버 |
| 시작/자동 시작 | `sudo systemctl enable --now ssh` | Ubuntu 서버 |
| 상태 | `systemctl status ssh.socket ssh` | Ubuntu 서버 |
| IP | `hostname -I` | Ubuntu 서버 |
| 리스닝 확인 | `sudo ss -tlnp \| grep ':22'` | Ubuntu 서버 |
| 방화벽 | `sudo ufw allow OpenSSH` | Ubuntu 서버 |
| 원격 접속 | `ssh ubuntuuser@192.168.0.100` | Windows 등 클라이언트 |
| 포트 지정 | `ssh -p 2222 ubuntuuser@192.168.0.100` | 클라이언트 |
| 키 생성 | `ssh-keygen -t ed25519` | 클라이언트 |
| 연결 디버그 | `ssh -vvv ubuntuuser@192.168.0.100` | 클라이언트 |
| 설정 검증 | `sudo sshd -t` | Ubuntu 서버 |
| 서버 설정 확인 | `sudo sshd -T` | Ubuntu 서버 |
| 파일 업로드 | `scp 파일 user@host:/경로/` | 클라이언트 |
| 파일 다운로드 | `scp user@host:/파일 로컬경로` | 클라이언트 |
| 대화형 파일 전송 | `sftp user@host` | 클라이언트 |
| 로컬 터널 | `ssh -N -L 8000:127.0.0.1:8000 user@host` | 클라이언트 |

---

## 16. 참고 자료

- [Ubuntu 공식 문서: OpenSSH server](https://ubuntu.com/server/docs/how-to/security/openssh-server/)
- [Ubuntu 공식 문서: OpenSSH](https://ubuntu.com/server/docs/openssh-server/)
- [Ubuntu Wiki: SSH/OpenSSH/Keys](https://wiki.ubuntu.com/SSH/OpenSSH/Keys)
- [Microsoft Learn: Key-Based Authentication in OpenSSH for Windows](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement)
- [Ubuntu Manual: SSH](https://manpages.ubuntu.com/manpages/jammy/man1/ssh.1.html)
- [Ubuntu Manual: SCP](https://manpages.ubuntu.com/manpages/jammy/man1/scp.1.html)

> 작성 기준: 2026-11-23. 실제 Ubuntu 버전과 운영 환경(Desktop/Server, VM/물리 서버, 클라우드, socket activation)에 따라 서비스 상태·설정 파일의 우선순위·네트워크 구성이 달라질 수 있다. 이 문서는 같은 LAN에서 SSH를 안전하게 시작하기 위한 입문 실습을 우선한다.
