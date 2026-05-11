import pytest


@pytest.mark.asyncio
async def test_create_image(test_client):
    payload = {"url": "https://example.com/test.jpg", "name": "test", "tags": ["test"]}
    response = await test_client.post("/images/", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "test"
    assert data["url"] == "https://example.com/test.jpg"
    assert data["tags"] == ["Test"]


@pytest.mark.asyncio
async def test_create_image_wrong_url(test_client):
    payload = {"url": "hellllo", "name": "Test Image", "tags": ["test"]}
    response = await test_client.post("/images/", json=payload)
    assert response.status_code == 422
