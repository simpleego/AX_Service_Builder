
"""
Day 5 - FastAPI 연동용 main.py
실행: uvicorn app.main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db, engine
from app import crud, schemas
from day3_models_complete import Base

# 테이블 자동생성 (개발용, 운영은 alembic 사용)
# Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Shop Mall API", version="1.0", description="AI캠퍼스 광주 풀스택 - 도메인 모델링 & 데이터 아키텍처")

@app.get("/", tags=["Health"])
def health():
    return {"status":"ok", "message":"Mini Shop API running"}

@app.get("/health/db", tags=["Health"])
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"db":"connected"}

# --- Product ---
@app.get("/products", response_model=list[schemas.ProductResponse], tags=["Products"])
def list_products(
    category_id: int = None,
    min_price: int = Query(None, ge=0),
    max_price: int = Query(None, ge=0),
    keyword: str = None,
    cursor: int = Query(None, description="커서 페이징: 마지막 id"),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """
    Day4 핵심쿼리 1번 + Day5 커서 페이징
    - keyword LIKE 검색은 Full-Text 인덱스로 개선 가능
    """
    return crud.get_products(db, category_id, min_price, max_price, keyword, cursor, limit)

# --- Cart ---
@app.post("/carts/{user_id}/items", tags=["Cart"])
def add_cart_item(user_id:int, payload: schemas.CartItemCreate, db: Session = Depends(get_db)):
    try:
        cart = crud.add_to_cart(db, user_id, payload.product_id, payload.quantity)
        return {"cart_id": cart.id, "message":"added"}
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/carts/{user_id}", tags=["Cart"])
def get_cart(user_id:int, db: Session = Depends(get_db)):
    cart = crud.get_or_create_cart(db, user_id)
    # 합계 계산 - Day4 쿼리 2번
    total = sum(item.product.price * item.quantity for item in cart.items) if hasattr(cart, 'items') else 0
    return {"cart_id": cart.id, "items": [{"product_id": i.product_id, "product_name": i.product.name if i.product else "", "quantity": i.quantity} for i in cart.items], "total_amount": total}

# --- Order ---
@app.post("/orders", response_model=schemas.OrderResponse, tags=["Orders"])
def create_order(payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Day4 핵심쿼리 3번: 트랜잭션 + FOR UPDATE로 재고 동시성 제어
    """
    try:
        order = crud.create_order_from_cart(db, payload.user_id)
        return order
    except ValueError as ve:
        raise HTTPException(400, str(ve))
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"주문 생성 실패: {e}")

@app.get("/orders/{user_id}", response_model=list[schemas.OrderResponse], tags=["Orders"])
def list_orders(user_id:int, db: Session = Depends(get_db)):
    from day3_models_complete import Order
    return db.query(Order).filter(Order.user_id==user_id).order_by(Order.created_at.desc()).limit(20).all()

# --- Best Seller (Day4 쿼리 5번) ---
@app.get("/stats/best-sellers", tags=["Stats"])
def best_sellers(db: Session = Depends(get_db)):
    sql = text("""
    SELECT p.id, p.name, SUM(oi.quantity) as sold_qty
    FROM order_items oi
    JOIN products p ON p.id = oi.product_id
    JOIN orders o ON o.id = oi.order_id
    WHERE o.status != 'CANCELLED'
    GROUP BY p.id ORDER BY sold_qty DESC LIMIT 10
    """)
    rows = db.execute(sql).mappings().all()
    return list(rows)

# --- Alembic Info ---
@app.get("/admin/alembic/current", tags=["Admin"])
def alembic_current(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT version_num FROM alembic_version"))
        return {"current_version": result.scalar()}
    except Exception as e:
        return {"current_version": None, "msg": "alembic_version 테이블 없음 - 아직 migrate 안함", "error": str(e)}
