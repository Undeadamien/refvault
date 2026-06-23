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


@pytest.mark.asyncio
async def test_get_me(test_client_auth, test_user):
    res = await test_client_auth.get("/auth/me")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == test_user.id
    assert data["username"] == test_user.username


@pytest.mark.asyncio
async def test_get_me_unauthorized(test_client_non_auth):
    res = await test_client_non_auth.get("/auth/me")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_update_me_password(test_client_auth, test_session, test_user):
    res = await test_client_auth.put("/auth/me", json={"password": "newpass"})
    assert res.status_code == 200
    data = {"username": test_user.username, "password": "newpass"}
    login = await test_client_auth.post("/auth/login", data=data)
    assert login.status_code == 200


@pytest.mark.asyncio
async def test_delete_me(test_client_auth):
    res = await test_client_auth.delete("/auth/me")
    assert res.status_code == 204


@pytest.mark.asyncio
async def test_delete_me_removes_user(test_client_auth, test_session, test_user):
    await test_client_auth.delete("/auth/me")
    data = {"username": test_user.username, "password": "secret"}
    login = await test_client_auth.post("/auth/login", data=data)
    assert login.status_code == 401
