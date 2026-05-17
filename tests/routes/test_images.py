import pytest

from src.config import settings


# todo: add more test related to pagination
@pytest.mark.asyncio
async def test_get_images(test_client):
    await test_client.post(
        "/images/",
        json={"url": "https://example.com/test.jpg", "name": "test", "tags": []},
    )
    res = await test_client.get("/images/")
    assert res.status_code == 200
    data = res.json()
    assert data
    assert len(data["items"]) == 1
    assert data["meta"]["current_page"] == 1
    assert data["meta"]["last_page"] == 1
    assert data["meta"]["per_page"] == settings.pagination_size
    assert data["meta"]["total"] == 1


@pytest.mark.asyncio
async def test_get_image_by_id(test_client):
    create = await test_client.post(
        "/images/",
        json={"url": "https://example.com/test.jpg", "name": "test", "tags": []},
    )
    img_id = create.json()["id"]
    res = await test_client.get(f"/images/{img_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == img_id


@pytest.mark.asyncio
async def test_get_image_by_id_invalid(test_client):
    res = await test_client.get("/images/9999")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_create_image(test_client):
    payload = {"url": "https://example.com/test.jpg", "name": "test", "tags": ["test"]}
    res = await test_client.post("/images/", json=payload)
    assert res.status_code == 200

    data = res.json()
    assert data["name"] == "test"
    assert data["url"] == "https://example.com/test.jpg"
    assert data["tags"] == ["test"]


@pytest.mark.asyncio
async def test_create_image_wrong_url(test_client):
    payload = {"url": "hellllo", "name": "Test Image", "tags": ["test"]}
    res = await test_client.post("/images/", json=payload)
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_delete_image(test_client):
    create = await test_client.post(
        "/images/",
        json={"url": "https://example.com/test.jpg", "name": "test", "tags": []},
    )
    img_id = create.json()["id"]
    res = await test_client.delete(f"/images/{img_id}")
    assert res.status_code == 204


@pytest.mark.asyncio
async def test_delete_image_invalid(test_client):
    res = await test_client.delete("/images/9999")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_set_tags(test_client):
    create = await test_client.post(
        "/images/",
        json={"url": "https://example.com/test.jpg", "name": "test", "tags": ["test"]},
    )
    img_id = create.json()["id"]
    res = await test_client.put(f"/images/{img_id}/tags", json={"tags": ["new_tag"]})
    assert res.status_code == 200
    data = res.json()
    assert data["tags"] == ["new_tag"]


@pytest.mark.asyncio
async def test_set_tags_invalid(test_client):
    res = await test_client.put("/images/9999/tags", json={"tags": ["new_tag"]})
    assert res.status_code == 404
    assert res.json()["detail"] == "Image not found"
