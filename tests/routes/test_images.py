import pytest

from src.models import Image, Tag


@pytest.mark.asyncio
async def test_get_images(test_client, test_session):
    img = Image(url="https://example.com/test.jpg", name="test", tags=[])
    test_session.add(img)
    await test_session.commit()
    response = await test_client.get("/images/")
    assert response.status_code == 200
    data = response.json()
    assert data and len(data) == 1


@pytest.mark.asyncio
async def test_get_image_by_id(test_client, test_session):
    img = Image(url="https://example.com/test.jpg", name="test", tags=[])
    test_session.add(img)
    await test_session.commit()
    await test_session.refresh(img)
    response = await test_client.get(f"/images/{img.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == img.id


@pytest.mark.asyncio
async def test_get_image_by_id_invalid(test_client):
    response = await test_client.get("/images/9999")
    assert response.status_code == 404


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


@pytest.mark.asyncio
async def test_delete_image(test_client, test_session):
    img = Image(url="https://example.com/test.jpg", name="test", tags=[])
    test_session.add(img)
    await test_session.commit()
    await test_session.refresh(img)
    response = await test_client.delete(f"/images/{img.id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_image_invalid(test_client):
    response = await test_client.delete("/images/9999")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_set_tags(test_client, test_session):
    tag = Tag(name="test")
    img = Image(url="https://example.com/test.jpg", name="test", tags=[tag])
    test_session.add(img)
    await test_session.commit()
    await test_session.refresh(img)
    response = await test_client.put(f"/images/{img.id}/tags", json={"tags": ["new_tag"]})
    assert response.status_code == 200
    data = response.json()
    assert data["tags"] == ["New_tag"]


@pytest.mark.asyncio
async def test_set_tags_invalid(test_client):
    response = await test_client.put("/images/9999/tags", json={"tags": ["new_tag"]})
    assert response.status_code == 404
    assert response.json()["detail"] == "Image not found"
