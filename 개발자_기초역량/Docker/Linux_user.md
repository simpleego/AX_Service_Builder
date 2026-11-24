# Linux 사용자 계정 명령어

-  파일·폴더 탐색/조작
-  텍스트 편집
-  프로세스·서비스 확인
-  네트워크·파일 전송
-  개발 환경 구성

---

## 1. 접속 직후 환경 및 위치 파악 실습

원격 접속 후 내가 어디에, 어떤 계정·시스템 상태로 들어왔는지 확인하는 단계입니다.

| 구분 | 명령어 | 실습 포인트 및 확인 방법 |
| --- | --- | --- |
| 계정·권한 확인 | `whoami`, `id` | 현재 접속한 사용자 이름과 소속 그룹 확인 |
| 현재 경로·목록 | `pwd`, `ls -alh` | 홈 폴더(`~`) 위치와 숨김 파일(`.bashrc`, `.ssh` 등) 포함 상세 목록 확인 |
| 이동 연습 | `cd /var/log`, `cd -`, `cd ~` | 절대 경로 이동, 직전 폴더(`-`) 복귀, 홈 복귀 연습 |
| 시스템 상태 | `lsb_release -a`, `uptime`, `df -h`, `free -h` | Ubuntu 버전, 가동 시간, 디스크 여유 공간, 메모리 상태 점검 |

---

## 2. 파일·폴더 생성, 탐색, 내용 확인 실습

프로젝트 작업 공간을 만들고, 로그나 설정 파일을 읽고 검색하는 단계입니다.

### 폴더·파일 조작

* `mkdir -p ~/lab/sub` : 실습용 중첩 폴더 한 번에 생성
* `touch ~/lab/sub/note.txt` : 빈 파일 생성
* `cp ~/lab/sub/note.txt ~/lab/note_bak.txt` : 파일 복사
* `mv ~/lab/note_bak.txt ~/lab/note_renamed.txt` : 이동 또는 이름 변경
* `ln -s ~/lab/note_renamed.txt ~/lab/note_link` : 심볼릭 링크 생성
* `rm -i ~/lab/note_renamed.txt` : 확인을 거치며 안전하게 파일 삭제 (`rm -r`로 폴더 삭제 시 대상 경로 먼저 확인)

### 파일 내용 보기 및 검색

* `cat /etc/os-release` : 짧은 파일 전체 출력
* `less /etc/passwd` : 긴 파일 페이지 단위 탐색 (`/단어` 검색, `q` 종료)
* `head -n 20 파일`, `tail -n 20 파일`, `tail -f 로그파일` : 앞/뒤 줄 및 실시간 로그 추적(`Ctrl + C`로 중단)
* `find ~ -name "*.txt"` : 홈 디렉터리 기준 특정 확장자 파일 검색
* `grep -rn "단어" 폴더` : 폴더 내 문자열 및 줄 번호 검색 (`-i`로 대소문자 구분 해제)

---

## 3. 권한 제어 및 관리자(`sudo`) 작업 실습

일반 사용자 계정에서 실행 권한을 다루고, 필요한 경우에만 `sudo`로 관리자 권한을 활용하는 단계입니다.

* `ls -l 파일` : 소유자, 그룹, 권한 문자열(`rwxr-xr--` 등) 확인
* `chmod +x script.sh` 또는 `chmod 755 script.sh` : 실행 권한 부여
* `chmod 600 secret_key` : 본인만 읽기/쓰기 가능하도록 제한
* `sudo apt update && sudo apt install -y git curl tree htop` : 패키지 목록 갱신 후 개발용 기본 도구 설치
* `sudo !!` : 방금 입력한 명령을 `sudo`를 붙여 재실행

> **주의:** `chmod -R 777`이나 출처 불명의 `curl ... | sudo bash`는 보안·안정성 위험이 크므로 실습에서도 피하는 것이 좋습니다.

---

## 4. 파이프·리다이렉션 및 프로세스·서비스 실습

명령 출력을 조합하고, 백그라운드 작업이나 실행 중인 프로세스·서비스를 다루는 단계입니다.

### 출력 연결 및 저장

* `ls -l > list.txt` : 결과를 파일로 저장(덮어쓰기)
* `echo "추가 줄" >> list.txt` : 기존 파일 끝에 내용 덧붙이기
* `ps aux | grep python` : 실행 중인 프로세스 중 `python` 관련 항목만 필터링
* `du -sh * | sort -rh | head -n 5` : 용량 큰 항목 상위 5개 정렬 출력

### 프로세스 및 서비스 제어

* `sleep 30 &` → `jobs` → `fg` : 백그라운드 실행, 작업 목록 확인, 포그라운드 전환 (`Ctrl + Z`로 일시 정지, `Ctrl + C`로 중단)
* `top` 또는 `htop` : 실시간 리소스 및 프로세스 확인 (`q`로 종료)
* `kill PID` : 정상 종료 요청 (강제 종료 `kill -9`는 최후 수단으로만 사용)
* `systemctl status ssh` 및 `journalctl -u ssh -f` : 서비스 상태와 로그 확인 (`start`/`stop`/`restart`는 `sudo` 필요)

---

## 5. 네트워크, 파일 전송, 압축 및 편집기 실습

원격 환경에서 외부 연결 점검, 파일 주고받기, 아카이브 관리, 텍스트 수정을 연습하는 단계입니다.

* **네트워크 점검:** `ip a`, `ping -c 4 google.com`, `tracepath google.com`, `ss -tulnp`, `curl -I [https://api.github.com](https://api.github.com)`
* **파일 복사 및 압축:** `scp 로컬파일 사용자@원격주소:경로`, `tar -czvf archive.tar.gz 대상폴더`, `tar -xzvf archive.tar.gz`
* **편집기 실습:** `nano 파일`(`Ctrl + O` 저장, `Ctrl + X` 종료) 또는 `vim 파일`(`i` 입력, `Esc` 후 `:wq` 저장·종료, `:q!` 강제 종료)

---

## 6. 개발 환경 및 원격 인증 설정 실습

터미널 세션을 유지할 설정과 Python·Git·SSH 작업 환경을 갖추는 단계입니다.

1. **셸 환경 설정 (`~/.bashrc`)**
* `alias ll='ls -alh'` 및 `export PATH="$HOME/.local/bin:$PATH"`를 `~/.bashrc`에 추가한 뒤 `source ~/.bashrc`로 즉시 반영 확인


2. **Python 가상 환경**
* `python3 -m venv .venv` → `source .venv/bin/activate` → 프롬프트 앞 `(.venv)` 확인 → `deactivate`로 해제


3. **Git 및 SSH 키**
* `git config --global user.name` / `user.email` 설정 후 저장소 클론 및 `git status` 확인
* `ssh-keygen -t ed25519 -C "메일주소"`로 키 쌍을 생성하고, `~/.ssh/id_ed25519.pub`(공개 키)만 등록 (개인 키 `id_ed25519`는 외부 노출 금지)



---

## 원격 접속 후 통합 실습 시나리오

위 항목들을 한 번에 이어서 연습해 볼 수 있는 순서입니다.

1. 원격 접속 후 `whoami`, `pwd`, `df -h`로 현재 계정·위치·디스크를 확인합니다.
2. `mkdir -p ~/remote_lab/logs`를 만들고 이동한 뒤, `echo "first line" > app.log`와 `echo "second line" >> app.log`를 실행합니다.
3. `cat app.log`, `grep -n "second" app.log`, `find ~/remote_lab -name "*.log"`로 내용을 검증합니다.
4. `chmod 600 app.log` 후 `ls -l app.log`로 권한이 `-rw-------`로 바뀌었는지 확인합니다.
5. `cd ~`로 돌아와 `tar -czvf remote_lab.tar.gz remote_lab`으로 압축하고, `rm -r remote_lab` 뒤 `tar -xzvf remote_lab.tar.gz`로 복구합니다.
