# Docker Compose
# **Docker Compose 완전 이해: 개념부터 MySQL 서버 구축까지**

Docker Compose는 **여러 Docker 컨테이너의 실행 환경을 하나의 YAML 파일에 정의하고, 하나의 명령어로 생성·실행·관리할 수 있도록 해주는 도구**입니다.

제시하신 `docker-compose.yml`은 Docker Compose를 처음 배우는 개발자에게 적합한 예제입니다. MySQL 서버 한 개만 실행하지만, 컨테이너를 운영하는 데 필요한 이미지, 환경변수, 포트, 데이터 저장소, 상태 검사까지 포함하고 있기 때문입니다.

## **1. Docker Compose란 무엇인가?**

Docker를 직접 사용할 때는 `docker run` 명령어에 실행에 필요한 옵션을 하나씩 지정합니다.

반면 Docker Compose는 이러한 옵션을 **설정 파일에 미리 작성하고, 필요할 때 재사용하는 방식**입니다.

**Docker Run**

실행할 때 옵션을 직접 입력

`docker run -d ...`

`-p 3306:3306 ...`

`-v mysql-data:...`

`-e MYSQL_...`

**Docker Compose**

설정 파일에 실행 방법 저장

`docker-compose.yml`

이미지 · 포트

환경변수 · 볼륨

재시작 · 상태 검사

`docker compose up -d`

설정 파일을 읽고 필요한 Docker 리소스를 준비하여 실행

쉽게 비유하면 다음과 같습니다.

- **Dockerfile:** 요리의 레시피 — 어떤 재료로 이미지를 만들 것인가?
- **Docker Image:** 준비된 밀키트 — 실행에 필요한 프로그램과 파일이 담겨 있음
- **Docker Container:** 실제 요리한 음식 — 이미지로부터 만들어진 실행 인스턴스
- **Docker Compose:** 식당 운영 계획서 — 어떤 서비스를 몇 개 실행하고, 어떻게 연결하며, 어디에 데이터를 저장할 것인가?

Docker Compose는 여러 컨테이너뿐만 아니라, 지금 예제처럼 **컨테이너 한 개를 체계적으로 운영하는 데도 유용**합니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.docker.com\&sz=32)

Docker Docs+1



## **2. Docker Compose가 필요한 이유**

MySQL 서버를 Docker로 실행한다고 가정하겠습니다.

### **방법 A. docker run 사용**

```
docker run -d \
  --name lab-mysql \
  --restart unless-stopped \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=root1234 \
  -e MYSQL_DATABASE=examdb \
  -e MYSQL_USER=student \
  -e MYSQL_PASSWORD=student1234 \
  -e TZ=Asia/Seoul \
  -v mysql-data:/var/lib/mysql \
  mysql:8.4
```

실행은 가능하지만, 설정이 길어질수록 다음과 같은 문제가 있습니다.

- 명령어를 외우거나 별도로 보관해야 합니다.
- 포트나 비밀번호 변경 시 실행 옵션을 다시 확인해야 합니다.
- 여러 컨테이너로 확장하면 명령어가 복잡해집니다.
- 학생마다 실행 옵션이 달라질 수 있습니다.

### **방법 B. Docker Compose 사용**

이러한 실행 옵션을 `docker-compose.yml`에 저장합니다.

```
services:
  mysql:
    image: mysql:8.4
    container_name: lab-mysql

    ports:
      - "3306:3306"

    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}

    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  mysql-data:
```

이제 다음 명령어만 실행합니다.

```
docker compose up -d
```

Docker Compose가 파일을 읽고 MySQL 컨테이너, 포트 매핑, 볼륨 등을 준비합니다.

**핵심 차이:** `docker run`은 명령어 중심, Docker Compose는 선언형 설정 파일 중심의 관리 방식입니다.

## **3. docker-compose.yml의 전체 계층구조**

제시하신 예제의 YAML 구조를 계층적으로 표현하면 다음과 같습니다.

**docker-compose.yml**

**services**

실행할 서비스 정의

**mysql**

MySQL 서비스 이름

image

mysql:8.4 이미지 사용

container_name

컨테이너 이름 lab-mysql

restart

자동 재시작 정책

environment

DB 계정·비밀번호·시간대

ports

VM 포트 ↔ 컨테이너 포트

volumes

데이터·설정·SQL 연결

healthcheck

MySQL 상태 검사

**volumes**

프로젝트의 볼륨 정의

mysql-data

DB 데이터 영구 저장

여기서 중요한 점은 `services`**&#x20;아래의&#x20;**`volumes`**와 최상위&#x20;**`volumes`**는 역할이 다르다**는 것입니다.

- `services.mysql.volumes`: MySQL 컨테이너에 무엇을 연결할 것인가?
- 최상위 `volumes`: Compose 프로젝트에서 관리할 Named Volume을 무엇으로 정의할 것인가?

Docker Compose는 서비스 외에도 최상위 `networks`, `configs`, `secrets` 등을 지원하지만, 이 MySQL 예제에서는 `services`와 `volumes`가 핵심입니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.docker.com\&sz=32)

Docker Docs+1



## **4. 각 항목을 실제 예제로 상세 분석**

### **① services: 어떤 서버를 실행할 것인가?**

```
services:
  mysql:
    image: mysql:8.4
    container_name: lab-mysql
```

| 항목               | 설명                       |
| ---------------- | ------------------------ |
| `services`       | 실행할 서비스들을 정의하는 최상위 항목    |
| `mysql`          | Compose 내부에서 사용하는 서비스 이름 |
| `image`          | 컨테이너를 생성할 이미지와 태그        |
| `container_name` | 실제 Docker 컨테이너 이름        |

**서비스 이름과 컨테이너 이름은 다릅니다.**

예를 들어 FastAPI 서비스를 추가한다면 다음과 같이 확장할 수 있습니다.

```
services:
  mysql:
    image: mysql:8.4

  backend:
    build: ./backend
```

이렇게 작성하면 MySQL과 FastAPI 서비스를 하나의 Compose 프로젝트로 관리할 수 있습니다. 같은 기본 네트워크에 속한 컨테이너들은 `mysql`과 같은 서비스 이름으로 서로 접근할 수 있습니다.

### **② restart: 언제 자동으로 재시작할 것인가?**

```
restart: unless-stopped
```

| 설정값              | 동작                                           |
| ---------------- | -------------------------------------------- |
| `no`             | 자동 재시작하지 않음 (기본값)                            |
| `always`         | 종료되면 자동 재시작, 수동 중지 후 Docker 데몬이 재시작되어도 다시 시작 |
| `on-failure`     | 비정상 종료 시 재시작                                 |
| `unless-stopped` | 자동 재시작하지만 사용자가 명시적으로 중지한 컨테이너는 자동 재시작하지 않음   |

MySQL은 계속 실행되어야 하는 서버이므로 `unless-stopped`가 적합합니다.

단, Docker 데몬 자체가 시작되어야 하고, `restart` 정책은 컨테이너의 비정상 상태를 모두 자동 복구하는 기능은 아닙니다.

### **③ environment: MySQL 초기 설정**

```
environment:
  MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
  MYSQL_ROOT_HOST: localhost
  MYSQL_DATABASE: ${MYSQL_DATABASE}
  MYSQL_USER: ${MYSQL_USER}
  MYSQL_PASSWORD: ${MYSQL_PASSWORD}
  TZ: Asia/Seoul
```

| 환경변수                  | 역할                             |
| --------------------- | ------------------------------ |
| `MYSQL_ROOT_PASSWORD` | root 관리자 비밀번호                  |
| `MYSQL_ROOT_HOST`     | 이미지 초기화 시 생성하는 root 계정의 허용 호스트 |
| `MYSQL_DATABASE`      | 최초 생성할 데이터베이스                  |
| `MYSQL_USER`          | 최초 생성할 일반 사용자                  |
| `MYSQL_PASSWORD`      | 일반 사용자 비밀번호                    |
| `TZ`                  | 컨테이너의 시간대                      |

`${변수명}`은 Compose가 변수 값을 치환하는 문법입니다.

예를 들어 `.env` 파일을 다음처럼 구성할 수 있습니다.

```
MYSQL_ROOT_PASSWORD=root1234
MYSQL_DATABASE=examdb
MYSQL_USER=student
MYSQL_PASSWORD=student1234
```

이 경우 Compose는 `.env`의 값으로 YAML 설정의 변수를 치환한 뒤 컨테이너를 생성합니다.

**중요: 최초 초기화와 비밀번호**

환경변수로 지정하는 MySQL 사용자·DB 생성 설정은 일반적으로 데이터 디렉터리가 비어 있는 최초 초기화에 적용됩니다. Named Volume에 기존 데이터가 있다면 `.env`의 비밀번호를 수정하고 재실행해도 기존 DB 계정의 비밀번호가 자동 변경되지는 않습니다.

또한 `.env`는 비밀번호를 소스코드와 분리할 수 있지만, 암호화된 비밀 저장소는 아닙니다. Git에 올리지 말고 접근 권한을 관리해야 합니다.

### **④ ports: 외부에서 MySQL에 접속하는 방법**

```
ports:
  - "3306:3306"
```

형식은 다음과 같습니다.

```
"호스트포트:컨테이너포트"
```

현재 실습 환경은 Windows → VirtualBox → Ubuntu → Docker → MySQL 구조입니다.

**Windows 로컬 PC**

Python / MySQL Workbench / DBeaver

127.0.0.1:13306

VirtualBox NAT 포트 포워딩

13306 → 3306

**Ubuntu VM (docker-lab)**

Docker Engine

호스트 포트 3306

Docker 포트 매핑

3306 → 3306

**lab-mysql**

MySQL 8.4 / 포트 3306

포트 변환이 두 번 발생합니다.

1. **VirtualBox:** Windows의 `13306`을 Ubuntu VM의 `3306`으로 전달
2. **Docker:** Ubuntu의 `3306`을 MySQL 컨테이너의 `3306`으로 전달

Docker Compose는 두 번째 포트 매핑만 관리합니다. 첫 번째 NAT 포트 포워딩은 VirtualBox에서 별도로 설정해야 합니다.

참고로 `"3306:3306"`은 일반적으로 VM의 모든 호스트 인터페이스에 포트를 게시합니다. 외부 노출을 제한하려면 바인딩 주소와 방화벽을 별도로 설정해야 합니다.

### **⑤ volumes: 컨테이너의 파일을 어디에 저장할 것인가?**

```
volumes:
  - mysql-data:/var/lib/mysql
  - ./conf/my.cnf:/etc/mysql/conf.d/lab.cnf:ro
  - ./init:/docker-entrypoint-initdb.d:ro
```

이 세 줄은 서로 다른 목적을 가집니다.

| 항목                          | 마운트 유형       | 역할             |
| --------------------------- | ------------ | -------------- |
| `mysql-data:/var/lib/mysql` | Named Volume | DB 데이터 영구 저장   |
| `./conf/my.cnf:...:ro`      | Bind Mount   | MySQL 설정 파일 제공 |
| `./init:...:ro`             | Bind Mount   | 초기화 SQL 제공     |

**Named Volume — 데이터 보존**

Docker 관리 저장소

`/var/lib/mysql`

컨테이너를 삭제·재생성해도 볼륨이 유지되면 DB 데이터 보존

**Bind Mount — 설정 파일 연결**

`./conf/my.cnf`

`/etc/mysql/conf.d/lab.cnf`

Ubuntu VM의 설정 파일을 컨테이너에 읽기 전용으로 연결

**Bind Mount — 초기화 SQL 연결**

`./init/`

`/docker-entrypoint-initdb.d/`

DB 최초 초기화 시 SQL을 실행하기 위해 파일을 제공

여기서 `:ro`는 \*\*읽기 전용(Read Only)\*\*을 의미합니다.

그리고 YAML 마지막에 선언한 다음 코드는

```
volumes:
  mysql-data:
```

`mysql-data`라는 Named Volume을 Compose 프로젝트에서 사용하도록 정의합니다. 특별한 `name`을 지정하지 않으면 실제 Docker 볼륨 이름에는 일반적으로 Compose 프로젝트 이름이 접두어로 붙습니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.docker.com\&sz=32)

Docker Docs+1



### **⑥ healthcheck: MySQL이 정상적으로 실행 중인가?**

```
healthcheck:
  test: ["CMD-SHELL", "mysqladmin ping -h 127.0.0.1 --silent"]
  interval: 10s
  timeout: 5s
  retries: 10
  start_period: 30s
```

| 항목             | 의미                       |
| -------------- | ------------------------ |
| `test`         | 컨테이너 내부에서 상태를 확인할 명령     |
| `interval`     | 검사 주기 10초                |
| `timeout`      | 검사를 완료할 제한 시간 5초         |
| `retries`      | 연속 실패 10회 시 unhealthy 판정 |
| `start_period` | 시작 초기 30초 동안 실패 횟수 계산 유예 |

단, `mysqladmin ping`은 MySQL 서버 프로세스의 응답 여부를 확인하는 검사로, **사용자 인증이나 SQL 조회가 정상적으로 작동한다는 사실까지 보장하지는 않습니다.**

따라서 실무에서는 실제 DB 계정으로 `SELECT 1` 같은 SQL을 실행하는 상태 검사도 고려할 수 있습니다.

또한 `healthcheck`가 `unhealthy`로 판정했다고 해서 `restart: unless-stopped`가 해당 컨테이너를 자동으로 재시작하는 것은 아닙니다. 이 둘은 서로 다른 기능입니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.docker.com\&sz=32)

Docker Docs+1



## **5. Docker Compose의 전체 구성요소 정리**

지금까지 살펴본 항목을 일반적인 Compose 파일의 구조로 확장하면 다음과 같습니다.

```
name: my-project          # 프로젝트 이름 (선택)

services:                 # 실행할 서비스 정의
  mysql:
    image: mysql:8.4      # 사용할 이미지
    container_name: lab-mysql
    restart: unless-stopped

    environment:           # 컨테이너 환경변수
      MYSQL_DATABASE: examdb

    ports:                 # 외부 접속 포트
      - "3306:3306"

    volumes:               # 저장소와 파일 마운트
      - mysql-data:/var/lib/mysql

    networks:              # 연결할 네트워크
      - backend-net

    healthcheck:           # 서비스 상태 검사
      test: ["CMD", "mysqladmin", "ping"]
      interval: 10s

networks:                  # 네트워크 정의
  backend-net:

volumes:                   # Named Volume 정의
  mysql-data:
```

위 코드는 구성요소 설명용 예제입니다. 비밀번호 등 필수 환경변수는 생략되어 있으므로 그대로 실행하는 완성형 설정은 아닙니다.

| 최상위 항목     | 핵심 역할             | 필수 여부 |
| ---------- | ----------------- | ----- |
| `name`     | 프로젝트 이름 지정        | 선택    |
| `services` | 실행할 컨테이너 서비스 정의   | 필수    |
| `networks` | 컨테이너 간 통신 네트워크 정의 | 선택    |
| `volumes`  | 영구 저장소 정의         | 선택    |
| `configs`  | 서비스에 설정 데이터 제공    | 선택    |
| `secrets`  | 서비스에 비밀 데이터 제공    | 선택    |

`build`, `ports`, `environment`, `depends_on`, `healthcheck` 등은 일반적으로 각 서비스 아래에서 지정합니다.

특히 Compose는 별도의 `networks`를 정의하지 않아도 프로젝트의 기본 네트워크를 생성하므로, **MySQL 컨테이너 한 개를 실행하는 현재 예제에는&#x20;**`networks`**&#x20;항목이 없어도 됩니다.**

## **6. Docker Compose 주요 실행 명령어**

Ubuntu VM에서 실행하는 실습 순서

1. **Compose 설정 검사**
   ```
   docker compose config -q
   ```
   YAML과 변수 치환이 유효한지 검사합니다.
2. **MySQL 서버 실행**
   ```
   docker compose up -d
   ```
   컨테이너를 생성하고 백그라운드에서 실행합니다.
3. **서비스 상태 확인**
   ```
   docker compose ps
   ```
   컨테이너 실행 상태와 포트 정보를 확인합니다.
4. **로그 확인**
   ```
   docker compose logs -f mysql
   ```
   MySQL 서버의 실행 로그를 확인합니다.
5. **MySQL 접속**
   ```
   docker compose exec mysql mysql -u root -p
   ```
   실행 중인 컨테이너 안에서 MySQL 클라이언트를 실행합니다.
6. **서비스 종료 및 정리**
   ```
   docker compose down
   ```
   컨테이너와 기본 네트워크를 제거하지만 Named Volume은 유지합니다.

### **주의: down과 down -v의 차이**

`docker compose down`

컨테이너 제거

Named Volume 유지

기존 DB 데이터를 남기고 서버를 정리할 때 사용

`docker compose down -v`

컨테이너 제거

Named Volume도 삭제

초기화 실습용. DB 데이터가 삭제될 수 있음

`down -v`로 볼륨을 삭제한 후 다시 `up -d`를 실행하면, 새로운 데이터 디렉터리가 초기화되면서 `init/01-schema.sql`이 다시 실행될 수 있습니다. 반드시 필요한 데이터를 백업한 후 사용해야 합니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.docker.com\&sz=32)

Docker Docs+1



## **7. 수업에서 강조할 핵심 개념**

다음 네 가지 개념을 구분하면 Docker Compose의 전체 구조를 쉽게 이해할 수 있습니다.

| 개념                   | 핵심 질문                     |
| -------------------- | ------------------------- |
| **Dockerfile**       | 이미지를 어떻게 만들 것인가?          |
| **Docker Image**     | 어떤 실행 환경을 사용할 것인가?        |
| **Docker Container** | 실제 실행 중인 프로그램은 무엇인가?      |
| **Docker Compose**   | 서비스들을 어떤 설정으로 함께 운영할 것인가? |

그리고 현재의 MySQL 실습은 다음 흐름으로 정리할 수 있습니다.

**docker-compose.yml 작성**

`docker compose up -d`**&#x20;실행**

**MySQL 8.4 이미지 준비**

**컨테이너 · 네트워크 · 볼륨 생성**

**최초 DB 초기화 및 MySQL 서버 실행**

**Windows Python / Workbench / DBeaver에서 접속**

**최종적으로 입문 개발자가 기억해야 할 문장:**

Docker는 컨테이너를 실행하는 기술이고, **Docker Compose는 컨테이너를 어떤 설정으로 실행하고 연결하고 관리할지 정의하는 도구**입니다.

처음에는 MySQL 서버 하나를 실행하는 데 사용하지만, 이후 FastAPI, React, Redis 등을 추가하면 여러 서비스를 함께 운영하는 개발 환경으로 확장할 수 있습니다.

공식 참고 문서: [Docker Compose Quickstart](https://docs.docker.com/compose/gettingstarted/?utm_source=chatgpt.com) · [Compose 파일 명세](https://docs.docker.com/reference/compose-file/?utm_source=chatgpt.com)
