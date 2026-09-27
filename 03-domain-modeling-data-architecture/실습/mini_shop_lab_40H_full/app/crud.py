
from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy import select, func
from day3_models_complete import Product, Cart, CartItem, Order, OrderItem, User, OrderStatus
import random, datetime

def get_products(db: Session, category_id: int=None, min_price:int=None, max_price:int=None, keyword:str=None, cursor:int=None, limit:int=20):
    q = select(Product).where(Product.is_active==True)
    if keyword: q = q.where(Product.name.like(f"%{keyword}%"))
    if min_price: q = q.where(Product.price >= min_price)
    if max_price: q = q.where(Product.price <= max_price)
    if cursor: q = q.where(Product.id < cursor)  # 커서 페이징
    q = q.order_by(Product.id.desc()).limit(limit)
    return db.execute(q).scalars().all()

def get_or_create_cart(db: Session, user_id:int):
    cart = db.query(Cart).filter(Cart.user_id==user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart); db.commit(); db.refresh(cart)
    return cart

def add_to_cart(db: Session, user_id:int, product_id:int, quantity:int):
    cart = get_or_create_cart(db, user_id)
    item = db.query(CartItem).filter(CartItem.cart_id==cart.id, CartItem.product_id==product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.add(item)
    db.commit()
    return cart

def create_order_from_cart(db: Session, user_id:int):
    # 트랜잭션 + FOR UPDATE 예시
    cart = db.query(Cart).options(selectinload(Cart.items).selectinload(CartItem.product)).filter(Cart.user_id==user_id).first()
    if not cart or not cart.items:
        raise ValueError("장바구니가 비었습니다")

    # 재고 체크 (SELECT ... FOR UPDATE)
    product_ids = [i.product_id for i in cart.items]
    products = db.query(Product).filter(Product.id.in_(product_ids)).with_for_update().all()
    prod_map = {p.id:p for p in products}

    total=0
    order_items=[]
    for ci in cart.items:
        p = prod_map[ci.product_id]
        if p.stock < ci.quantity:
            raise ValueError(f"{p.name} 재고 부족 (남은: {p.stock})")
        p.stock -= ci.quantity
        subtotal = p.price * ci.quantity
        total+=subtotal
        order_items.append(OrderItem(product_id=p.id, product_name=p.name, unit_price=p.price, quantity=ci.quantity, subtotal=subtotal))

    order_no = f"ORD-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100000,999999)}"
    order = Order(order_no=order_no, user_id=user_id, status=OrderStatus.PENDING, total_amount=total, final_amount=total, items=order_items)
    db.add(order)
    # 장바구니 비우기
    db.query(CartItem).filter(CartItem.cart_id==cart.id).delete()
    db.commit()
    db.refresh(order)
    return order
