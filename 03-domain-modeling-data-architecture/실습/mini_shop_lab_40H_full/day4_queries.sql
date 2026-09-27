
-- Day4 - 쇼핑몰 핵심 쿼리 8선 (교강사용)
-- 1. 상품 검색 + 필터 (카테고리, 가격, 키워드, 페이징)
SELECT p.id, p.name, p.price, p.review_avg
FROM products p
JOIN product_categories pc ON pc.product_id = p.id
WHERE p.is_active = 1
  AND pc.category_id = 2
  AND p.price BETWEEN 10000 AND 50000
  AND p.name LIKE '%티셔츠%'
ORDER BY p.created_at DESC
LIMIT 20 OFFSET 0;

-- 커서 기반 페이징 (성능 Good)
SELECT p.id, p.name, p.price
FROM products p
WHERE p.is_active = 1 AND p.id < 50000
ORDER BY p.id DESC LIMIT 20;

-- 2. 장바구니 합계
SELECT c.user_id, SUM(ci.quantity * p.price) as total
FROM carts c
JOIN cart_items ci ON ci.cart_id = c.id
JOIN products p ON p.id = ci.product_id
WHERE c.user_id = 1
GROUP BY c.user_id;

-- 3. 주문 생성 시 재고 차감 (트랜잭션 + FOR UPDATE)
START TRANSACTION;
SELECT stock FROM products WHERE id IN (10,20) FOR UPDATE;
-- app에서 stock 체크 후
UPDATE products SET stock = stock - 1 WHERE id = 10 AND stock >= 1;
INSERT INTO orders (order_no, user_id, total_amount, final_amount) VALUES (...);
INSERT INTO order_items ...;
COMMIT;

-- 4. 내 주문 목록 + 주문 상세
SELECT o.order_no, o.status, o.final_amount, o.created_at,
       (SELECT COUNT(*) FROM order_items oi WHERE oi.order_id = o.id) as item_cnt
FROM orders o
WHERE o.user_id = 1
ORDER BY o.created_at DESC LIMIT 10;

SELECT oi.product_name, oi.unit_price, oi.quantity, oi.subtotal
FROM order_items oi
WHERE oi.order_id = 123;

-- 5. 베스트셀러 TOP 10
SELECT p.id, p.name, SUM(oi.quantity) as sold_qty, SUM(oi.subtotal) as revenue
FROM order_items oi
JOIN products p ON p.id = oi.product_id
JOIN orders o ON o.id = oi.order_id
WHERE o.status IN ('PAID','PREPARING','SHIPPED','DELIVERED')
  AND o.created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY p.id
ORDER BY sold_qty DESC LIMIT 10;

-- 6. 리뷰 평점 집계 (반정규화 갱신)
SELECT product_id, COUNT(*) as cnt, AVG(rating) as avg_rating
FROM reviews GROUP BY product_id;

UPDATE products p
JOIN (SELECT product_id, COUNT(*) as cnt, AVG(rating) as avg_rating FROM reviews GROUP BY product_id) r
ON r.product_id = p.id
SET p.review_count = r.cnt, p.review_avg = r.avg_rating;

-- 7. 쿠폰 적용 가능 검증
SELECT * FROM coupons
WHERE code = 'WELCOME10' AND is_active=1 AND expires_at > NOW() AND total_used < total_issued;

-- 8. 월별 매출 통계
SELECT DATE_FORMAT(o.created_at, '%Y-%m') as ym,
       COUNT(*) as order_cnt,
       SUM(o.final_amount) as sales
FROM orders o
WHERE o.status != 'CANCELLED'
GROUP BY ym ORDER BY ym;

-- Window Function: 카테고리별 가격 랭킹
SELECT p.name, p.price, pc.category_id,
       RANK() OVER (PARTITION BY pc.category_id ORDER BY p.price DESC) as price_rank
FROM products p JOIN product_categories pc ON pc.product_id = p.id;
