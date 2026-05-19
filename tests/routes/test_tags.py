import pytest


@pytest.mark.asyncio
async def test_get_tags(test_client_auth):
    await test_client_auth.post(
        "/images/",
        json={"url": "https://example.com/t.jpg", "name": "t", "tags": ["manual-tag"]},
    )
    res = await test_client_auth.get("/tags/")
    assert res.status_code == 200
    data = res.json()
    assert data and len(data) == 1
    assert data[0] == "manual-tag"


@pytest.mark.asyncio
async def test_get_tags_empty(test_client_auth):
    res = await test_client_auth.get("/tags/")
    assert res.status_code == 200
    assert res.json() == []
