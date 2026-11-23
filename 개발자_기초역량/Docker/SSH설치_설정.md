같은 PC에서 접속하는 경우는 **우분투에 SSH 서버 설치 → VirtualBox 포트포워딩 → Windows에서 접속** 세 단계면 됩니다. Windows에는 SSH 클라이언트가 기본으로 들어 있어서 따로 설치할 프로그램이 없습니다.

## 1단계. 우분투 VM 콘솔에서 할 일
이 단계는 붙여넣기가 안 되니 직접 타이핑해야 합니다. 지금 root로 로그인되어 있으므로 `sudo`는 필요 없습니다.

**① SSH 서버 설치**
```bash
apt update
apt install -y openssh-server
```

**② 실행 확인**
```bash
systemctl enable --now ssh
systemctl status ssh
```
`active (running)`이 보이면 정상이고, `q`를 누르면 빠져나옵니다.

**③ 접속할 계정의 비밀번호 정하기**
root로는 SSH 비밀번호 접속이 기본으로 막혀 있으니 일반 계정을 씁니다.
```bash
passwd vboxuser
```
입력하는 동안 화면에 아무것도 표시되지 않는 것이 정상입니다. 두 번 입력하면 됩니다.

## 2단계. VirtualBox 포트포워딩 설정
관리자 창에서 설정합니다.
1. `ubuntu24`를 선택하고 **설정(S) → 네트워크 → 어댑터 1**로 갑니다.
2. Attached to가 **NAT**인지 확인합니다.
3. **포트 포워딩**을 누르고 오른쪽 **+** 로 규칙을 추가합니다.

   | 이름 | 프로토콜 | 호스트 IP | 호스트 포트 | 게스트 IP | 게스트 포트 |
   |---|---|---|---|---|---|
   | ssh | TCP | 127.0.0.1 | 2222 | (비움) | 22 |
   | mysql | TCP | 127.0.0.1 | 3306 | (비움) | 3306 |

4. **확인 → 확인**을 누릅니다. VM이 켜져 있어도 바로 적용됩니다.

mysql 규칙은 나중에 Windows에서 MySQL Workbench 같은 도구로 DB에 접속할 때 필요합니다.

## 3단계. Windows에서 접속
**① SSH 클라이언트 확인**
PowerShell을 열고 입력합니다.
```powershell
ssh -V
```
`OpenSSH_for_Windows_...`처럼 버전이 나오면 준비가 끝난 것입니다.

**② 접속**
```powershell
ssh -p 2222 vboxuser@127.0.0.1
```
- 처음 접속하면 `Are you sure you want to continue connecting (yes/no)?`라고 묻습니다. `yes`를 입력하세요.
- 1단계에서 정한 비밀번호를 입력하면 `vboxuser@ubuntu24:~$` 프롬프트가 나옵니다.

**③ 붙여넣기**
이제 이 PowerShell 창에서는 **마우스 오른쪽 클릭**이나 `Ctrl+V`로 붙여넣을 수 있습니다. 관리자 권한이 필요하면 `sudo -i`로 root가 되면 됩니다. vboxuser가 sudo 그룹에 있어야 합니다(아래 문제 해결 참고).

## 4단계. MySQL 실행
접속한 창에서 이어서 진행합니다.
```bash
nano mysql-lab.sh
```
스크립트 내용을 붙여넣고 `Ctrl+O` → `Enter` → `Ctrl+X`로 저장한 뒤 실행합니다.
```bash
chmod +x mysql-lab.sh
./mysql-lab.sh
```

## 잘 안 될 때

| 증상 | 원인과 해결 |
|---|---|
| `Connection refused` | 우분투의 SSH 서버가 꺼져 있습니다. VM 콘솔에서 `systemctl status ssh`를 확인하세요. |
| `Connection timed out` | 포트포워딩 규칙이 없거나 어댑터가 NAT가 아닙니다. 2단계를 다시 확인하세요. |
| `Permission denied` | 비밀번호가 틀렸거나 root로 접속하려 한 경우입니다. `vboxuser`로 접속하세요. |
| `REMOTE HOST IDENTIFICATION HAS CHANGED` | VM을 새로 만들었을 때 나옵니다. `ssh-keygen -R "[127.0.0.1]:2222"`를 실행한 뒤 다시 접속하세요. |
| `sudo` 실행 시 권한 없음 | VM 콘솔(root)에서 `usermod -aG sudo vboxuser`를 실행하고 다시 접속하세요. |

## 매번 접속하기 편하게 하려면 (선택)
Windows의 `C:\Users\201-3\.ssh\config` 파일에 아래 내용을 저장해 두면, 다음부터는 `ssh ubuntu`만 입력해도 접속됩니다.
```
Host ubuntu
    HostName 127.0.0.1
    Port 2222
    User vboxuser
```
