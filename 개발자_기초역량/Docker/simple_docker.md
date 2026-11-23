# 간단한 도커 서비스 환경 구축 - MySQL

# **Docker 실습 강의교안: MySQL 서버 구축과 HeidiSQL 원격 접속**

입문 개발자

실습 40\~50분

Ubuntu + Docker + MySQL 8.4 + HeidiSQL

## **1. 실습 개요**

이번 실습은 **VirtualBox에 설치한 Ubuntu에서 Docker로 MySQL 서버를 실행하고, Windows에 설치된 HeidiSQL에서 접속하여 데이터베이스가 정상적으로 서비스되는지 확인**하는 과정입니다.

Docker의 이미지, 컨테이너, 포트 매핑, 데이터 영속성이라는 네 가지 핵심 개념을 자연스럽게 학습할 수 있도록 구성했습니다.

### **실습 환경 구조**

**Windows PC (호스트 컴퓨터)**

**HeidiSQL**

MySQL 데이터베이스 관리 프로그램

127.0.0.1 : 13306

VirtualBox NAT 포트 포워딩

**VirtualBox — Ubuntu VM**

Ubuntu TCP :3306

**Docker 컨테이너: mysql-lab**

MySQL 8.4

TCP 3306 · labdb 데이터베이스

Docker Volume

mysql_lab_data (데이터 보존)

여기에는 두 가지 포트 연결이 있습니다.

- **VirtualBox 포트 포워딩:** Windows의 `13306` → Ubuntu의 `3306`
- **Docker 포트 매핑:** Ubuntu의 `3306` → MySQL 컨테이너의 `3306`

따라서 Windows의 HeidiSQL은 Ubuntu의 IP 주소를 직접 사용하지 않고 `127.0.0.1:13306`으로 접속할 수 있습니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.oracle.com\&sz=32)

Oracle Docs+1



## **2. Ubuntu에 Docker 설치**

Ubuntu 24.04 LTS 기준으로 진행합니다. Docker가 이미 설치되어 있다면 설치 단계는 건너뜁니다.

### **① 패키지 업데이트**

```
sudo apt update
```

### **② Docker 설치**

```
sudo apt install -y docker.io
```

### **③ Docker 서비스 시작**

```
sudo systemctl enable --now docker
```

### **④ 설치 확인**

```
sudo docker --version
sudo docker run --rm hello-world
```

`Hello from Docker!`라는 메시지가 출력되면 정상입니다.

강의 편의를 위해 Ubuntu 저장소의 docker.io 패키지를 사용합니다. 공식 Docker CE를 별도로 설치하려면 [Docker 공식 설치 가이드](https://docs.docker.com/engine/install/ubuntu/?utm_source=chatgpt.com)를 이용합니다.

## **3. MySQL Docker 컨테이너 실행**

### **① MySQL 8.4 이미지 다운로드**

```
sudo docker pull mysql:8.4
```

이미지는 MySQL 서버를 실행하는 데 필요한 프로그램과 실행 환경이 포함된 템플릿입니다.

### **② MySQL 서버 실행**

아래 명령어를 Ubuntu 터미널에서 실행합니다.

```
sudo docker run -d \
  --name mysql-lab \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=Root1234! \
  -e MYSQL_DATABASE=labdb \
  -e MYSQL_USER=labuser \
  -e MYSQL_PASSWORD=Lab1234! \
  -v mysql_lab_data:/var/lib/mysql \
  --restart unless-stopped \
  mysql:8.4
```

비밀번호는 교육용 예시입니다. 외부 공개 서버나 실제 운영 환경에는 사용하지 않습니다.

### **명령어 옵션 설명**

| 옵션                                 | 의미                    |
| ---------------------------------- | --------------------- |
| `-d`                               | 백그라운드에서 실행            |
| `--name mysql-lab`                 | 컨테이너 이름 지정            |
| `-p 3306:3306`                     | Ubuntu 포트와 컨테이너 포트 연결 |
| `MYSQL_ROOT_PASSWORD`              | MySQL root 비밀번호       |
| `MYSQL_DATABASE`                   | 최초 생성할 DB             |
| `MYSQL_USER`                       | 일반 DB 사용자 생성          |
| `MYSQL_PASSWORD`                   | 일반 사용자 비밀번호           |
| `-v mysql_lab_data:/var/lib/mysql` | DB 데이터 영구 보관          |
| `--restart unless-stopped`         | 서버 재시작 시 자동 실행 설정     |

환경변수에 따라 MySQL이 최초 기동 시 DB와 사용자를 자동 생성합니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://hub.docker.com\&sz=32)

Docker Hub+1



### **③ 실행 여부 확인**

```
sudo docker ps
```

정상 실행되면 다음과 유사한 결과가 출력됩니다.

```
CONTAINER ID   IMAGE       STATUS      PORTS
a1b2c3d4e5f6   mysql:8.4   Up 1 min    0.0.0.0:3306->3306/tcp
```

단, `Up`은 컨테이너 프로세스가 실행 중이라는 의미이며, MySQL이 접속 준비를 완료했다는 뜻은 아닙니다.

### **④ 컨테이너 내부에서 MySQL 접속 확인**

```
sudo docker exec -it mysql-lab \
  mysql -u labuser -p labdb
```

비밀번호 `Lab1234!`를 입력합니다.

```
SELECT VERSION();
SHOW DATABASES;
EXIT;
```

정상적으로 MySQL 버전과 데이터베이스 목록이 조회되면 MySQL 서버가 실행된 것입니다.

## **4. VirtualBox 포트 포워딩 설정**

Windows에서 Ubuntu의 MySQL 서버에 접속하기 위한 과정입니다.

VirtualBox에서 Ubuntu 가상머신을 종료한 후 다음 메뉴로 이동합니다.

**VirtualBox → Ubuntu 가상머신 선택 → 설정 → 네트워크 → 어댑터 1**

네트워크 연결 방식이 `NAT`인지 확인한 후, **고급 → 포트 포워딩**을 선택합니다.

다음 규칙을 추가합니다.

| 항목     | 설정값         |
| ------ | ----------- |
| 이름     | MySQL       |
| 프로토콜   | TCP         |
| 호스트 IP | `127.0.0.1` |
| 호스트 포트 | `13306`     |
| 게스트 IP | 비워 둠        |
| 게스트 포트 | `3306`      |

핵심 포트 전달 구조

Windows

13306

Ubuntu

3306

MySQL

3306

Windows의 `13306` 포트를 사용하는 이유는 Windows에 별도로 MySQL이나 MariaDB가 설치되어 있더라도 기본 포트 `3306`과 충돌하지 않게 하기 위해서입니다.

설정을 저장한 다음 Ubuntu를 다시 실행하고, 컨테이너가 실행 중인지 `sudo docker ps`로 확인합니다.

## **5. Windows HeidiSQL에서 접속**

Windows에서 HeidiSQL을 실행한 후 \*\*새 세션(New)\*\*을 생성합니다.

**HeidiSQL 접속 설정**

| 네트워크 유형   | MariaDB or MySQL (TCP/IP) |
| --------- | ------------------------- |
| 호스트명 / IP | `127.0.0.1`               |
| 사용자       | `labuser`                 |
| 암호        | `Lab1234!`                |
| 포트        | `13306`                   |
| 데이터베이스    | `labdb` (선택 사항)           |

**[열기]** 버튼을 클릭하여 접속합니다.

접속에 성공하면 HeidiSQL 왼쪽 데이터베이스 목록에서 `labdb`를 확인할 수 있습니다.

## **6. HeidiSQL에서 DB 서비스 동작 확인**

HeidiSQL의 쿼리 탭에서 아래 SQL을 실행합니다.

### **① 테이블 생성**

```
USE labdb;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    score INT
);
```

### **② 데이터 입력**

```
INSERT INTO students (name, score)
VALUES
('홍길동', 90),
('김철수', 85),
('이영희', 95);
```

### **③ 데이터 조회**

```
SELECT * FROM students;
```

예상 결과:

| id | name | score |
| -- | ---- | ----- |
| 1  | 홍길동  | 90    |
| 2  | 김철수  | 85    |
| 3  | 이영희  | 95    |

이 결과가 출력되면 **Windows의 HeidiSQL → VirtualBox Ubuntu → Docker MySQL 컨테이너 → 데이터베이스**로 이어지는 서비스가 정상적으로 작동한 것입니다.

## **7. Docker 컨테이너의 장점 확인**

이번에는 컨테이너를 종료한 뒤 다시 실행하여 서비스가 복구되는지 확인합니다.

### **① 컨테이너 종료**

```
sudo docker stop mysql-lab
```

이 상태에서 HeidiSQL로 다시 접속하면 연결에 실패합니다. 이미 열려 있던 접속은 끊어질 수 있습니다.

### **② 컨테이너 재시작**

```
sudo docker start mysql-lab
```

MySQL의 초기화가 끝나면 HeidiSQL에서 다시 접속합니다.

```
SELECT * FROM labdb.students;
```

기존에 입력한 학생 데이터가 그대로 조회됩니다.

### **③ 컨테이너 삭제 후 재생성 (선택 실습)**

데이터 영속성을 더 명확하게 확인하려면 컨테이너를 삭제합니다.

```
sudo docker stop mysql-lab
sudo docker rm mysql-lab
```

그다음 3장의 `docker run` 명령어를 다시 실행합니다. 동일한 `mysql_lab_data` 볼륨을 사용하므로 기존 DB 데이터가 유지됩니다.

이 실습을 통해 **컨테이너의 생명주기와 데이터의 생명주기가 분리되어 있다**는 Docker의 중요한 특징을 확인할 수 있습니다.

## **8. 자주 발생하는 오류**

| 증상                          | 원인과 해결 방법                 |
| --------------------------- | ------------------------- |
| `docker: command not found` | Docker 설치 여부 확인           |
| `permission denied`         | 명령 앞에 `sudo` 추가           |
| HeidiSQL 연결 실패              | NAT 포트 포워딩 및 컨테이너 실행 확인   |
| `Access denied for user`    | 사용자명 및 비밀번호 확인            |
| `port is already allocated` | Ubuntu에서 3306 포트 사용 여부 확인 |
| 최초 접속이 느림                   | MySQL 초기화가 끝날 때까지 로그 확인   |

MySQL 로그 확인:

```
sudo docker logs mysql-lab
```

MySQL의 `ready for connections` 메시지를 확인하면 됩니다.

## **9. 실습 평가 체크리스트**

**실습 완료 현황**

0 / 7

Ubuntu에서 Docker 설치 및 실행 성공

MySQL 8.4 이미지 다운로드 성공

MySQL 컨테이너 실행 성공

VirtualBox NAT 포트 포워딩 설정 완료

Windows HeidiSQL 접속 성공

학생 테이블 생성·입력·조회 성공

컨테이너 재시작 후 기존 데이터 확인

## **10. 강의 마무리 — 핵심 개념 정리**

이번 실습으로 다음 관계를 이해하면 충분합니다.

| 핵심 개념            | 이번 실습에서의 역할              |
| ---------------- | ------------------------ |
| VirtualBox       | Ubuntu 가상머신을 실행          |
| Ubuntu           | Docker가 실행되는 호스트 OS      |
| Docker Image     | MySQL 서버 실행용 템플릿         |
| Docker Container | 실제 실행 중인 MySQL 서버        |
| Port Mapping     | 컨테이너의 서비스를 외부에 연결        |
| Docker Volume    | 컨테이너와 별도로 DB 데이터 보존      |
| HeidiSQL         | Windows에서 DB를 관리하는 클라이언트 |

**강의의 핵심 메시지:** Ubuntu에 MySQL 서버를 직접 설치하지 않아도 Docker 이미지 하나로 DB 서버를 실행하고, 외부 클라이언트에 데이터베이스 서비스를 제공할 수 있습니다.

이번 구성은 로컬 교육 실습 전용입니다. 실제 운영 시에는 예시 비밀번호 대신 안전한 비밀정보 관리 방식을 사용하고, DB 포트 노출 범위와 방화벽을 별도로 설정해야 합니다.

참고: [MySQL Docker 공식 이미지](https://hub.docker.com/_/mysql?utm_source=chatgpt.com) · [VirtualBox 네트워크 공식 문서](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/networkingdetails.html?utm_source=chatgpt.com)
