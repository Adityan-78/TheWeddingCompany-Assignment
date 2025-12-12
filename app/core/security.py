import hashlib
import bcrypt

def _sha(text: str) -> bytes:
    return hashlib.sha256(text.encode()).hexdigest().encode()

def hash_password(password: str) -> str:
    pre = _sha(password)
    return bcrypt.hashpw(pre, bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    pre = _sha(password)
    return bcrypt.checkpw(pre, hashed.encode())
