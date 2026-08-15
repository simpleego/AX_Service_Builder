import socket

HOST = "127.0.0.1"
PORT = 6000

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

message = "Hello UDP"

client.sendto(
    message.encode(),
    (HOST, PORT)
)

data, addr = client.recvfrom(1024)

print("Server 응답:", data.decode())

client.close()
