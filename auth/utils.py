from datetime import datetime, timedelta

import jwt
from core.config import settings
import bcrypt


def encode_jwt(  # создаёт токен.
    payload: dict,
    key: str = settings.auth_jwt.private_key_path.read_text(),  #  Обязательно приватный и добавляем read_text() чтобы прочитать и закрыть сразу
    algorithm: str = settings.auth_jwt.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
):
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(  # проверяет и распаковывает токен.
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),  #  Обязательно публичный и добавляем read_text() чтобы прочитать и закрыть сразу
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_passwd(password: str) -> bytes:  # хеширует пароль через bcrypt.
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_passwd(  #
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
