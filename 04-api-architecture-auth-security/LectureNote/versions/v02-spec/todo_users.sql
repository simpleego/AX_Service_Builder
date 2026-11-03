-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        11.4.13-MariaDB - MariaDB Server
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  12.21.0.7344
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- todo_course 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `todo_course` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
USE `todo_course`;

-- 테이블 todo_course.oauth_states 구조 내보내기
CREATE TABLE IF NOT EXISTS `oauth_states` (
  `state_hash` char(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  `binding_hash` char(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  `nonce` varchar(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  `verifier` varchar(128) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  `expires_at` datetime NOT NULL,
  PRIMARY KEY (`state_hash`),
  KEY `ix_oauth_expiry` (`expires_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 todo_course.oauth_states:~0 rows (대략적) 내보내기

-- 테이블 todo_course.refresh_tokens 구조 내보내기
CREATE TABLE IF NOT EXISTS `refresh_tokens` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `token_hash` char(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `family_id` char(36) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  `expires_at` datetime NOT NULL,
  `revoked_at` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_hash` (`token_hash`),
  KEY `fk_refresh_user` (`user_id`),
  KEY `ix_refresh_family` (`family_id`),
  KEY `ix_refresh_expiry` (`expires_at`),
  CONSTRAINT `fk_refresh_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 todo_course.refresh_tokens:~0 rows (대략적) 내보내기

-- 테이블 todo_course.social_accounts 구조 내보내기
CREATE TABLE IF NOT EXISTS `social_accounts` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `provider` varchar(30) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  `provider_subject` varchar(255) CHARACTER SET ascii COLLATE ascii_bin NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  `provider_email` varchar(254) DEFAULT NULL COMMENT '표시/참고용. 자동 계정 병합에 사용 금지',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_social_identity` (`provider`,`provider_subject`),
  KEY `fk_social_user` (`user_id`),
  CONSTRAINT `fk_social_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 todo_course.social_accounts:~0 rows (대략적) 내보내기

-- 테이블 todo_course.todos 구조 내보내기
CREATE TABLE IF NOT EXISTS `todos` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `owner_id` int(10) unsigned NOT NULL,
  `title` varchar(200) NOT NULL,
  `completed` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `ix_todo_owner_id` (`owner_id`,`id`),
  KEY `ix_todo_owner_completed` (`owner_id`,`completed`,`id`),
  CONSTRAINT `fk_todo_owner` FOREIGN KEY (`owner_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `ck_todo_title` CHECK (char_length(trim(`title`)) between 1 and 200),
  CONSTRAINT `ck_todo_completed` CHECK (`completed` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 todo_course.todos:~5 rows (대략적) 내보내기
INSERT INTO `todos` (`id`, `owner_id`, `title`, `completed`, `created_at`, `updated_at`) VALUES
	(1, 1, '자바 공부', 0, '2026-11-02 06:32:15', '2026-11-02 06:32:15'),
	(2, 1, 'Python 공부', 0, '2026-11-02 06:34:07', '2026-11-02 06:34:07'),
	(5, 1, '편지쓰기', 1, '2026-11-02 07:12:30', '2026-11-02 07:12:40'),
	(6, 1, '음악감상', 0, '2026-11-02 07:57:07', '2026-11-02 07:57:07'),
	(7, 1, '운동하기', 0, '2026-11-02 07:59:00', '2026-11-02 07:59:00');

-- 테이블 todo_course.users 구조 내보내기
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(254) DEFAULT NULL COMMENT '로컬 로그인 식별자. 소셜 전용 계정은 NULL',
  `password_hash` varchar(200) DEFAULT NULL COMMENT 'scrypt salt:hash. 평문 저장 금지',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 테이블 데이터 todo_course.users:~1 rows (대략적) 내보내기
INSERT INTO `users` (`id`, `email`, `password_hash`, `created_at`) VALUES
	(1, 'simple@example.com', NULL, '2026-11-02 04:41:47');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
