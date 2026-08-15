import socket
import threading

HOST = "127.0.0.1"
PORT = 5001

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect((HOST, PORT))


def receive_message():
    while True:
        try:
            message = client.recv(1024).decode()

            if not message:
                break

            print("\n", message)

        except Exception:
            break


thread = threading.Thread(
    target=receive_message,
    daemon=True
)

thread.start()

print("채팅 시작")

while True:
    message = input("> ")

    if message == "exit":
        break

    client.sendall(message.encode())

client.close()
