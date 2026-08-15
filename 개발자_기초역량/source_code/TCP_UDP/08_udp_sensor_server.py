import socket

HOST = "127.0.0.1"
PORT = 6001

server = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

server.bind((HOST, PORT))

print("Sensor Server 실행")

while True:
    data, addr = server.recvfrom(1024)
    print("센서 데이터:", data.decode())
