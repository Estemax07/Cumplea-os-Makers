from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from .config import settings

# Nota: usamos la librería `bcrypt` directamente en vez de `passlib.CryptContext`
# porque passlib 1.7.x tiene un bug de compatibilidad con bcrypt >= 4.1 que
# rompe el hashing (ver https://github.com/pyca/bcrypt/issues/684).
_BCRYPT_MAX_BYTES = 72  # límite duro de bcrypt


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:_BCRYPT_MAX_BYTES]
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verificar_password(password_plano: str, password_hasheado: str) -> bool:
    password_bytes = password_plano.encode("utf-8")[:_BCRYPT_MAX_BYTES]
    try:
        return bcrypt.checkpw(password_bytes, password_hasheado.encode("utf-8"))
    except ValueError:
        return False


def crear_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decodificar_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
