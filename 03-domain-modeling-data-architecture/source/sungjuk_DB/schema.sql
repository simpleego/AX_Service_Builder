-- HeidiSQL 또는 MariaDB 클라이언트에서 관리자 계정으로 실행하세요.
-- 기존 자료는 삭제하지 않습니다.
CREATE DATABASE IF NOT EXISTS sungjuk_db
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sungjuk_db;

CREATE TABLE IF NOT EXISTS students (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    department VARCHAR(50) NOT NULL,
    korean TINYINT UNSIGNED NOT NULL DEFAULT 0 CHECK (korean <= 100),
    english TINYINT UNSIGNED NOT NULL DEFAULT 0 CHECK (english <= 100),
    math TINYINT UNSIGNED NOT NULL DEFAULT 0 CHECK (math <= 100)
) ENGINE=InnoDB;

-- 총점, 평균, 학점 컬럼은 만들지 않습니다. Python에서 계산합니다.
-- 별도의 앱 전용 계정 생성 예시: 비밀번호를 변경하고 아래 주석을 해제하세요.
-- CREATE USER IF NOT EXISTS 'sungjuk_app'@'127.0.0.1' IDENTIFIED BY 'CHANGE_ME';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON sungjuk_db.* TO 'sungjuk_app'@'127.0.0.1';
