import socket
import random

HOST = "127.0.0.1"
PORT = 6002

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

server.bind((HOST, PORT))

print("UDP Loss Test Server")

while True:
    data, addr = server.recvfrom(1024)

    message = data.decode()

    # 30% 확률로 패킷 손실 시뮬레이션
    if random.random() < 0.3:
        print("DROP:", message)
        continue

    print("RECEIVE:", message)

    server.sendto(
        f"ACK {message}".encode(),
        addr
    )
