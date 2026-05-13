import pytest


@pytest.mark.asyncio
async def test_get_tags(test_client):
    await test_client.post(
        "/images/",
        json={"url": "https://example.com/t.jpg", "name": "t", "tags": ["manual-tag"]},
    )
    res = await test_client.get("/tags/")
    assert res.status_code == 200
    data = res.json()
    assert data and len(data) == 1
    assert data[0] == "manual-tag"


@pytest.mark.asyncio
async def test_get_tags_empty(test_client):
    res = await test_client.get("/tags/")
    assert res.status_code == 200
    assert res.json() == []


@pytest.mark.asyncio
async def test_delete_tag(test_client):
    await test_client.post(
        "/images/",
        json={"url": "https://example.com/t.jpg", "name": "t", "tags": ["nature"]},
    )
    res = await test_client.delete("/tags/nature")
    assert res.status_code == 204


@pytest.mark.asyncio
async def test_delete_tag_invalid(test_client):
    res = await test_client.delete("/tags/nature")
    assert res.status_code == 404
