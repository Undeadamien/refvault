from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from refvault.database import get_db
from refvault.models import User
from refvault.schemas import Token, UserCreate
from refvault.services.auth import (
    authenticate_user,
    create_access_token,
    decode_token,
    hash_password,
)

router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=Token)
async def register(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    user = User(username=data.username, hashed_password=hash_password(data.password))
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Username already taken")
    await db.refresh(user)
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    res = await db.execute(select(User).where(User.username == username))
    user = res.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
