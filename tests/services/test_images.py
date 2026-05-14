import pytest

from src.services.images import *

payloads = [
    ImageCreate(url="https://example.com/test_00.jpg", name="test", tags=["0", "1"]),
    ImageCreate(url="https://example.com/test_01.jpg", name="test", tags=["0", "1"]),
]


@pytest.mark.asyncio
async def test_get_all_images(test_session, test_user):
    for payload in payloads:
        await create_image(test_session, test_user.id, payload)
    imgs = await get_all_images(test_session, test_user.id)
    assert len(imgs) == len(payloads)


@pytest.mark.asyncio
async def test_get_image_by_id(test_session, test_user):
    created = await create_image(test_session, test_user.id, payloads[0])
    fetched = await get_image_by_id(test_session, test_user.id, created.id)
    assert fetched is not None
    assert created == fetched


@pytest.mark.asyncio
async def test_create_image(test_session, test_user):
    img = await create_image(test_session, test_user.id, payloads[0])
    assert img.id is not None
    assert len(img.tags) == 2


@pytest.mark.asyncio
async def test_delete_image_by_id(test_session, test_user):
    img = await create_image(test_session, test_user.id, payloads[0])
    assert await get_image_by_id(test_session, test_user.id, img.id) is not None
    await delete_image_by_id(test_session, test_user.id, img.id)
    assert await get_image_by_id(test_session, test_user.id, img.id) is None


@pytest.mark.asyncio
async def test_delete_image_by_id_invalid(test_session, test_user):
    assert await delete_image_by_id(test_session, test_user.id, 888888) is False


@pytest.mark.asyncio
async def test_update_image_tags(test_session, test_user):
    img = await create_image(test_session, test_user.id, payloads[0])
    assert list(map(lambda x: str(x.name), img.tags)) == payloads[0].tags
    new_tags = ["new_tag"]
    updated = await update_image_tags(test_session, test_user.id, img.id, new_tags)
    assert updated
    assert list(map(lambda x: str(x.name), updated.tags)) == ["new_tag"]


@pytest.mark.asyncio
async def test_update_image_tags_invalid(test_session, test_user):
    updated = await update_image_tags(test_session, test_user.id, 0, [])
    assert not updated
