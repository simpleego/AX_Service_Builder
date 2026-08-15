import socket

HOST = "127.0.0.1"
PORT = 5000

server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"TCP Server 실행: {HOST}:{PORT}")

conn, addr = server_socket.accept()

print("Client 연결:", addr)

data = conn.recv(1024)

message = data.decode()
print("받은 데이터:", message)

response = f"Echo: {message}"

conn.sendall(response.encode())

conn.close()
server_socket.close()
