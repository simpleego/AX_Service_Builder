학생들이 접속하려면 **포트포워딩이 모든 네트워크에서 받도록 바꾸고, Windows 방화벽에서 포트를 여는 것**이 핵심입니다. 지금은 호스트 IP를 `127.0.0.1`로 해 두어서 이 PC 자신만 접속할 수 있는 상태입니다.

## 1. 포트포워딩의 호스트 IP 비우기
관리자 창에서 `ubuntu24` → **설정 → 네트워크 → 포트 포워딩**으로 가서, 두 규칙의 **호스트 IP 칸을 비웁니다.** `0.0.0.0`을 입력해도 같습니다.

| 이름 | 프로토콜 | 호스트 IP | 호스트 포트 | 게스트 포트 |
|---|---|---|---|---|
| ssh | TCP | **(비움)** | 2222 | 22 |
| mysql | TCP | **(비움)** | 3306 | 3306 |

## 2. Windows 방화벽에서 포트 열기
**PowerShell을 관리자 권한으로 실행**한 뒤 입력합니다.
```powershell
New-NetFirewallRule -DisplayName "VBox SSH 2222" -Direction Inbound -Protocol TCP -LocalPort 2222 -Action Allow
```
```powershell
New-NetFirewallRule -DisplayName "VBox MySQL 3306" -Direction Inbound -Protocol TCP -LocalPort 3306 -Action Allow
```
- 네트워크 프로필이 **공용**이면 막힐 수 있습니다. **설정 → 네트워크 및 인터넷 → 연결된 네트워크 → 개인 네트워크**로 바꾸는 것이 좋습니다.
- 처음에 VirtualBox가 방화벽 허용 팝업을 띄웠다면 **허용**을 누르세요.

## 3. 이 PC의 내부 IP 확인
```powershell
ipconfig
```
사용 중인 어댑터의 **IPv4 주소**를 확인합니다. 예: `192.168.0.25`

## 4. 학생들의 접속 방법
학생들은 각자 PC의 PowerShell에서 접속합니다.
```powershell
ssh -p 2222 아이디@192.168.0.25
```
MySQL Workbench나 DBeaver로 DB에 접속할 때는 다음 정보를 쓰면 됩니다.
- 호스트: `192.168.0.25`
- 포트: `3306`
- 사용자: `labuser` / `Lab1234!`
- DB: `labdb`

## 5. 학생 계정 만들기
한 계정을 같이 쓰게 하는 것보다 학생마다 계정을 주는 것이 안전합니다. 우분투에서 한꺼번에 만들 수 있습니다.
```bash
for i in $(seq -w 1 20); do
  sudo useradd -m -s /bin/bash student$i
  echo "student$i:Pass${i}!" | sudo chpasswd
  sudo chage -d 0 student$i   # 첫 로그인 시 비밀번호 변경 강제
done
```
이렇게 하면 `student01`부터 `student20`까지 계정이 만들어지고, 초기 비밀번호는 `Pass01!` 같은 형식입니다.
- 학생들도 Docker를 써야 한다면 `sudo usermod -aG docker student01`처럼 docker 그룹에 추가합니다. 단, docker 그룹 사용자는 사실상 root 권한을 갖게 되니 주의하세요.
- **sudo 그룹에는 넣지 않는 것을 권장합니다.**

## 6. 접속 테스트
- 이 PC에서 내부 IP로 접속해 봅니다.
  ```powershell
  ssh -p 2222 vboxuser@192.168.0.25
  ```
- 학생 PC에서 포트가 열려 있는지 확인합니다. `TcpTestSucceeded : True`가 나오면 정상입니다.
  ```powershell
  Test-NetConnection 192.168.0.25 -Port 2222
  ```

## 참고
- **수업 중에는 이 PC와 VM이 계속 켜져 있어야 합니다.** 이 PC의 IP가 바뀌면 학생들의 접속 주소도 바뀌니, 가능하면 고정 IP를 쓰세요.
- **학생 수가 많고 DB를 따로 써야 한다면** 학생마다 MySQL 계정과 DB를 만들어 주는 것이 좋습니다. 필요하면 생성 스크립트를 만들어 드리겠습니다.
- **학원·학교 네트워크가 PC끼리 통신을 막는 경우**(AP 격리 등)에는 위 설정을 해도 접속되지 않습니다. 그때는 네트워크 관리자에게 문의해야 합니다.
