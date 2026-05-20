from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from refvault.config import settings
from refvault.models import User

password_hash = PasswordHash.recommended()


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire_time = settings.access_token_expire_minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_time)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> User | None:
    res = await db.execute(select(User).where(User.username == username))
    user = res.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except InvalidTokenError:
        return None
