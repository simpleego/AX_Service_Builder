-- ============================================================
--  최초 실행 시 1회만 자동 실행됩니다 (MYSQL_DATABASE=lab_db 안에서 실행)
--  다시 실행하려면: docker compose down -v  후  docker compose up -d
-- ============================================================
SET NAMES utf8mb4;

-- 회원 테이블
CREATE TABLE members (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  name       VARCHAR(50)  NOT NULL,
  email      VARCHAR(100) NOT NULL UNIQUE,
  city       VARCHAR(30),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 주문 테이블 (members 와 1:N 관계)
CREATE TABLE orders (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  member_id  INT          NOT NULL,
  product    VARCHAR(100) NOT NULL,
  price      INT          NOT NULL,
  qty        INT          NOT NULL DEFAULT 1,
  ordered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (member_id) REFERENCES members(id)
);

INSERT INTO members (name, email, city) VALUES
  ('김도커', 'docker.kim@example.com', '서울'),
  ('이컨테', 'container.lee@example.com', '부산'),
  ('박이미', 'image.park@example.com', '서울'),
  ('최볼륨', 'volume.choi@example.com', '대전');

INSERT INTO orders (member_id, product, price, qty) VALUES
  (1, '무선 키보드', 45000, 1),
  (1, 'USB-C 허브',  32000, 2),
  (2, '27인치 모니터', 289000, 1),
  (3, '노트북 거치대', 25000, 1),
  (3, '무선 마우스',  19000, 3),
  (4, '외장 SSD 1TB', 129000, 1);
