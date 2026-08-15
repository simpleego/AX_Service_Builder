import socket

HOST = "127.0.0.1"
PORT = 5000

client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client_socket.connect((HOST, PORT))

message = "Hello TCP Server"

client_socket.sendall(message.encode())

data = client_socket.recv(1024)

print("Server 응답:", data.decode())

client_socket.close()
