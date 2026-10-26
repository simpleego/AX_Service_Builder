"""
📌 3일차 실습 — 비밀번호 해싱 & JWT
📌 4일차 실습 — Refresh Token 생성

아래 함수들을 직접 구현하세요. (AI 도구 사용 금지 — 강의안 원칙 참고)
막히면 강의안 3~4일차의 그림(비유·시퀀스 다이어그램)을 다시 보세요.
"""
import secrets
import hashlib
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt, JWTError

from app.core.config import settings


# ---------- 3일차: 비밀번호 해싱 ----------
def hash_password(plain_password: str) -> str:
    """
    TODO: 평문 비밀번호를 bcrypt로 해싱해서 반환하세요.
    힌트: bcrypt.hashpw(bytes, bcrypt.gensalt()) 는 bytes를 반환합니다.
          DB에는 문자열(str)로 저장할 것이므로 decode가 필요합니다.
    """
    raise NotImplementedError("hash_password를 구현하세요 (3일차)")


def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    TODO: 로그인 시 입력한 평문 비밀번호와 저장된 해시를 비교하세요.
    힌트: bcrypt.checkpw(bytes, bytes) -> bool
    """
    raise NotImplementedError("verify_password를 구현하세요 (3일차)")


# ---------- 3일차: Access Token (JWT) ----------
def create_access_token(user_id: int) -> str:
    """
    TODO: user_id를 담은 JWT를 발급하세요.
    포함해야 할 정보(payload):
      - sub: 사용자 식별자 (문자열로 변환해서 넣을 것)
      - exp: 만료 시각 (settings.ACCESS_TOKEN_EXPIRE_MINUTES 분 후)
      - type: "access" (refresh와 구분하기 위함)
    힌트: jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    """
    raise NotImplementedError("create_access_token을 구현하세요 (3일차)")


def decode_access_token(token: str) -> int | None:
    """
    TODO: JWT를 검증하고 user_id(int)를 반환하세요.
    - 서명이 잘못됐거나 만료됐으면 예외(JWTError)가 발생합니다 -> None 반환
    - type이 'access'가 아니면 -> None 반환
    힌트: jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    """
    raise NotImplementedError("decode_access_token을 구현하세요 (3일차)")


# ---------- 4일차: Refresh Token ----------
# 💡 왜 JWT가 아니라 무작위 문자열인지 강의안 4일차 이론을 참고하세요.
def generate_refresh_token() -> str:
    """
    TODO: 사용자에게 내려줄 원본 Refresh Token을 생성하세요.
    힌트: secrets.token_urlsafe(n)
    """
    raise NotImplementedError("generate_refresh_token을 구현하세요 (4일차)")


def hash_refresh_token(raw_token: str) -> str:
    """
    TODO: 원본 토큰을 해시해서 반환하세요. (DB에는 원본이 아니라 해시만 저장!)
    힌트: hashlib.sha256(bytes).hexdigest()
    """
    raise NotImplementedError("hash_refresh_token을 구현하세요 (4일차)")
