from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from refvault.config import settings


@pytest.mark.asyncio
async def test_get_images(test_client_auth):
    await test_client_auth.post(
        "/images/",
        files={
            "file": ("test.jpg", b"fake-image-data", "image/jpeg"),
            "name": (None, "test"),
            "tags": (None, "[]"),
        },
    )
    res = await test_client_auth.get("/images/")
    assert res.status_code == 200
    data = res.json()
    assert data
    assert len(data["items"]) == 1
    assert data["meta"]["current_page"] == 1
    assert data["meta"]["last_page"] == 1
    assert data["meta"]["per_page"] == settings.pagination_size
    assert data["meta"]["total"] == 1


@pytest.mark.asyncio
async def test_get_image_by_id(test_client_auth):
    create = await test_client_auth.post(
        "/images/",
        files={
            "file": ("test.jpg", b"fake-image-data", "image/jpeg"),
            "name": (None, "test"),
            "tags": (None, "[]"),
        },
    )
    img_id = create.json()["id"]
    res = await test_client_auth.get(f"/images/{img_id}")
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == img_id


@pytest.mark.asyncio
async def test_get_image_by_id_invalid(test_client_auth):
    res = await test_client_auth.get("/images/9999")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_create_image(test_client_auth):
    res = await test_client_auth.post(
        "/images/",
        files={
            "file": ("test.jpg", b"fake-image-data", "image/jpeg"),
            "name": (None, "test"),
            "tags": (None, '["test"]'),
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "test"
    assert data["url"].startswith("/uploads/")
    assert data["tags"] == ["test"]


@pytest.mark.asyncio
async def test_create_image_from_url(test_client_auth):
    fake = b"fake-remote-image"
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.content = fake
        mock_res.headers = {"content-type": "image/jpeg"}
        mock_get.return_value = mock_res
        res = await test_client_auth.post(
            "/images/",
            data={
                "url": "https://example.com/photo.jpg",
                "name": "test",
                "tags": '["test"]',
            },
        )
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "test"
    assert data["url"].startswith("/uploads/")


@pytest.mark.asyncio
async def test_create_image_wrong_url(test_client_auth):
    res = await test_client_auth.post(
        "/images/",
        data={
            "url": "not-a-url",
            "name": "test",
            "tags": "[]",
        },
    )
    assert res.status_code == 422


@pytest.mark.asyncio
async def test_create_image_no_source(test_client_auth):
    res = await test_client_auth.post(
        "/images/",
        data={
            "name": "test",
            "tags": "[]",
        },
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_create_image_wrong_extension(test_client_auth):
    res = await test_client_auth.post(
        "/images/",
        files={
            "file": ("test.exe", b"fake", "application/x-msdownload"),
            "name": (None, "test"),
            "tags": (None, "[]"),
        },
    )
    assert res.status_code == 400


@pytest.mark.asyncio
async def test_delete_image(test_client_auth):
    create = await test_client_auth.post(
        "/images/",
        files={
            "file": ("test.jpg", b"fake-image-data", "image/jpeg"),
            "name": (None, "test"),
            "tags": (None, "[]"),
        },
    )
    img_id = create.json()["id"]
    res = await test_client_auth.delete(f"/images/{img_id}")
    assert res.status_code == 204


@pytest.mark.asyncio
async def test_delete_image_invalid(test_client_auth):
    res = await test_client_auth.delete("/images/9999")
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_set_tags(test_client_auth):
    create = await test_client_auth.post(
        "/images/",
        files={
            "file": ("test.jpg", b"fake-image-data", "image/jpeg"),
            "name": (None, "test"),
            "tags": (None, '["test"]'),
        },
    )
    img_id = create.json()["id"]
    res = await test_client_auth.put(
        f"/images/{img_id}/tags", json={"tags": ["new_tag"]}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["tags"] == ["new_tag"]


@pytest.mark.asyncio
async def test_set_tags_invalid(test_client_auth):
    res = await test_client_auth.put("/images/9999/tags", json={"tags": ["new_tag"]})
    assert res.status_code == 404
    assert res.json()["detail"] == "Image not found"
