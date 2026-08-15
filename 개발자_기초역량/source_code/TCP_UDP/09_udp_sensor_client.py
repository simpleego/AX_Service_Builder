import socket
import random
import time
import json

HOST = "127.0.0.1"
PORT = 6001

client = socket.socket(
    socket.AF_INET,
    socket.SOCK_DGRAM
)

while True:
    data = {
        "temperature": round(
            random.uniform(20, 30),
            2
        ),
        "humidity": round(
            random.uniform(40, 70),
            2
        )
    }

    message = json.dumps(data)

    client.sendto(
        message.encode(),
        (HOST, PORT)
    )

    print("전송:", message)

    time.sleep(1)
