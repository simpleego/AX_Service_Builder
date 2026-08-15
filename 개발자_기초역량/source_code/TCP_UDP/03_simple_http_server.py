import socket

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))
server.listen()

print("HTTP Server 실행")
print(f"http://{HOST}:{PORT}")

while True:
    conn, addr = server.accept()

    request = conn.recv(4096).decode()

    print("\n===== HTTP Request =====")
    print(request)

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

    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body.encode())}\r\n"
        "\r\n"
        + body
    )

    conn.sendall(response.encode())
    conn.close()
