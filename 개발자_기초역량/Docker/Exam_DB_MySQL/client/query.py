"""
Windows(로컬 PC)에서 Docker MySQL 에 접속해 조회하는 예제

  경로: Windows 127.0.0.1:13306 --(VirtualBox NAT)--> VM 3306 --(docker -p)--> 컨테이너 3306

준비:  pip install -r requirements.txt
실행:  python query.py
"""
import os
import pymysql

CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "13306")),
    "user": os.getenv("DB_USER", "lab_user"),
    "password": os.getenv("DB_PASSWORD", "labpass1234"),
    "database": os.getenv("DB_NAME", "lab_db"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "connect_timeout": 5,
}


def show(title, rows):
    print(f"\n=== {title} ===")
    if not rows:
        print("(결과 없음)")
        return
    cols = list(rows[0].keys())
    print(" | ".join(cols))
    print("-" * 60)
    for r in rows:
        print(" | ".join(str(r[c]) for c in cols))


def main():
    print(f"접속 시도: {CONFIG['user']}@{CONFIG['host']}:{CONFIG['port']}/{CONFIG['database']}")
    conn = pymysql.connect(**CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT VERSION() AS version, @@hostname AS container_id, NOW() AS server_time")
            show("서버 정보 (container_id = Docker 컨테이너 ID)", cur.fetchall())

            cur.execute("SELECT * FROM members")
            show("전체 회원", cur.fetchall())

            # 파라미터 바인딩(%s) - SQL Injection 방지
            cur.execute("SELECT id, name, email FROM members WHERE city = %s", ("서울",))
            show("서울 회원", cur.fetchall())

            cur.execute("""
                SELECT m.name, COUNT(o.id) AS order_count, SUM(o.price * o.qty) AS total_amount
                FROM members m LEFT JOIN orders o ON o.member_id = m.id
                GROUP BY m.id, m.name ORDER BY total_amount DESC
            """)
            show("회원별 주문 합계", cur.fetchall())
    finally:
        conn.close()
    print("\n접속/조회 성공!")


if __name__ == "__main__":
    main()
