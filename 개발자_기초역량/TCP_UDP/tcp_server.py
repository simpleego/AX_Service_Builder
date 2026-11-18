import socket

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server_socket.bind((HOST, PORT))
server_socket.listen()

# Windows는 accept()가 막혀 있는 동안 Ctrl+C를 받지 못한다.
# 1초마다 accept()에서 빠져나오게 해서 Ctrl+C를 바로 처리할 수 있게 한다.
server_socket.settimeout(1.0)

print(f"TCP Server 실행: {HOST}:{PORT} (종료: Ctrl+C)")

try:
    conn = None
    while conn is None:  # 클라이언트 1명이 접속할 때까지 대기
        try:
            conn, addr = server_socket.accept()
        except socket.timeout:
            pass  # 1초 동안 접속 없음 → 다시 대기 (이 사이에 Ctrl+C 확인)
            # except 안에서 continue를 쓰지 않는다. 그 순간에 Ctrl+C가 들어오면
            # Python 3.12에서 바깥 try가 잡지 못한다.

    print("Client 연결:", addr)

    data = conn.recv(1024)

    message = data.decode()
    print("받은 데이터:", message)

    response = f"Echo: {message}"

    conn.sendall(response.encode())

    conn.close()

except KeyboardInterrupt:
    print("\n서버를 종료합니다.")

finally:
    server_socket.close()
