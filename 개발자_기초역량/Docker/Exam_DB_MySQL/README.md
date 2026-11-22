# 실습: Docker로 MySQL DB 서버 구성하고 로컬 PC에서 접속하기

## 실습 목표
1. Docker로 MySQL 8.4를 실행합니다. (**Image, Container**)
2. Compose로 "서버"답게 구성합니다. 자동 재시작, 데이터 보존, 초기 테이블 생성까지 설정합니다. (**Compose, Volume**)
3. 로컬 PC(Windows)에서 포트로 접속해 조회합니다. (**Network, 포트 매핑**)

## 구성도

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryTextColor': '#263238', 'lineColor': '#607D8B', 'fontFamily': 'Noto Sans KR, sans-serif'}}}%%
graph TD
    %% --- 최상위 계층: Windows ---
    subgraph Win [Windows (로컬 PC)]
        direction TB
        subgraph Tools [클라이언트 도구]
            Py[Python]
            WB[MySQL Workbench]
            DB[DBeaver]
        end
    end

    %% --- 중간 계층: VirtualBox VM ---
    subgraph VBox [VirtualBox VM docker-lab]
        direction TB
        NAT[NAT 포트포워딩 13306 -> 3306]
        subgraph Ub [Ubuntu 환경]
            direction TB
            DockerCmd[docker run -p 3306:3306]
        end
    end

    %% --- 최하위 계층: Docker 컨테이너 ---
    subgraph DCont [컨테이너 lab-mysql]
        MySQL[MySQL 8.4 서비스]
        IntPort[:3306]
    end

    %% --- 외부 영구 저장소 ---
    Volume[(Docker Volume)]

    %% --- 연결 정의 및 라벨링 ---

    %% Windows 도구 -> NAT 연결
    Py -- "127.0.0.1:13306" --> NAT
    WB -- "127.0.0.1:13306" --> NAT
    DB -- "127.0.0.1:13306" --> NAT

    %% NAT -> Ubuntu -> 컨테이너 연결
    NAT -- "내부 네트워크" --> Ub
    Ub -- "포트 매핑" --> DCont

    %% 컨테이너 내부 구성
    MySQL -- "서비스 실행" --> IntPort

    %% 볼륨 마운트 연결
    MySQL <== "영구 데이터 저장" ==> Volume

    %% 스타일 적용 (시각적 구분)
    classDef client fill:#E1F5FE,stroke:#0277BD,stroke-width:2px;
    classDef vm fill:#E0F2F1,stroke:#00695C,stroke-width:2px;
    classDef container fill:#FFF9C4,stroke:#FBC02D,stroke-width:2px;
    classDef storage fill:#FCE4EC,stroke:#C2185B,stroke-width:2px,stroke-dasharray: 5 5;

    class Py,WB,DB client;
    class NAT,Ub,DockerCmd vm;
    class MySQL,IntPort container;
    class Volume storage;
```

> Windows의 3306 포트는 이 PC에 설치된 **MariaDB**가 이미 쓰고 있습니다. 그래서 Docker MySQL에는 **13306**으로 접속합니다. 같은 포트를 두 프로그램이 동시에 쓸 수 없다는 것도 이번 실습에서 확인할 포인트입니다.

## 파일 구성

```
Exam_DB_MySQL/
├── docker-compose.yml   # MySQL 서버 정의
├── .env                 # 계정/비밀번호 (실습용 값)
├── conf/my.cnf          # 문자셋(utf8mb4), 시간대, 외부 접속 허용
├── init/01-schema.sql   # 최초 1회 실행: members, orders 테이블 + 샘플 데이터
├── sql/practice.sql     # 조회 실습 SQL
└── client/
    ├── query.py         # Windows에서 접속/조회하는 Python 예제
    └── requirements.txt
```

| 항목 | 값 |
|---|---|
| DB | `lab_db` |
| 원격 접속 계정 | `lab_user` (비밀번호는 `.env` 참고) |
| root | 컨테이너 안에서만 접속 가능 (원격 차단) |
| Windows에서 접속 | `127.0.0.1:13306` |

---

## 0단계: 준비 (VirtualBox VM과 Docker 설치 완료 상태)

`virtualbox` 폴더의 01~03 스크립트로 VM과 Docker를 먼저 설치하세요. 아래는 VM에 MySQL 포트포워딩을 추가하는 방법입니다.

- **VM을 새로 만드는 경우**: `config.ps1`에 `mysql,13306,3306`이 이미 들어 있어서 자동으로 추가됩니다.
- **VM을 이미 만든 경우**: Windows PowerShell에서 아래 명령을 한 번 실행합니다. VM이 켜져 있어도 됩니다.

```bash
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" controlvm docker-lab natpf1 "mysql,tcp,127.0.0.1,13306,,3306"
```

VM이 꺼져 있다면 `controlvm docker-lab natpf1` 대신 `modifyvm docker-lab --natpf1`을 쓰세요.

## 1단계: VM에 접속하고 실습 파일 가져오기

```bash
ssh -p 2222 docker@127.0.0.1
```

VM 안에서 아래 명령을 실행합니다.

```bash
cp -r /media/sf_work/Exam_DB_MySQL ~/ && cd ~/Exam_DB_MySQL
```
```bash
find . -type f \( -name '*.yml' -o -name '*.sql' -o -name '*.cnf' -o -name '.env' \) -exec sed -i 's/\r$//' {} +
```

> **왜 복사하나요?** 공유 폴더(`/media/sf_*`)는 VirtualBox 전용 파일시스템이라, 컨테이너 안의 mysql 사용자가 파일을 읽지 못하는 권한 문제가 생깁니다. 두 번째 명령은 Windows 줄바꿈(CRLF)을 Linux 줄바꿈(LF)으로 바꿉니다.

---

## 2단계 (개념 맛보기): `docker run`으로 한 줄 실행

Compose를 쓰기 전에, MySQL 컨테이너가 결국 무엇을 하는지 먼저 확인합니다.

```bash
docker run -d --name quick-mysql -e MYSQL_ROOT_PASSWORD=test1234 -p 3306:3306 mysql:8.4
```
```bash
docker ps
```
```bash
docker logs -f quick-mysql
```

로그에 `ready for connections`가 보이면 Ctrl+C로 로그 보기를 끝냅니다.

```bash
docker exec -it quick-mysql mysql -uroot -ptest1234 -e "SELECT VERSION();"
```

확인했으면 삭제합니다. 다음 단계에서 같은 3306 포트를 쓰기 때문입니다.

```bash
docker rm -f quick-mysql
```

**이 방식의 한계**
- 옵션이 길어서 매번 입력하기 어렵습니다.
- Volume이 없어서 컨테이너를 삭제하면 데이터도 사라집니다.
- 재부팅하면 자동으로 다시 켜지지 않습니다.

다음 단계에서 Compose로 이 문제들을 해결합니다.

---

## 3단계: Compose로 DB 서버 구성

[docker-compose.yml](docker-compose.yml)에서 볼 핵심 설정은 아래와 같습니다.

| 설정 | 의미 |
|---|---|
| `image: mysql:8.4` | LTS 버전 이미지 사용 |
| `restart: unless-stopped` | 장애가 나거나 VM이 재부팅되면 **자동으로 다시 시작**합니다. 서버 운영의 기본입니다. |
| `ports: "3306:3306"` | VM의 3306 포트를 컨테이너의 3306 포트로 연결 |
| `mysql-data:/var/lib/mysql` | DB 파일을 **Named Volume**에 저장해서 컨테이너를 지워도 데이터가 남습니다 |
| `./init:/docker-entrypoint-initdb.d` | DB를 **처음 만들 때 한 번만** SQL을 자동 실행 (테이블과 샘플 데이터 생성) |
| `MYSQL_USER / MYSQL_PASSWORD` | 원격 접속용 일반 계정을 만들고 `lab_db`에 대한 권한을 줍니다 |
| `MYSQL_ROOT_HOST: localhost` | root 원격 접속을 차단합니다 (보안) |
| `healthcheck` | DB가 정말 접속 가능한 상태인지 주기적으로 검사합니다 |
| `conf/my.cnf`의 `bind-address=0.0.0.0` | 외부 접속을 받는 **서버 설정** |

```bash
docker compose up -d
```

처음에는 이미지를 받고 DB를 초기화하느라 30초~1분 정도 걸립니다. 아래 명령으로 상태를 확인하고, STATUS가 **`(healthy)`**가 될 때까지 기다리세요.

```bash
docker compose ps
```
```bash
docker compose logs mysql | tail -n 20
```

`(healthy)`가 되면 접속할 준비가 된 것입니다.

---

## 4단계: VM 안에서 먼저 확인

```bash
docker exec -it lab-mysql mysql -ulab_user -plabpass1234 lab_db -e "SHOW TABLES; SELECT * FROM members;"
```

실습 SQL 전체를 실행해 봅니다.

```bash
docker exec -i lab-mysql mysql -ulab_user -plabpass1234 --table < sql/practice.sql
```

포트가 VM에 열려 있는지도 확인합니다.

```bash
ss -lntp | grep 3306
```

---

## 5단계: 로컬 PC(Windows)에서 접속하기

이제 VM 밖으로 나와서 **Windows**에서 작업합니다.

### 방법 A: Python (추천: 코드로 DB에 접속하는 기본 패턴)

Windows PowerShell에서 실행합니다.

```bash
cd E:\AX_WORK\Docker\Exam_DB_MySQL\client
```
```bash
pip install -r requirements.txt
```
```bash
python query.py
```

정상이라면 이렇게 출력됩니다.

```
접속 시도: lab_user@127.0.0.1:13306/lab_db

=== 서버 정보 (container_id = Docker 컨테이너 ID) ===
version | container_id | server_time
------------------------------------------------------------
8.4.x | 3f2a9c1b7d4e | 2026-11-17 14:30:00
...
=== 회원별 주문 합계 ===
name | order_count | total_amount
이컨테 | 1 | 289000
...
접속/조회 성공!
```

> `container_id`가 `docker ps`에 나오는 컨테이너 ID와 같으면, **Windows에서 VM 안의 컨테이너까지 연결된 것**이 확인됩니다.

### 방법 B: GUI 도구 (MySQL Workbench / DBeaver)

| 항목 | 값 |
|---|---|
| Host | `127.0.0.1` |
| Port | `13306` |
| Username | `lab_user` |
| Password | `labpass1234` |
| Database | `lab_db` |

- **DBeaver**: 연결 설정 → Driver properties에서 `allowPublicKeyRetrieval=true`, `useSSL=false`로 설정합니다. MySQL 8의 기본 인증 방식 때문에 필요합니다.
- 연결한 뒤 [sql/practice.sql](sql/practice.sql)의 쿼리를 하나씩 실행해 봅니다.

### 방법 C: 이 PC의 MariaDB 클라이언트 (참고)

```bash
& "C:\Program Files\MariaDB 11.4\bin\mysql.exe" -h 127.0.0.1 -P 13306 -u lab_user -p lab_db --skip-ssl-verify-server-cert
```

> MariaDB 클라이언트는 MySQL 8의 `caching_sha2_password` 인증과 맞지 않아 접속이 안 될 수 있습니다. 그럴 때는 A나 B 방법을 쓰세요.

> **흔한 실수**: `-P 3306`으로 접속하면 Docker MySQL이 아니라 **로컬 MariaDB**에 접속됩니다. `SELECT VERSION();`을 실행했을 때 `MariaDB`가 나오면 포트를 잘못 지정한 것입니다.

---

## 6단계: 데이터 영속성(Volume) 확인

Windows(Workbench/DBeaver)나 VM에서 데이터를 하나 추가합니다.

```sql
INSERT INTO members (name, email, city) VALUES ('정네트', 'network.jung@example.com', '광주');
```

VM 안에서 컨테이너를 **삭제한 뒤 다시** 만들어 봅니다.

```bash
docker compose down
```
```bash
docker compose up -d
```

다시 조회했을 때 '정네트'가 **남아 있으면**, Volume 덕분에 데이터가 보존된 것입니다.

```bash
docker exec -it lab-mysql mysql -ulab_user -plabpass1234 lab_db -e "SELECT * FROM members;"
```

완전히 초기화하려면 `-v` 옵션으로 Volume까지 삭제합니다. 다음에 실행할 때 init SQL이 다시 실행됩니다.

```bash
docker compose down -v
```

---

## 7단계: 서버 운영 기본 명령

| 목적 | 명령 |
|---|---|
| 상태 확인 | `docker compose ps` |
| 로그 보기 | `docker compose logs -f mysql` |
| 리소스 사용량 | `docker stats lab-mysql` |
| 컨테이너 안에 들어가기 | `docker exec -it lab-mysql bash` |
| 백업 | `docker exec lab-mysql mysqldump -uroot -prootpass1234 lab_db > backup.sql` |
| 복원 | `docker exec -i lab-mysql mysql -uroot -prootpass1234 lab_db < backup.sql` |
| 중지 / 시작 | `docker compose stop` / `docker compose start` |
| 볼륨 확인 | `docker volume ls`, `docker volume inspect exam_db_mysql_mysql-data` |

---

## 확장 과제

1. **읽기 전용 계정 만들기**: 조회만 가능한 계정을 만들어 권한의 개념을 익힙니다.
   ```sql
   -- docker exec -it lab-mysql mysql -uroot -prootpass1234
   CREATE USER 'reader'@'%' IDENTIFIED BY 'reader1234';
   GRANT SELECT ON lab_db.* TO 'reader'@'%';
   ```
   `reader`로 접속해서 INSERT를 실행하면 거부되는지 확인합니다.
2. **테이블 추가**: `init/02-products.sql` 파일을 추가한 뒤 `docker compose down -v && docker compose up -d`로 초기화가 다시 되는지 확인합니다.
3. **다른 PC에서 접속**(강의실의 수강생 PC 등):
   - 포트포워딩의 호스트 IP를 `127.0.0.1`에서 빈 값(모든 IP)으로 바꿉니다.
   - Windows 방화벽에서 13306 인바운드를 허용합니다. 관리자 권한이 필요합니다.
   - 수강생은 `강사PC_IP:13306`으로 접속합니다.
   - 실제로 외부에 공개할 때는 강한 비밀번호와 접속 IP 제한이 꼭 필요합니다.

---

## 문제 해결

| 증상 | 원인 / 해결 |
|---|---|
| `docker compose ps`에서 `(unhealthy)` 또는 재시작이 반복됨 | `docker compose logs mysql`로 원인을 확인합니다. 설정을 바꿨다면 `docker compose down -v`로 초기화합니다. |
| 테이블이 없음 | init SQL은 **Volume이 비어 있을 때만** 실행됩니다. `docker compose down -v` 후 다시 `up`합니다. |
| `Bind for 0.0.0.0:3306 failed: port is already allocated` | 2단계의 `quick-mysql`이 남아 있습니다. `docker rm -f quick-mysql`로 삭제합니다. |
| Windows에서 `Can't connect ... (10061)` | ① VM이 켜져 있는지 ② 13306 포트포워딩이 있는지 (`VBoxManage showvminfo docker-lab \| findstr mysql`) ③ 컨테이너가 healthy인지 확인합니다. |
| `Access denied for user 'root'@...` | 의도된 동작입니다. root는 원격 접속을 막아 두었으니 `lab_user`를 쓰세요. |
| Python: `cryptography package is required` | `pip install cryptography` |
| 한글이 깨짐 | 클라이언트 문자셋을 `utf8mb4`로 설정합니다. 이미 깨진 데이터는 `down -v`로 다시 초기화합니다. |
| init SQL의 한글이 깨지거나 SQL 오류 | 1단계의 CRLF 변환(`sed`) 명령을 실행했는지 확인합니다. |
