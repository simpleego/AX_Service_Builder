import socket

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))
server.listen()

# Windows는 accept()가 막혀 있는 동안 Ctrl+C를 받지 못한다.
# 1초마다 accept()에서 빠져나오게 해서 Ctrl+C를 바로 처리할 수 있게 한다.
server.settimeout(1.0)

print(f"HTTP Server 실행 (종료: Ctrl+C)")
print(f"http://{HOST}:{PORT}")

body = """
<html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>Hello TCP</h1>
        <p>Python TCP Socket Web Server</p>
    </body>
</html>
"""

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

        request = conn.recv(4096).decode()

        print("\n===== HTTP Request =====")
        print(request)

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            f"Content-Length: {len(body.encode())}\r\n"
            "\r\n"
            + body
        )

        conn.sendall(response.encode())

        conn.close()

except KeyboardInterrupt:
    print("\n서버를 종료합니다.")

finally:
    server.close()
