-- =====================================================================
-- 쿠키 / 세션 인증 실습용 MySQL 스키마
-- 실행: mysql -u root -p < sql/schema.sql
-- (서버 시작 시 SQLAlchemy가 테이블을 자동 생성하므로 DB/계정만 만들어도 됩니다)
-- =====================================================================

CREATE DATABASE IF NOT EXISTS webauth_db
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

-- 실습 전용 계정 (비밀번호는 .env 의 DB_PASSWORD 와 맞추세요)
CREATE USER IF NOT EXISTS 'webauth'@'localhost' IDENTIFIED BY 'webauth1234';
CREATE USER IF NOT EXISTS 'webauth'@'%'         IDENTIFIED BY 'webauth1234';
GRANT ALL PRIVILEGES ON webauth_db.* TO 'webauth'@'localhost';
GRANT ALL PRIVILEGES ON webauth_db.* TO 'webauth'@'%';
FLUSH PRIVILEGES;

USE webauth_db;

-- 회원 테이블
CREATE TABLE IF NOT EXISTS users (
  id            INT          NOT NULL AUTO_INCREMENT,
  username      VARCHAR(50)  NOT NULL,
  email         VARCHAR(100) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,          -- bcrypt 해시 (평문 저장 금지)
  created_at    DATETIME     DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uq_users_username (username),
  UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB;

-- 서버 측 세션 저장소 (세션 인증 실습용)
CREATE TABLE IF NOT EXISTS login_sessions (
  session_id       VARCHAR(64)  NOT NULL,       -- 쿠키에 저장되는 랜덤 문자열
  user_id          INT          NOT NULL,
  created_at       DATETIME     NOT NULL,
  expires_at       DATETIME     NOT NULL,
  last_accessed_at DATETIME     NOT NULL,
  ip_address       VARCHAR(45)  NULL,
  user_agent       VARCHAR(255) NULL,
  PRIMARY KEY (session_id),
  KEY ix_login_sessions_user_id (user_id),
  KEY ix_login_sessions_expires_at (expires_at),
  CONSTRAINT fk_login_sessions_user
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- 수업 중 확인용 쿼리
-- ---------------------------------------------------------------------
-- SELECT id, username, LEFT(password_hash, 20) AS hash_prefix FROM users;
-- SELECT LEFT(session_id, 10) AS sid, user_id, created_at, expires_at, ip_address FROM login_sessions;
-- 관리자 강제 로그아웃:  DELETE FROM login_sessions WHERE user_id = 1;
