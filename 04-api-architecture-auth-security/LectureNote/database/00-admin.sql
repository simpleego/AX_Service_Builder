-- MySQL 관리자 계정에서 실행한다. MySQL 8.0 이상, InnoDB, UTF-8을 사용한다.
CREATE DATABASE IF NOT EXISTS todo_course CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
-- 비밀번호를 먼저 수정한다. 앱에서 root를 사용하지 않는다.
CREATE USER IF NOT EXISTS 'todo_app'@'localhost' IDENTIFIED BY 'ReplaceWithYourDatabasePassword';
-- CREATE USER IF NOT EXISTS는 기존 비밀번호를 변경하지 않는다. 변경 시 ALTER USER를 사용한다.
GRANT SELECT, INSERT, UPDATE, DELETE ON todo_course.* TO 'todo_app'@'localhost';
-- 원격 앱 서버는 localhost 대신 실제 앱 호스트로 제한한 별도 계정을 만든다.
