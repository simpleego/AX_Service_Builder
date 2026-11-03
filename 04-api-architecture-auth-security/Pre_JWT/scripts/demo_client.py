"""
프론트엔드 없이 쿠키/세션 인증 흐름을 단계별로 확인하는 데모 클라이언트

사용법:
  1) 서버 실행:   uvicorn app.main:app --reload
  2) 다른 터미널: python scripts/demo_client.py

httpx.Client 는 브라우저처럼 응답의 Set-Cookie 를 저장해 두었다가
다음 요청에 Cookie 헤더로 자동 전송합니다.
"""
import sys

import httpx

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"


def title(text):
    print("\n" + "=" * 70 + f"\n {text}\n" + "=" * 70)


def show(label, r: httpx.Response):
    print(f"\n▶ {label}")
    print(f"  {r.request.method} {r.request.url.path}  →  {r.status_code}")
    if "cookie" in r.request.headers:
        print(f"  [요청 Cookie]  {r.request.headers['cookie'][:90]}")
    for sc in r.headers.get_list("set-cookie"):
        print(f"  [Set-Cookie]   {sc[:90]}")
    try:
        print(f"  [응답 본문]    {r.json()}")
    except Exception:
        print(f"  [응답 본문]    {r.text[:200]}")


def main():
    users = [
        {"username": "hong", "email": "hong@example.com", "password": "1234"},
        {"username": "kim", "email": "kim@example.com", "password": "5678"},
    ]

    title("0. 회원가입 (이미 있으면 409)")
    with httpx.Client(base_url=BASE) as c:
        for u in users:
            show(f"signup {u['username']}", c.post("/users/signup", json=u))

    # ------------------------------------------------------------------
    title("1-1. 평문 쿠키 - 위조 공격 체험")
    with httpx.Client(base_url=BASE) as c:
        show("hong 로그인", c.post("/cookie/v1/login", json={"username": "hong", "password": "1234"}))
        r = c.get("/cookie/v1/me")
        show("내 정보 조회", r)
        hong_id = r.json()["id"]

    with httpx.Client(base_url=BASE) as attacker:
        # 로그인 없이 쿠키 값만 직접 만들어 보냄
        attacker.cookies.set("user_id", str(hong_id + 1))
        show("⚠ 공격자: 쿠키를 user_id=다른번호 로 조작", attacker.get("/cookie/v1/me"))

    # ------------------------------------------------------------------
    title("1-2. 서명 쿠키 - 위조 방지, 그러나 로그아웃 후에도 재사용 가능")
    with httpx.Client(base_url=BASE) as c:
        show("hong 로그인", c.post("/cookie/v2/login", json={"username": "hong", "password": "1234"}))
        show("내 정보 조회", c.get("/cookie/v2/me"))
        show("쿠키 내용 들여다보기", c.get("/cookie/v2/inspect"))
        stolen = c.cookies.get("auth")

        tampered = stolen[:-3] + ("AAA" if not stolen.endswith("AAA") else "BBB")
        with httpx.Client(base_url=BASE) as attacker:
            attacker.cookies.set("auth", tampered)
            show("공격자: 서명 부분을 변조", attacker.get("/cookie/v2/me"))

        show("hong 로그아웃", c.post("/cookie/v2/logout"))
        show("로그아웃 후 내 정보 (쿠키 삭제됨)", c.get("/cookie/v2/me"))

    with httpx.Client(base_url=BASE) as attacker:
        attacker.cookies.set("auth", stolen)
        show("⚠ 미리 복사해 둔 쿠키로 접근 → 여전히 성공!", attacker.get("/cookie/v2/me"))

    # ------------------------------------------------------------------
    title("2. 서버 세션 - 로그아웃 시 즉시 무효화")
    with httpx.Client(base_url=BASE, headers={"User-Agent": "PC-Chrome"}) as pc, \
         httpx.Client(base_url=BASE, headers={"User-Agent": "Mobile-Safari"}) as mobile:
        show("PC에서 로그인", pc.post("/session/login", json={"username": "hong", "password": "1234"}))
        show("모바일에서 로그인", mobile.post("/session/login", json={"username": "hong", "password": "1234"}))
        show("PC: 마이페이지", pc.get("/session/mypage"))
        show("PC: 내 접속 기기 목록", pc.get("/session/devices"))

        stolen = pc.cookies.get("session_id")
        show("PC 로그아웃 (DB 세션 삭제)", pc.post("/session/logout"))

        with httpx.Client(base_url=BASE) as attacker:
            attacker.cookies.set("session_id", stolen)
            show("✅ 미리 복사해 둔 세션 쿠키로 접근 → 실패", attacker.get("/session/me"))

        show("모바일은 여전히 로그인 상태", mobile.get("/session/me"))
        show("모바일: 모든 기기 로그아웃", mobile.post("/session/logout-all"))
        show("모바일: 다시 조회", mobile.get("/session/me"))

    with httpx.Client(base_url=BASE) as anon:
        show("로그인 없이 보호된 API 접근", anon.get("/session/mypage"))


if __name__ == "__main__":
    main()
