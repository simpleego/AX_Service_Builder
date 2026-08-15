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

        except Exception:
            break

    if conn in clients:
        clients.remove(conn)

    conn.close()
    print("종료:", addr)


server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))
server.listen()

print(f"Chat Server: {HOST}:{PORT}")

while True:
    conn, addr = server.accept()

    clients.append(conn)

    thread = threading.Thread(
        target=handle_client,
        args=(conn, addr),
        daemon=True
    )

    thread.start()
