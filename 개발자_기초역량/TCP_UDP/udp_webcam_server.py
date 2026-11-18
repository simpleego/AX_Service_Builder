"""
UDP 웹캠 송신 서버 (강사)

웹캠 화면을 JPEG로 압축해서, 접속한 수강생들에게 UDP로 계속 보낸다.
프레임 1장 = UDP 패킷 1개. 중간에 몇 장 빠져도 다음 장을 보여주면 그만이다.

실행: python udp_webcam_server.py   (종료: 미리보기 창에서 q)
"""

import socket

import cv2

HOST = "0.0.0.0"      # 다른 PC의 수강생도 받을 수 있도록 모든 주소에서 대기
PORT = 6000
MAX_PACKET = 65000    # UDP 패킷 하나에 담을 수 있는 최대 크기(약 64KB) 이하로

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
sock.setblocking(False)   # 수강생 접속 확인 때문에 영상 송신이 멈추지 않도록

viewers = set()           # 영상을 받을 수강생 주소 목록 (ip, port)


def check_viewers():
    """수강생이 보낸 JOIN / LEAVE 를 처리한다 (기다리지 않고 있는 것만 읽음)."""
    while True:
        try:
            data, addr = sock.recvfrom(1024)
        except BlockingIOError:      # 더 읽을 게 없음
            return
        except ConnectionResetError:  # Windows: 이미 꺼진 수강생에게 보냈던 흔적, 무시
            continue

        if data == b"JOIN":
            viewers.add(addr)
            print("수강생 입장:", addr, "/ 현재", len(viewers), "명")
        elif data == b"LEAVE":
            viewers.discard(addr)
            print("수강생 퇴장:", addr, "/ 현재", len(viewers), "명")


cap = cv2.VideoCapture(0)
print(f"웹캠 송신 서버: UDP {PORT} 포트")

while True:
    check_viewers()

    ok, frame = cap.read()
    if not ok:
        print("웹캠을 읽을 수 없습니다.")
        break

    # 패킷 하나에 들어가도록 크기를 줄이고 JPEG로 압축
    frame = cv2.resize(frame, (640, 480))
    ok, jpg = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
    data = jpg.tobytes()

    if len(data) <= MAX_PACKET:
        for viewer in viewers:
            sock.sendto(data, viewer)   # 받았는지 확인하지 않고 그냥 보낸다

    cv2.imshow("Teacher (q: quit)", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
sock.close()
