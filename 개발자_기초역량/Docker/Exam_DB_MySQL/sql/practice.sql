-- ============================================================
--  조회 실습 SQL  (Windows 클라이언트 또는 VM 에서 실행)
-- ============================================================
SET NAMES utf8mb4;
USE lab_db;

-- 1) 전체 회원
SELECT * FROM members;

-- 2) 조건 조회: 서울 회원
SELECT id, name, email FROM members WHERE city = '서울';

-- 3) JOIN: 누가 무엇을 샀나
SELECT m.name, o.product, o.price, o.qty, o.price * o.qty AS total
FROM orders o
JOIN members m ON m.id = o.member_id
ORDER BY total DESC;

-- 4) 집계: 회원별 주문 금액 합계
SELECT m.name, COUNT(o.id) AS order_count, SUM(o.price * o.qty) AS total_amount
FROM members m
LEFT JOIN orders o ON o.member_id = m.id
GROUP BY m.id, m.name
ORDER BY total_amount DESC;

-- 5) 서버 정보 확인: 지금 접속한 곳이 Docker 컨테이너인지 확인
SELECT VERSION() AS mysql_version, @@hostname AS container_id, CURRENT_USER() AS login_user, NOW() AS server_time;
