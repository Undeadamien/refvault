import pytest

from src.models import User
from src.services.auth import hash_password


@pytest.mark.asyncio
async def test_login_valid(test_client, test_session):
    test_session.add(User(username="testuser", hashed_password=hash_password("secret")))
    await test_session.commit()
    data = {"username": "testuser", "password": "secret"}
    res = await test_client.post("/auth/token", data=data)
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(test_client, test_session):
    test_session.add(User(username="testuser", hashed_password=hash_password("secret")))
    await test_session.commit()
    data = {"username": "testuser", "password": "wrong"}
    res = await test_client.post("/auth/token", data=data)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_login_not_found(test_client):
    data = {"username": "testuser", "password": "secret"}
    res = await test_client.post("/auth/token", data=data)
    assert res.status_code == 401
