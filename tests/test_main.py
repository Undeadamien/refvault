import pytest


@pytest.mark.asyncio
async def test_create_image(client):
    payload = {
        "url": "https://example.com/test.jpg",
        "name": "Test Image",
        "tags": ["test"],
    }
    response = await client.post("/images/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Image"
    assert data["url"] == "https://example.com/test.jpg"
