# 우분투 리눅스 기초 명령어 — 입문 개발자용

Ubuntu 24.04 기준으로, 개발을 시작할 때 바로 쓰게 되는 명령어만 골라 정리했습니다.
처음부터 다 외울 필요는 없습니다. 필요할 때 찾아보고, 자주 쓰다 보면 손에 익습니다.

## 목차

1. [터미널과 프롬프트](#1-터미널과-프롬프트)
2. [도움말 보기](#2-도움말-보기)
3. [위치 확인과 이동](#3-위치-확인과-이동)
4. [파일·폴더 다루기](#4-파일폴더-다루기)
5. [파일 내용 보기](#5-파일-내용-보기)
6. [찾기](#6-찾기)
7. [권한과 sudo](#7-권한과-sudo)
8. [사용자 계정](#8-사용자-계정)
9. [패키지 설치 (apt)](#9-패키지-설치-apt)
10. [리다이렉션과 파이프](#10-리다이렉션과-파이프)
11. [프로세스 관리](#11-프로세스-관리)
12. [시스템 정보](#12-시스템-정보)
13. [네트워크](#13-네트워크)
14. [압축과 해제](#14-압축과-해제)
15. [텍스트 편집기](#15-텍스트-편집기)
16. [서비스 관리 (systemctl)](#16-서비스-관리-systemctl)
17. [개발 환경 설정](#17-개발-환경-설정)
18. [터미널 단축키](#18-터미널-단축키)
19. [주의할 명령어](#19-주의할-명령어)
20. [연습 문제](#20-연습-문제)

---

## 1. 터미널과 프롬프트

- 터미널 열기: `Ctrl + Alt + T`
- 명령어는 `명령 [옵션] [대상]` 형태로 씁니다. 예: `ls -l /etc`
- 리눅스는 **대소문자를 구분**합니다. `File.txt`와 `file.txt`는 다른 파일입니다.

프롬프트를 읽는 법:

```text
vboxuser@ubuntu:~/project$
```

| 부분 | 뜻 |
|---|---|
| `vboxuser` | 사용자 이름 |
| `ubuntu` | 컴퓨터 이름 |
| `~/project` | 현재 위치 (`~`는 홈 폴더) |
| `$` | 일반 사용자 (root이면 `#`) |

자주 쓰는 경로 기호:

| 기호 | 뜻 |
|---|---|
| `/` | 최상위(루트) 폴더 |
| `~` | 내 홈 폴더 (`/home/사용자이름`) |
| `.` | 현재 폴더 |
| `..` | 상위 폴더 |
| `-` | 직전에 있던 폴더 (`cd -`) |

주요 폴더:

```text
/
├── home/    # 사용자 홈 폴더 (/home/vboxuser)
├── etc/     # 설정 파일
├── var/     # 로그 등 자주 바뀌는 데이터 (/var/log)
├── usr/     # 설치된 프로그램
├── tmp/     # 임시 파일 (재부팅하면 지워짐)
└── root/    # root 계정의 홈 폴더
```

## 2. 도움말 보기

| 명령 | 설명 |
|---|---|
| `명령 --help` | 짧은 사용법 |
| `man 명령` | 자세한 매뉴얼 (`q`로 나가기, `/단어`로 검색) |
| `type 명령` | 이 명령이 무엇인지 (내장 명령, 별칭, 프로그램) |

```bash
ls --help
man ls
```

## 3. 위치 확인과 이동

| 명령 | 설명 |
|---|---|
| `pwd` | 현재 위치 출력 |
| `ls` | 현재 폴더의 파일 목록 |
| `ls -l` | 자세히 (권한, 크기, 날짜) |
| `ls -a` | 숨김 파일(`.`으로 시작)까지 |
| `ls -lh` | 크기를 KB, MB로 읽기 쉽게 |
| `cd 폴더` | 폴더로 이동 |
| `cd ..` | 상위 폴더로 |
| `cd` 또는 `cd ~` | 홈 폴더로 |
| `cd -` | 직전 폴더로 |

```bash
pwd
ls -alh
cd /var/log
cd ~
```

> 💡 폴더 이름을 몇 글자만 치고 `Tab`을 누르면 나머지가 자동으로 채워집니다.

## 4. 파일·폴더 다루기

| 명령 | 설명 |
|---|---|
| `mkdir 폴더` | 폴더 만들기 |
| `mkdir -p a/b/c` | 중간 폴더까지 한 번에 만들기 |
| `touch 파일` | 빈 파일 만들기 (있으면 수정 시각만 갱신) |
| `cp 원본 대상` | 파일 복사 |
| `cp -r 폴더 대상` | 폴더 통째로 복사 |
| `mv 원본 대상` | 이동, 또는 이름 바꾸기 |
| `rm 파일` | 파일 삭제 |
| `rm -r 폴더` | 폴더와 그 안의 내용 삭제 |
| `rmdir 폴더` | 빈 폴더만 삭제 |
| `ln -s 원본 링크` | 바로가기(심볼릭 링크) 만들기 |

```bash
mkdir -p ~/project/src
touch ~/project/README.md
cp ~/project/README.md ~/project/README.bak
mv ~/project/README.bak ~/project/old_README.md
rm ~/project/old_README.md
```

> ⚠️ 리눅스에는 휴지통이 없습니다. `rm`으로 지운 파일은 되살릴 수 없습니다. 처음에는 `rm -i`(하나씩 확인)를 쓰는 습관을 들이세요.

## 5. 파일 내용 보기

| 명령 | 설명 |
|---|---|
| `cat 파일` | 전체 출력 (짧은 파일) |
| `less 파일` | 한 화면씩 보기 (`Space` 다음, `b` 이전, `/` 검색, `q` 나가기) |
| `head -n 20 파일` | 앞 20줄 |
| `tail -n 20 파일` | 뒤 20줄 |
| `tail -f 파일` | 파일 끝에 새로 추가되는 줄을 계속 보기 (로그 확인, `Ctrl + C`로 종료) |
| `wc -l 파일` | 줄 수 세기 |
| `diff 파일1 파일2` | 두 파일의 다른 줄 비교 |

```bash
cat /etc/os-release
sudo tail -f /var/log/syslog
```

## 6. 찾기

| 명령 | 설명 |
|---|---|
| `find 위치 -name "이름"` | 이름으로 파일 찾기 |
| `find . -name "*.py"` | 현재 폴더 아래의 모든 `.py` 파일 |
| `find . -type d -name "venv"` | 폴더만 찾기 |
| `grep "단어" 파일` | 파일에서 단어가 들어간 줄 찾기 |
| `grep -rn "단어" 폴더` | 폴더 전체에서 찾기 (줄 번호 포함) |
| `grep -i "단어" 파일` | 대소문자 무시 |
| `which 명령` | 명령 프로그램이 설치된 위치 |

```bash
find ~ -name "*.md"
grep -rn "import numpy" ~/project
which python3
```

## 7. 권한과 sudo

`ls -l`의 결과 읽는 법 (예시):

```text
-rwxr-xr-- 1 vboxuser vboxuser 1234 Nov 18 10:00 run.sh
```

| 부분 | 뜻 |
|---|---|
| `-` (첫 글자) | 종류: `-` 파일, `d` 폴더, `l` 링크 |
| `rwx` | 소유자 권한 |
| `r-x` | 그룹 권한 |
| `r--` | 그 외 사용자 권한 |
| `vboxuser` (첫 번째) | 소유자 |
| `vboxuser` (두 번째) | 그룹 |
| `1234` | 크기 (바이트) |

| 글자 | 뜻 | 숫자 |
|---|---|---|
| `r` | 읽기 | 4 |
| `w` | 쓰기 | 2 |
| `x` | 실행 (폴더는 들어가기) | 1 |

숫자는 더해서 씁니다. `rwx = 4+2+1 = 7`, `r-x = 4+1 = 5`, `r-- = 4`이므로 위 예의 권한은 `754`입니다.

| 명령 | 설명 |
|---|---|
| `chmod +x 파일` | 실행 권한 추가 |
| `chmod 755 파일` | 숫자로 권한 지정 (소유자 rwx, 나머지 r-x) |
| `chmod 600 파일` | 나만 읽고 쓰기 (SSH 키 등 비밀 파일) |
| `sudo chown 사용자:그룹 파일` | 소유자 바꾸기 |
| `sudo 명령` | 관리자(root) 권한으로 한 번 실행 |
| `sudo -i` | root 셸로 들어가기 (`exit`로 나오기) |

```bash
chmod +x run.sh
./run.sh
```

> 💡 `Permission denied`가 나오면 권한 문제입니다. 무조건 `sudo`를 붙이기보다 먼저 `ls -l`로 소유자와 권한을 확인하세요.

## 8. 사용자 계정

| 명령 | 설명 |
|---|---|
| `whoami` | 현재 사용자 이름 |
| `id` | 사용자 번호와 속한 그룹 |
| `passwd` | 내 비밀번호 바꾸기 |
| `su - 사용자` | 다른 사용자로 전환 (`exit` 또는 `Ctrl + D`로 돌아오기) |
| `sudo adduser 이름` | 새 사용자 만들기 |
| `sudo usermod -aG sudo 이름` | 사용자에게 sudo 권한 주기 (다시 로그인해야 적용) |
| `sudo passwd -S root` | root 비밀번호 상태 (`L` 잠김, `P` 설정됨) |

> 💡 Ubuntu는 기본적으로 root 계정이 잠겨 있고, 일반 계정에서 `sudo`를 쓰는 방식을 권장합니다.

## 9. 패키지 설치 (apt)

| 명령 | 설명 |
|---|---|
| `sudo apt update` | 설치 가능한 패키지 목록 새로 받기 (설치 전에 먼저) |
| `sudo apt upgrade` | 설치된 패키지 모두 업데이트 |
| `sudo apt install 패키지` | 설치 |
| `sudo apt remove 패키지` | 삭제 (설정 파일은 남김) |
| `sudo apt purge 패키지` | 설정 파일까지 삭제 |
| `sudo apt autoremove` | 더 이상 필요 없는 의존 패키지 정리 |
| `apt search 단어` | 패키지 검색 |
| `apt list --installed` | 설치된 패키지 목록 |

개발을 시작할 때 자주 설치하는 패키지:

```bash
sudo apt update
sudo apt install -y git curl wget build-essential python3-pip python3-venv tree htop
```

## 10. 리다이렉션과 파이프

명령의 출력을 파일로 보내거나, 다른 명령의 입력으로 넘깁니다.

| 기호 | 설명 | 예 |
|---|---|---|
| `>` | 출력을 파일에 저장 (덮어쓰기) | `ls > list.txt` |
| `>>` | 파일 끝에 덧붙이기 | `echo "끝" >> list.txt` |
| `2>` | 에러 메시지만 파일로 | `python3 app.py 2> error.log` |
| `&>` | 출력과 에러 모두 파일로 | `python3 app.py &> all.log` |
| `\|` | 앞 명령의 출력을 뒤 명령의 입력으로 | `ls -l \| grep ".py"` |
| `&&` | 앞 명령이 성공하면 뒤 명령 실행 | `sudo apt update && sudo apt upgrade` |

```bash
# 프로세스 목록에서 python만 골라 보기
ps aux | grep python

# 가장 큰 폴더 5개
du -sh * | sort -rh | head -n 5
```

## 11. 프로세스 관리

| 명령 | 설명 |
|---|---|
| `ps aux` | 실행 중인 모든 프로세스 |
| `top` / `htop` | 실시간 CPU·메모리 사용량 (`q`로 나가기) |
| `kill PID` | 프로세스 종료 요청 (PID는 `ps`로 확인) |
| `kill -9 PID` | 강제 종료 (정상 종료가 안 될 때만) |
| `pkill 이름` | 이름으로 종료 |
| `명령 &` | 백그라운드에서 실행 |
| `jobs` | 현재 터미널의 백그라운드 작업 목록 |
| `fg` | 백그라운드 작업을 앞으로 가져오기 |
| `Ctrl + C` | 실행 중인 명령 중단 |
| `Ctrl + Z` | 일시 정지 (`fg`로 재개, `bg`로 백그라운드에서 재개) |

```bash
ps aux | grep python
kill 12345
```

## 12. 시스템 정보

| 명령 | 설명 |
|---|---|
| `lsb_release -a` | Ubuntu 버전 |
| `uname -a` | 커널 버전 |
| `hostname` | 컴퓨터 이름 |
| `uptime` | 켜져 있던 시간과 부하 |
| `df -h` | 디스크 남은 용량 |
| `du -sh 폴더` | 폴더 크기 |
| `free -h` | 메모리 사용량 |
| `nproc` | CPU 코어 수 |
| `date` | 현재 날짜와 시간 |
| `history` | 지금까지 입력한 명령 목록 |

## 13. 네트워크

| 명령 | 설명 |
|---|---|
| `ip a` | 내 IP 주소 (네트워크 장치별) |
| `ping 주소` | 연결 확인 (`Ctrl + C`로 종료, `-c 4`로 4번만) |
| `traceroute 주소` | 서버까지 거치는 홉 경로 (`sudo apt install traceroute`) |
| `tracepath 주소` | 설치 없이 쓰는 홉 경로 확인 |
| `ss -tulnp` | 열려 있는(대기 중인) 포트 목록 |
| `curl 주소` | 웹 요청을 보내고 응답 출력 (API 테스트) |
| `curl -I 주소` | 응답 헤더만 |
| `wget 주소` | 파일 내려받기 |
| `ssh 사용자@주소` | 원격 서버 접속 |
| `scp 파일 사용자@주소:경로` | 원격 서버로 파일 복사 |

```bash
ping -c 4 google.com
tracepath google.com
sudo ss -tulnp
curl https://api.github.com
```

> 💡 VirtualBox의 기본 네트워크(NAT)에서는 `traceroute`의 기본 방식이 잘 안 될 수 있습니다. 이때는 `sudo traceroute -I 주소`를 써 보세요.

## 14. 압축과 해제

| 명령 | 설명 |
|---|---|
| `tar -czvf 묶음.tar.gz 폴더` | 폴더를 `.tar.gz`로 압축 |
| `tar -xzvf 묶음.tar.gz` | `.tar.gz` 풀기 |
| `tar -xzvf 묶음.tar.gz -C 폴더` | 지정한 폴더에 풀기 |
| `zip -r 묶음.zip 폴더` | zip 압축 (`sudo apt install zip`) |
| `unzip 묶음.zip` | zip 풀기 (`sudo apt install unzip`) |

> 💡 tar 옵션 뜻: `c` 만들기, `x` 풀기, `z` gzip 압축, `v` 진행 과정 표시, `f` 파일 이름 지정.

## 15. 텍스트 편집기

**nano** (입문자에게 추천): `nano 파일`로 열고, 화면 아래에 단축키가 표시됩니다.

| 키 | 동작 |
|---|---|
| `Ctrl + O` → `Enter` | 저장 |
| `Ctrl + X` | 나가기 |
| `Ctrl + W` | 검색 |
| `Ctrl + K` / `Ctrl + U` | 줄 잘라내기 / 붙여넣기 |

**vim**: 서버에는 거의 항상 설치되어 있으니 최소한 나가는 법은 알아 두세요.

| 키 | 동작 |
|---|---|
| `i` | 입력 모드 (글자 쓰기 시작) |
| `Esc` | 명령 모드로 돌아가기 |
| `:w` | 저장 |
| `:q` | 나가기 |
| `:wq` | 저장하고 나가기 |
| `:q!` | 저장하지 않고 나가기 |

## 16. 서비스 관리 (systemctl)

웹 서버, DB처럼 계속 실행되는 프로그램(서비스)을 관리합니다.

| 명령 | 설명 |
|---|---|
| `systemctl status 서비스` | 상태 확인 |
| `sudo systemctl start 서비스` | 시작 |
| `sudo systemctl stop 서비스` | 중지 |
| `sudo systemctl restart 서비스` | 재시작 |
| `sudo systemctl enable 서비스` | 부팅할 때 자동 시작 |
| `sudo systemctl disable 서비스` | 자동 시작 끄기 |
| `journalctl -u 서비스 -f` | 서비스 로그 실시간 보기 |

```bash
systemctl status ssh
sudo systemctl restart ssh
```

## 17. 개발 환경 설정

**환경 변수**

```bash
echo $HOME              # 변수 값 보기
echo $PATH              # 명령을 찾는 폴더 목록
export MY_ENV=dev       # 현재 터미널에서만 유지되는 변수
env                     # 모든 환경 변수
```

**`~/.bashrc`**: 터미널을 열 때마다 실행되는 설정 파일입니다. 여기에 적으면 계속 유지됩니다.

```bash
nano ~/.bashrc
# 파일 끝에 추가
alias ll='ls -alh'
export PATH="$HOME/.local/bin:$PATH"

# 저장 후 바로 적용
source ~/.bashrc
```

**Python 가상 환경**

```bash
python3 --version
python3 -m venv .venv          # 가상 환경 만들기
source .venv/bin/activate      # 켜기 (프롬프트 앞에 (.venv) 표시)
pip install -r requirements.txt
deactivate                     # 끄기
```

**Git 기본 설정**

```bash
git config --global user.name "이름"
git config --global user.email "메일주소"
git clone 저장소주소
git status
git add .
git commit -m "메시지"
git push
```

**SSH 키 만들기** (GitHub, 원격 서버 접속용)

```bash
ssh-keygen -t ed25519 -C "메일주소"
cat ~/.ssh/id_ed25519.pub      # 이 공개 키를 GitHub 설정에 등록
```

> ⚠️ `id_ed25519`(`.pub`가 없는 파일)는 개인 키입니다. 다른 사람에게 보여 주거나 Git에 올리지 마세요.

## 18. 터미널 단축키

| 키 | 동작 |
|---|---|
| `Tab` | 자동 완성 (두 번 누르면 후보 목록) |
| `↑` / `↓` | 이전·다음 명령 |
| `Ctrl + R` | 지난 명령 검색 |
| `Ctrl + C` | 실행 중인 명령 중단 |
| `Ctrl + D` | 입력 끝 / 셸 종료 (`exit`와 같음) |
| `Ctrl + L` | 화면 지우기 (`clear`와 같음) |
| `Ctrl + A` / `Ctrl + E` | 줄 맨 앞 / 맨 뒤로 |
| `Ctrl + U` | 커서 앞 내용 지우기 |
| `Ctrl + Shift + C` / `V` | 터미널에서 복사 / 붙여넣기 |
| `!!` | 직전 명령 다시 실행 (`sudo !!`: 직전 명령을 sudo로) |

## 19. 주의할 명령어

| 명령 | 위험한 이유 |
|---|---|
| `rm -rf 경로` | 확인 없이 통째로 지웁니다. 경로를 잘못 쓰면 되돌릴 수 없습니다. 실행 전에 `ls 경로`로 대상을 먼저 확인하세요. |
| `sudo rm -rf /` | 시스템 전체를 지웁니다. 절대 실행하지 마세요. |
| `chmod -R 777 폴더` | 모든 사용자에게 모든 권한을 줍니다. 문제를 덮을 뿐 해결이 아니고 보안에 위험합니다. |
| `curl 주소 \| sudo bash` | 인터넷에서 받은 스크립트를 내용 확인 없이 관리자 권한으로 실행합니다. 먼저 내려받아 내용을 읽어 보세요. |
| `kill -9` | 정리 작업 없이 강제 종료해 데이터가 깨질 수 있습니다. 먼저 `kill`을 쓰세요. |
| `> 파일` | 기존 내용이 경고 없이 사라집니다. 덧붙일 때는 `>>`를 쓰세요. |

## 20. 연습 문제

아래 순서대로 직접 입력해 보세요.

1. 홈 폴더에 `practice/logs` 폴더를 한 번에 만드세요.
2. `practice` 폴더로 이동한 뒤 현재 위치를 출력하세요.
3. `hello.txt`를 만들고 `echo`로 "안녕 리눅스" 한 줄을 넣으세요.
4. `hello.txt`를 `logs` 폴더에 `hello_copy.txt`로 복사하세요.
5. `ls -l`로 `hello.txt`의 권한을 확인하고, 나만 읽고 쓸 수 있게(`600`) 바꾸세요.
6. 홈 폴더 아래의 모든 `.txt` 파일을 찾으세요.
7. 디스크 남은 용량과 메모리 사용량을 확인하세요.
8. `practice` 폴더를 `practice.tar.gz`로 압축한 뒤 폴더를 지우고, 압축을 풀어 되살리세요.

<details>
<summary>정답 보기</summary>

```bash
mkdir -p ~/practice/logs
cd ~/practice
pwd
echo "안녕 리눅스" > hello.txt
cp hello.txt logs/hello_copy.txt
ls -l hello.txt
chmod 600 hello.txt
find ~ -name "*.txt"
df -h
free -h
cd ~
tar -czvf practice.tar.gz practice
rm -r practice
tar -xzvf practice.tar.gz
```

</details>

### 확인 퀴즈

1. 프롬프트 끝이 `#`이면 어떤 계정인가요?
2. 파일을 덮어쓰지 않고 끝에 내용을 덧붙이는 기호는?
3. `chmod 754`에서 그룹 사용자가 가진 권한은?
4. `apt install` 전에 먼저 실행해야 하는 명령은?
5. vim에서 저장하지 않고 나가는 방법은?

<details>
<summary>정답 보기</summary>

1. root (관리자) 계정
2. `>>`
3. 읽기와 실행 (`5 = 4 + 1`, `r-x`)
4. `sudo apt update`
5. `Esc`를 누른 뒤 `:q!`

</details>
