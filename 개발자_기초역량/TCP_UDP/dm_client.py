"""
1:1 메시지 클라이언트

실행:  python dm_client.py alice
       python dm_client.py bob
종료:  /exit
"""

import json
import os
import socket
import sys
import threading

HOST = "127.0.0.1"
PORT = 5002


def send_json(sock, obj):
    sock.sendall((json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8"))


def show(text):
    # 입력 중인 프롬프트 줄을 덮어쓰고 출력한 뒤 프롬프트를 다시 그린다
    print(f"\r{text}\n> ", end="", flush=True)


def receive_loop(sock):
    reader = sock.makefile("r", encoding="utf-8", newline="\n")
    peer = "상대"

    try:
        for line in reader:
            packet = json.loads(line)
            kind = packet.get("type")

            if kind == "welcome":
                peer = packet["peer"]
                state = "접속 중" if packet["peer_online"] else "오프라인"
                show(f"=== {packet['user']}님 환영합니다. 대화 상대: {peer} ({state}) ===")
                if packet["queued"]:
                    show(f"--- 안 읽은 메시지 {packet['queued']}개 ---")

            elif kind == "msg":
                mark = " (오프라인 중 수신)" if packet.get("offline") else ""
                show(f"[{packet['time']}] {packet['from']}: {packet['text']}{mark}")

            elif kind == "ack":
                if packet["status"] == "queued":
                    show(f"    ({peer}님이 오프라인입니다. 접속하면 전달됩니다)")

            elif kind == "presence":
                state = "접속했습니다" if packet["online"] else "나갔습니다"
                show(f"*** {packet['user']}님이 {state} ***")

            elif kind == "error":
                print(f"\n[오류] {packet['message']}")
                os._exit(1)

    except (ConnectionError, OSError, json.JSONDecodeError):
        pass

    print("\n서버와 연결이 끊어졌습니다.")
    os._exit(0)


def main():
    user = sys.argv[1] if len(sys.argv) > 1 else input("사용자 이름: ").strip()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    send_json(sock, {"type": "login", "user": user})

    threading.Thread(target=receive_loop, args=(sock,), daemon=True).start()

    try:
        while True:
            text = input("> ")
            if text.strip() == "/exit":
                break
            if text.strip():
                send_json(sock, {"type": "msg", "text": text})
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        sock.close()


if __name__ == "__main__":
    main()
