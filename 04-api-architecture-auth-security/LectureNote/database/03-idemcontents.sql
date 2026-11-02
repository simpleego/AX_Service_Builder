-- 기존 00-admin.sql, 01-schema.sql 다음에 관리자 계정으로 한 번 실행한다.
USE todo_course;
CREATE TABLE IF NOT EXISTS idempotency_records (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id INT UNSIGNED NOT NULL,
  operation VARCHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  key_hash CHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  request_hash CHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  response_body MEDIUMTEXT NOT NULL COMMENT '최초 성공 JSON 응답 스냅샷',
  status_code SMALLINT UNSIGNED NOT NULL,
  location VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_idempotency_scope UNIQUE (user_id,operation,key_hash),
  CONSTRAINT fk_idempotency_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;
-- 기존 todo_app의 todo_course.* DML 권한이 이 테이블에도 적용된다.
-- 수업 정책: 키 기록에 TTL을 두지 않는다. 임의 삭제하면 과거 요청의 중복 생성 방지 보장이 끝난다.
