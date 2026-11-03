"""
비밀번호 해시 유틸리티
- 비밀번호는 절대 평문으로 저장하지 않습니다.
- bcrypt는 매번 다른 salt를 자동으로 붙이므로 같은 비밀번호라도 해시값이 달라집니다.
"""
import bcrypt


def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))
