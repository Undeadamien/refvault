import pytest

from src.services.auth import *


@pytest.mark.asyncio
async def test_password():
    hashed = hash_password("secret")
    assert verify_password("secret", hashed) is True
    assert verify_password("terces", hashed) is False


@pytest.mark.asyncio
async def test_token():
    token = create_access_token({"sub": "testuser"})
    payload = decode_token(token)
    assert payload
    assert payload["sub"] == "testuser"
    assert "exp" in payload


@pytest.mark.asyncio
async def test_user_found(test_session):
    hashed = hash_password("secret")
    test_session.add(User(username="testuser", hashed_password=hashed))
    await test_session.commit()
    user = await authenticate_user(test_session, "testuser", "secret")
    assert user is not None
    assert user.username == "testuser"


@pytest.mark.asyncio
async def test_wrong_password(test_session):
    hashed = hash_password("secret")
    test_session.add(User(username="testuser", hashed_password=hashed))
    await test_session.commit()
    user = await authenticate_user(test_session, "testuser", "wrong")
    assert user is None


@pytest.mark.asyncio
async def test_user_not_found(test_session):
    user = await authenticate_user(test_session, "testuser", "secret")
    assert user is None
