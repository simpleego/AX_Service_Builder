"""
UDP 웹캠 수신 클라이언트 (수강생)

서버에 JOIN 을 보내 등록한 뒤, 날아오는 JPEG 프레임을 받아 화면에 보여준다.

실행: python udp_webcam_client.py [서버IP]   (기본 127.0.0.1, 종료: 창에서 q)
"""

import socket
import sys

import cv2
import numpy as np

SERVER = (sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1", 6000)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)
sock.sendto(b"JOIN", SERVER)    # "영상 보내주세요" 등록
print("서버에 접속 요청:", SERVER)

while True:
    try:
        data, _ = sock.recvfrom(65536)
    except (socket.timeout, ConnectionResetError):
        # 1초간 아무것도 안 옴 → 서버가 아직 안 켜졌거나 JOIN 이 유실됨. 다시 요청
        sock.sendto(b"JOIN", SERVER)
        continue

    # 받은 바이트(JPEG) → 이미지로 복원
    frame = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
    if frame is None:       # 깨진 패킷이면 버리고 다음 프레임
        continue

    cv2.imshow("Student (q: quit)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

sock.sendto(b"LEAVE", SERVER)
sock.close()
cv2.destroyAllWindows()
