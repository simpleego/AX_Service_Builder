import socket

HOST = "127.0.0.1"
PORT = 6000

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

server.bind((HOST, PORT))

print(f"UDP Server: {HOST}:{PORT}")

while True:
    data, addr = server.recvfrom(1024)

    message = data.decode()
    print(f"{addr} → {message}")

    response = f"Echo: {message}"

    server.sendto(
        response.encode(),
        addr
    )
