"""
1:1 메시지 서버 (카톡처럼 지정된 상대와만 대화)

- 사용자마다 대화 상대가 PARTNERS에 미리 지정되어 있다.
- 상대가 접속 중이면 즉시 전달, 오프라인이면 보관했다가 접속 시 전달한다.
- 상대의 접속/퇴장을 알려준다.

프로토콜: JSON 한 줄 = 메시지 하나 (줄바꿈 '\n'으로 메시지 경계 구분)
  클라이언트 -> 서버
    {"type": "login", "user": "alice"}
    {"type": "msg", "text": "안녕"}
  서버 -> 클라이언트
    {"type": "welcome", "user", "peer", "peer_online", "queued"}
    {"type": "msg", "from", "text", "time", "offline"}
    {"type": "ack", "status": "delivered" | "queued", "time"}
    {"type": "presence", "user", "online"}
    {"type": "error", "message"}
"""

import json
import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5002

# 지정된 대화 상대 (사용자 -> 상대)
PARTNERS = {
    "alice": "bob",
    "bob": "alice",
}

online = {}    # user -> Session (접속 중인 사용자)
pending = {}   # user -> [msg, ...] (오프라인일 때 받은 메시지 보관)
lock = threading.Lock()


class Session:
    """소켓 하나와 전송 잠금을 묶는다. 여러 스레드가 같은 소켓에 동시에 쓰지 않도록."""

    def __init__(self, conn):
        self.conn = conn
        self.send_lock = threading.Lock()

    def send(self, obj):
        data = (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8")
        with self.send_lock:
            self.conn.sendall(data)


def now():
    return datetime.now().strftime("%H:%M")


def notify_presence(user, peer, is_online):
    with lock:
        peer_session = online.get(peer)
    if peer_session:
        try:
            peer_session.send({"type": "presence", "user": user, "online": is_online})
        except OSError:
            pass


def handle_client(conn, addr):
    session = Session(conn)
    reader = conn.makefile("r", encoding="utf-8", newline="\n")
    user = None

    try:
        # 1) 로그인
        line = reader.readline()
        if not line:
            return
        login = json.loads(line)
        user = login.get("user")

        if login.get("type") != "login" or user not in PARTNERS:
            session.send({"type": "error", "message": f"등록되지 않은 사용자: {user}"})
            user = None
            return

        peer = PARTNERS[user]

        with lock:
            if user in online:
                session.send({"type": "error", "message": f"{user}는 이미 접속 중입니다."})
                user = None
                return
            online[user] = session
            queued = pending.pop(user, [])
            peer_online = peer in online

        print(f"[접속] {user} {addr}")

        session.send({
            "type": "welcome",
            "user": user,
            "peer": peer,
            "peer_online": peer_online,
            "queued": len(queued),
        })

        # 오프라인 동안 쌓인 메시지 전달
        for msg in queued:
            session.send(msg)

        notify_presence(user, peer, True)

        # 2) 메시지 중계
        for line in reader:
            try:
                packet = json.loads(line)
            except json.JSONDecodeError:
                continue

            if packet.get("type") != "msg":
                continue

            text = str(packet.get("text", "")).strip()
            if not text:
                continue

            out = {"type": "msg", "from": user, "text": text, "time": now(), "offline": False}

            with lock:
                peer_session = online.get(peer)

            status = "queued"
            if peer_session:
                try:
                    peer_session.send(out)
                    status = "delivered"
                except OSError:
                    pass

            if status == "queued":
                with lock:
                    pending.setdefault(peer, []).append({**out, "offline": True})

            print(f"[{out['time']}] {user} -> {peer} ({status}): {text}")
            session.send({"type": "ack", "status": status, "time": out["time"]})

    except (ConnectionError, OSError, json.JSONDecodeError):
        pass

    finally:
        if user:
            with lock:
                if online.get(user) is session:
                    del online[user]
            print(f"[종료] {user} {addr}")
            notify_presence(user, PARTNERS[user], False)
        reader.close()
        conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    # Windows는 accept()가 막혀 있는 동안 Ctrl+C를 받지 못한다.
    # 1초마다 accept()에서 빠져나오게 해서 Ctrl+C를 바로 처리할 수 있게 한다.
    server.settimeout(1.0)

    print(f"DM Server: {HOST}:{PORT} (종료: Ctrl+C)")
    print("등록된 사용자:", ", ".join(f"{u} <-> {p}" for u, p in PARTNERS.items() if u < p))

    try:
        while True:
            try:
                conn, addr = server.accept()
            except socket.timeout:
                conn = None  # 1초 동안 접속 없음
            # continue는 except 밖에 둔다. except 안에서 continue하는 순간에
            # Ctrl+C가 들어오면 Python 3.12에서 바깥 try가 잡지 못한다.
            if conn is None:
                continue
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
