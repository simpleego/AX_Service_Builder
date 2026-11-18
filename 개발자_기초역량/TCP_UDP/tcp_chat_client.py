import os
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
            data = client.recv(1024)
        except OSError:
            # exit 입력으로 소켓을 닫았거나, 연결이 강제로 끊김
            break

        # recv()가 빈 바이트(b"")를 돌려주면 서버가 연결을 닫은 것
        # 이 검사가 없으면 빈 문자열을 무한히 출력한다
        if not data:
            print("\n서버와 연결이 끊어졌습니다.", flush=True)
            os._exit(0)  # input()에서 대기 중인 메인 스레드까지 함께 종료

        print("\n" + data.decode())


thread = threading.Thread(
    target=receive_message,
    daemon=True
)

thread.start()

print("채팅 시작 (종료: exit)")

while True:

    try:
        message = input("> ")
    except (EOFError, KeyboardInterrupt):
        break

    if message.strip() == "exit":
        break

    if not message.strip():
        continue

    try:
        client.sendall(message.encode())
    except OSError:
        print("메시지를 보낼 수 없습니다. 서버 연결이 끊어졌습니다.")
        break

client.close()
