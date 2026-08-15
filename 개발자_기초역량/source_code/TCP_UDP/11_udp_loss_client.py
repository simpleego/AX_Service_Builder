import socket
import time

HOST = "127.0.0.1"
PORT = 6002

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

client.settimeout(1)

for i in range(1, 11):
    message = f"Packet-{i}"

    client.sendto(
        message.encode(),
        (HOST, PORT)
    )

    try:
        data, addr = client.recvfrom(1024)
        print(
            message,
            "→",
            data.decode()
        )

    except socket.timeout:
        print(
            message,
            "→ 응답 없음"
        )

    time.sleep(0.5)

client.close()
