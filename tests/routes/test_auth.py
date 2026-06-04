import pytest

from refvault.models import User
from refvault.services.auth import create_access_token, hash_password


@pytest.mark.asyncio
async def test_login_valid(test_client_non_auth, test_session):
    test_session.add(User(username="testuser", hashed_password=hash_password("secret")))
    await test_session.commit()
    data = {"username": "testuser", "password": "secret"}
    res = await test_client_non_auth.post("/auth/login", data=data)
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(test_client_non_auth, test_session):
    test_session.add(User(username="testuser", hashed_password=hash_password("secret")))
    await test_session.commit()
    data = {"username": "testuser", "password": "wrong"}
    res = await test_client_non_auth.post("/auth/login", data=data)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_login_not_found(test_client_non_auth):
    data = {"username": "testuser", "password": "secret"}
    res = await test_client_non_auth.post("/auth/login", data=data)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(test_session, test_client_non_auth):
    test_session.add(User(username="testuser", hashed_password=hash_password("secret")))
    await test_session.commit()
    token = create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {token}"}
    res = await test_client_non_auth.get("/images/", headers=headers)
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(test_client_non_auth):
    headers = {"Authorization": f"Bearer token"}
    res = await test_client_non_auth.get("/images/", headers=headers)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_invalid_user(test_client_non_auth):
    token = create_access_token(data={"sub": "test"})
    headers = {"Authorization": f"Bearer {token}"}
    res = await test_client_non_auth.get("/images/", headers=headers)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_missing_sub(test_client_non_auth):
    token = create_access_token(data={"test": "test"})
    headers = {"Authorization": f"Bearer {token}"}
    res = await test_client_non_auth.get("/images/", headers=headers)
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_register(test_client_non_auth):
    body = {"username": "user", "password": "secret"}
    res = await test_client_non_auth.post("/auth/register", json=body)
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.parametrize(
    "username",
    [""],
)
@pytest.mark.asyncio
async def test_register_invalid_username(test_client_non_auth, username):
    body = {"username": username, "password": "secret"}
    res = await test_client_non_auth.post("/auth/register", json=body)
    assert res.status_code == 422


@pytest.mark.parametrize(
    "password",
    [""],
)
@pytest.mark.asyncio
async def test_register_invalid_password(test_client_non_auth, password):
    body = {"username": "user", "password": password}
    res = await test_client_non_auth.post("/auth/register", json=body)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_register_user_duplicate(test_client_non_auth):
    body = {"username": "user", "password": "secret"}
    await test_client_non_auth.post("/auth/register", json=body)
    res = await test_client_non_auth.post("/auth/register", json=body)
    assert res.status_code == 409
