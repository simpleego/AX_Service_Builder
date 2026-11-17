# Docker 실습 환경 (VirtualBox + Ubuntu)

## 왜 VirtualBox인가

이 PC(Ryzen 7 3700X / BIOSTAR A320MH, BIOS 2020)는 Windows 하이퍼바이저(Hyper-V)를 켜면 부팅 도중에 멈춥니다. Docker Desktop은 WSL2를 쓰고, WSL2는 이 하이퍼바이저가 있어야 동작합니다. 그래서 이 PC에서는 Docker Desktop을 쓸 수 없습니다. 11/16 이벤트 로그와 `docker-diag-result.txt`에서 확인한 내용입니다.

대신 **하이퍼바이저를 끈 상태에서 VirtualBox로 Ubuntu VM을 만들고, 그 안에 Docker Engine을 설치합니다.** 실제 서버의 Docker 환경과 같은 구성이라 강의 내용과도 잘 맞습니다.

```
Windows 11 (하이퍼바이저 OFF)
 └─ VirtualBox
     └─ Ubuntu Server 24.04 VM "docker-lab"  (4 CPU / 6GB / 40GB)
         └─ Docker Engine + Compose
             └─ 컨테이너들 ──(NAT 포트포워딩)──▶ Windows 브라우저 http://localhost:8080
```

## 사전 준비 (한 번만)

1. **하이퍼바이저가 꺼져 있는지 확인**합니다. 현재는 꺼져 있습니다. 만약 켜져 있다면 관리자 PowerShell에서 아래 명령을 실행하고 재부팅하세요.
   ```
   bcdedit /set hypervisorlaunchtype off
   ```
   - Docker Desktop, WSL2, "가상 머신 플랫폼"은 **설치하거나 켜지 마세요.** 다시 부팅이 멈출 수 있습니다.
2. **VirtualBox 설치**: https://www.virtualbox.org/wiki/Downloads 에서 "Windows hosts" 설치 파일을 받아 설치합니다.
3. **Ubuntu Server ISO**: https://ubuntu.com/download/server 에서 24.04 LTS ISO를 받아 `virtualbox\iso\` 폴더에 넣습니다.

## 설치 순서

PowerShell을 열고 `E:\AX_WORK\Docker\virtualbox` 폴더에서 아래 명령을 차례로 실행합니다. 관리자 권한은 필요 없습니다.

| 단계 | 명령 | 내용 |
|---|---|---|
| 1 | `powershell -ExecutionPolicy Bypass -File .\01-check-host.ps1` | 하이퍼바이저, VirtualBox, ISO, 디스크 공간 점검 (읽기 전용) |
| 2 | `powershell -ExecutionPolicy Bypass -File .\02-create-vm.ps1` | VM을 만들고 Ubuntu를 자동 설치 (10~20분) |
| 3 | `powershell -ExecutionPolicy Bypass -File .\03-install-docker.ps1` | SSH로 접속해 Docker Engine 설치, hello-world와 nginx로 동작 확인 |

3단계가 끝나면 브라우저에서 http://localhost:8080 을 엽니다. "Welcome to nginx!"가 보이면 설치가 완료된 것입니다.

설정값(VM 이름, CPU, 메모리, 계정, 포트)은 [config.ps1](config.ps1)에서 바꿀 수 있습니다.

## 수업 중 사용법

```
ssh -p 2222 docker@127.0.0.1
```

- **VS Code**: Remote-SSH 확장을 설치한 뒤 `docker@127.0.0.1:2222`로 접속하면 VM 안의 파일을 바로 편집할 수 있습니다.
- **공유 폴더**: Windows의 `E:\AX_WORK\Docker\work` 폴더가 VM 안에서는 `/media/sf_work`로 보입니다.
- **포트 매핑**: 컨테이너를 VM의 80, 3000, 5000, 8000, 8888 포트로 띄우면 Windows에서 아래 주소로 접속할 수 있습니다.

| Windows | VM |
|---|---|
| localhost:2222 | 22 (SSH) |
| localhost:8080 | 80 |
| localhost:3000 | 3000 |
| localhost:5000 | 5000 |
| localhost:8000 | 8000 |
| localhost:8888 | 8888 |

  예를 들어 `docker run -d -p 3000:3000 ...`으로 실행하면 Windows에서 http://localhost:3000 으로 접속합니다.
- **VM 끄기/켜기**: VirtualBox 관리자에서 하거나 아래 명령을 씁니다. `--type headless`로 켜면 창 없이 백그라운드에서 실행됩니다.
  ```
  & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm docker-lab --type headless
  & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" controlvm docker-lab acpipowerbutton
  ```
- **스냅샷**: Docker 설치 직후에 스냅샷을 찍어 두면, 수업이 끝날 때마다 깨끗한 상태로 되돌릴 수 있습니다.
  ```
  & "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" snapshot docker-lab take docker-installed
  ```

## 문제 해결

| 증상 | 해결 |
|---|---|
| VM 창 오른쪽 아래에 **거북이 아이콘**이 보이고 VM이 매우 느림 | Windows 하이퍼바이저가 켜져 있습니다. `bcdedit /set hypervisorlaunchtype off`를 실행하고 재부팅하세요. |
| `VT-x/AMD-V is not available` | BIOS에서 SVM Mode를 Enabled로 바꾸세요. |
| 자동 설치가 멈추거나 실패함 | VM을 삭제하고 VirtualBox에서 직접 ISO로 Ubuntu를 설치하세요. 설치할 때 "Install OpenSSH server"를 체크하고, 포트포워딩을 추가합니다. 설치가 끝나면 `scripts/install-docker.sh`를 VM으로 복사해 `sudo bash install-docker.sh`를 실행하면 됩니다. |
| `permission denied ... docker.sock` | docker 그룹이 아직 적용되지 않았습니다. `exit`로 나간 뒤 다시 SSH로 접속하세요. |
| `/media/sf_work` 접근이 거부됨 | 다시 로그인하세요. vboxsf 그룹이 적용됩니다. |
| 3단계에서 SSH 연결 실패 | VM에 로그인한 뒤 `sudo apt install -y openssh-server`를 실행하세요. |
