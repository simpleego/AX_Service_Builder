
# Day 3-5 - seed_faker_100k.py
# pip install sqlalchemy pymysql faker tqdm
# python seed_faker_100k.py --total 100000
import argparse, random, string
from datetime import datetime, timedelta
from faker import Faker
from tqdm import tqdm
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# 교강사용 정답 모델 import (스타터 쓰면 User, Product만)
from day3_models_complete import Base, User, Category, Product, ProductCategory, Cart, CartItem, Order, OrderItem, OrderStatus

fake = Faker("ko_KR")
# MySQL 예시 - 본인 환경에 맞게 수정
DATABASE_URL = "mysql+pymysql://root:1234@localhost/mini_shop?charset=utf8mb4"

def random_slug(name, idx):
    return f"{name.lower().replace(' ','-')}-{idx}"[:200]

def create_categories(session: Session):
    print("Seeding categories...")
    roots = ["상의","하의","아우터","신발","액세서리","디지털"]
    cats = []
    for r in roots:
        c = Category(name=r, depth=0)
        session.add(c); cats.append(c)
    session.flush()
    # 2depth
    sub_map = {
        "상의":["티셔츠","셔츠","맨투맨","후드"], "하의":["청바지","슬랙스","조거"],
        "아우터":["패딩","코트","자켓"], "신발":["운동화","구두","샌들"],
        "액세서리":["가방","모자","벨트"], "디지털":["마우스","키보드","모니터"]
    }
    sub_cats=[]
    for root in cats:
        for sub in sub_map.get(root.name, []):
            sc = Category(name=sub, parent_id=root.id, depth=1)
            session.add(sc); sub_cats.append(sc)
    session.commit()
    return cats + sub_cats

def seed_users(session: Session, n=5000):
    print(f"Seeding {n} users...")
    users=[]
    for i in tqdm(range(n)):
        u = User(email=f"user{i}_{fake.user_name()}@test.com", password_hash="hashed", name=fake.name(), phone=fake.phone_number()[:20])
        users.append(u)
        if len(users)>=1000:
            session.bulk_save_objects(users); session.commit(); users=[]
    if users: session.bulk_save_objects(users); session.commit()

def seed_products(session: Session, total=100000, batch=2000):
    print(f"Seeding {total} products...")
    categories = session.query(Category).filter(Category.depth==1).all()
    cat_ids = [c.id for c in categories]
    if not cat_ids:
        print("No categories found! run create_categories first")
        return
    adjs = ["프리미엄","베이직","오버핏","슬림","워싱","빈티지","테크","에센셜","코튼","울"]
    nouns = ["티셔츠","청바지","후드","자켓","스니커즈","가방","모자","키보드","마우스","모니터","패딩","셔츠"]
    count=0
    while count < total:
        cur_batch = min(batch, total-count)
        objs=[]
        for i in range(cur_batch):
            name = f"{random.choice(adjs)} {random.choice(nouns)} {fake.word()}"
            price = random.choice([9900,12900,19900,29900,39900,49900,89000,129000])
            stock = random.randint(0,500)
            p = Product(name=name[:200], slug=random_slug(name, count+i), price=price, compare_price=price+random.randint(0,20000), stock=stock, review_count=random.randint(0,200), review_avg=round(random.uniform(3.5,5.0),2), is_active=True)
            objs.append(p)
        session.bulk_save_objects(objs); session.commit()
        # product_categories 매핑
        # 최근 batch의 product id 가져오기
        last_products = session.query(Product).order_by(Product.id.desc()).limit(cur_batch).all()
        mappings=[]
        for p in last_products:
            # 상품당 1~2개 카테고리
            for cid in random.sample(cat_ids, k=random.randint(1,2)):
                mappings.append(ProductCategory(product_id=p.id, category_id=cid))
        session.bulk_save_objects(mappings); session.commit()
        count+=cur_batch
        print(f"  -> {count}/{total}")

def seed_orders(session: Session, n_orders=20000):
    print(f"Seeding {n_orders} orders + order_items...")
    users = [u.id for u in session.query(User.id).limit(5000).all()]
    products = session.query(Product).filter(Product.stock>0).limit(5000).all()
    if not users or not products:
        print("Need users/products first")
        return
    for i in tqdm(range(n_orders)):
        user_id = random.choice(users)
        order_no = f"ORD-{datetime.now().strftime('%Y%m%d')}-{i:06d}"
        # 1~4개 아이템
        chosen = random.sample(products, k=random.randint(1,4))
        total=0
        items=[]
        for prod in chosen:
            qty = random.randint(1,3)
            subtotal = prod.price * qty
            total+=subtotal
            items.append(OrderItem(product_id=prod.id, product_name=prod.name, unit_price=prod.price, quantity=qty, subtotal=subtotal))
        discount = random.choice([0,0,0,1000,3000,5000])
        order = Order(order_no=order_no, user_id=user_id, status=random.choice(list(OrderStatus)), total_amount=total, discount_amount=discount, final_amount=total-discount, created_at=fake.date_time_between(start_date="-90d", end_date="now"))
        session.add(order); session.flush()
        for it in items: it.order_id = order.id; session.add(it)
        if i % 1000 == 0:
            session.commit()
    session.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--total", type=int, default=10000, help="총 상품 수")
    parser.add_argument("--users", type=int, default=5000)
    parser.add_argument("--orders", type=int, default=0, help="주문 생성 수 (0이면 skip)")
    parser.add_argument("--reset", action="store_true", help="드랍 후 재생성")
    args = parser.parse_args()

    engine = create_engine(DATABASE_URL, echo=False)
    if args.reset:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print("Reset DB done")
    
    with Session(engine) as session:
        if session.query(Category).count()==0:
            create_categories(session)
        if session.query(User).count()==0:
            seed_users(session, n=args.users)
        seed_products(session, total=args.total)
        if args.orders>0:
            seed_orders(session, n_orders=args.orders)
    print("Done!")
