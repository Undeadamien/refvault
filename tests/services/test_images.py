import pytest

from src.services.images import *

payloads = [
    ImageCreate(url="https://example.com/test_00.jpg", name="test", tags=["0", "1"]),
    ImageCreate(url="https://example.com/test_01.jpg", name="test", tags=["0", "1"]),
]


@pytest.mark.asyncio
async def test_get_all_images(test_session):
    for payload in payloads:
        await create_image(test_session, payload)
    imgs = await get_all_images(test_session)
    assert len(imgs) == len(payloads)


@pytest.mark.asyncio
async def test_get_image_by_id(test_session):
    created = await create_image(test_session, payloads[0])
    fetched = await get_image_by_id(test_session, created.id)
    assert fetched is not None
    assert created == fetched


@pytest.mark.asyncio
async def test_create_image(test_session):
    img = await create_image(test_session, payloads[0])
    assert img.id is not None
    assert len(img.tags) == 2


@pytest.mark.asyncio
async def test_delete_image_by_id(test_session):
    img = await create_image(test_session, payloads[0])
    assert await get_image_by_id(test_session, img.id) is not None
    await delete_image_by_id(test_session, img.id)
    assert await get_image_by_id(test_session, img.id) is None


@pytest.mark.asyncio
async def test_update_image_tags(test_session):
    img = await create_image(test_session, payloads[0])
    assert list(map(lambda x: str(x.name), img.tags)) == payloads[0].tags
    new_tags = ["new_tag"]
    updated = await update_image_tags(test_session, img.id, new_tags)
    assert updated
    assert list(map(lambda x: str(x.name), updated.tags)) == new_tags


@pytest.mark.asyncio
async def test_update_image_tags_invalid(test_session):
    updated = await update_image_tags(test_session, 0, [])
    assert not updated
