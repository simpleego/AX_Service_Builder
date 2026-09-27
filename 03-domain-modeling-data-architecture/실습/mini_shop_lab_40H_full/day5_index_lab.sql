
-- Day5 - 인덱스 & 성능 최적화 실습
-- 1. 인덱스 전/후 비교
EXPLAIN ANALYZE SELECT * FROM products WHERE is_active=1 AND price BETWEEN 20000 AND 40000;
CREATE INDEX idx_products_active_price ON products(is_active, price);
EXPLAIN ANALYZE SELECT * FROM products WHERE is_active=1 AND price BETWEEN 20000 AND 40000;

-- 2. 복합 인덱스 순서 실험
-- 카디널리티 높은 컬럼을 앞에?
CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);
EXPLAIN SELECT * FROM orders WHERE user_id=1 ORDER BY created_at DESC LIMIT 10;

-- 3. Covering Index
CREATE INDEX idx_products_cover ON products(is_active, category_id, price, id, name);
-- SELECT id, name 에서 테이블 접근 없이 인덱스만으로 해결

-- 4. Full-Text (MySQL)
ALTER TABLE products ADD FULLTEXT INDEX ft_name (name);
SELECT * FROM products WHERE MATCH(name) AGAINST('프리미엄 티셔츠' IN NATURAL LANGUAGE MODE);

-- PostgreSQL 버전
-- CREATE EXTENSION pg_trgm; CREATE INDEX trgm_idx ON products USING gin(name gin_trgm_ops);

-- 5. N+1 문제 확인용 Slow Query
SET GLOBAL slow_query_log=1; SET GLOBAL long_query_time=0.5;

-- 6. 주문 상태 로그용 인덱스
CREATE INDEX idx_order_status_logs_order_id ON order_status_logs(order_id, created_at);
