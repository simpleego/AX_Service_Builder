-- 관리자/마이그레이션 계정으로 한 번 실행한다. 기존 테이블을 삭제하지 않는다.
USE todo_course;
SET time_zone = '+00:00';

CREATE TABLE IF NOT EXISTS users (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(254) NULL UNIQUE COMMENT '로컬 로그인 식별자. 소셜 전용 계정은 NULL',
  password_hash VARCHAR(200) NULL COMMENT 'scrypt salt:hash. 평문 저장 금지',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS todos (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  owner_id INT UNSIGNED NOT NULL,
  title VARCHAR(200) NOT NULL,
  completed BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_todo_owner FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
  CONSTRAINT ck_todo_title CHECK (CHAR_LENGTH(TRIM(title)) BETWEEN 1 AND 200),
  CONSTRAINT ck_todo_completed CHECK (completed IN (0,1)),
  INDEX ix_todo_owner_id (owner_id,id),
  INDEX ix_todo_owner_completed (owner_id,completed,id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS refresh_tokens (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  token_hash CHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL UNIQUE,
  user_id INT UNSIGNED NOT NULL,
  family_id CHAR(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  expires_at DATETIME NOT NULL,
  revoked_at DATETIME NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_refresh_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX ix_refresh_family (family_id), INDEX ix_refresh_expiry (expires_at)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS social_accounts (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  provider VARCHAR(30) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  provider_subject VARCHAR(255) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  user_id INT UNSIGNED NOT NULL,
  provider_email VARCHAR(254) NULL COMMENT '표시/참고용. 자동 계정 병합에 사용 금지',
  CONSTRAINT uq_social_identity UNIQUE (provider,provider_subject),
  CONSTRAINT fk_social_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS oauth_states (
  state_hash CHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL PRIMARY KEY,
  binding_hash CHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  nonce VARCHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  verifier VARCHAR(128) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  expires_at DATETIME NOT NULL,
  INDEX ix_oauth_expiry (expires_at)
) ENGINE=InnoDB;

-- v01~v02만 사용하는 로그인 불가 공용 사용자. 중복 실행으로 실제 사용자를 수정하지 않는다.
INSERT IGNORE INTO users(id,email,password_hash) VALUES(1,'classroom@example.invalid',NULL);
