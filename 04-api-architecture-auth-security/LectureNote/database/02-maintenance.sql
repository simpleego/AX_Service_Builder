USE todo_course;
-- 만료 state는 정기 삭제한다. 회전된 토큰은 원래 만료까지 보관해야 재사용을 탐지할 수 있다.
DELETE FROM oauth_states WHERE expires_at < UTC_TIMESTAMP();
DELETE FROM refresh_tokens WHERE expires_at < DATE_SUB(UTC_TIMESTAMP(), INTERVAL 1 DAY);
-- 이 파일은 선택 작업이다. 이벤트 스케줄러/운영 배치로 주기 실행할 수 있다.
