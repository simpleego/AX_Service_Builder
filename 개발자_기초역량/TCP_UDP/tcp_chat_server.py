import socket
import threading

HOST = "127.0.0.1"
PORT = 5001

clients = []

def handle_client(conn, addr):

    print("접속:", addr)

    while True:
        try:
            data = conn.recv(1024)

            if not data:
                break

            message = data.decode()

            print(addr, message)

            for client in clients:
                if client != conn:
                    client.sendall(
                        f"{addr}: {message}".encode()
                    )

        except:
            break

    clients.remove(conn)

    conn.close()

    print("종료:", addr)


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))
server.listen()

# Windows는 accept()가 막혀 있는 동안 Ctrl+C를 받지 못한다.
# 1초마다 accept()에서 빠져나오게 해서 Ctrl+C를 바로 처리할 수 있게 한다.
server.settimeout(1.0)

print(f"Chat Server: {HOST}:{PORT} (종료: Ctrl+C)")

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

        clients.append(conn)

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr),
            daemon=True
        )

        thread.start()

except KeyboardInterrupt:
    print("\n서버를 종료합니다.")

finally:
    server.close()