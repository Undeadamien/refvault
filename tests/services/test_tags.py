import pytest

from src.services.images import *
from src.services.tags import *

payloads = [
    ImageCreate(url="https://example.com/test_00.jpg", name="test", tags=["0", "1"]),
    ImageCreate(url="https://example.com/test_01.jpg", name="test", tags=["2", "3"]),
]


@pytest.mark.asyncio
async def test_get_all_tags(test_session):
    expected = set()
    for payload in payloads:
        await create_image(test_session, payload)
        expected.update(payload.tags)
    tags = await get_all_tags(test_session)
    assert {t.name for t in tags} == expected


@pytest.mark.asyncio
async def test_get_create_tag(test_session):
    tags = await get_all_tags(test_session)
    assert len(tags) == 0
    tag = await get_or_create_tag(test_session, "test")
    assert tag.name == "test"
    res = await get_all_tags(test_session)
    assert len(res) == 1
    assert res[0].name == "test"


@pytest.mark.asyncio
async def test_delete_tag(test_session):
    await get_or_create_tag(test_session, "nature")
    res = await delete_tag_by_name(test_session, "nature")
    assert res is True
    assert await get_all_tags(test_session) == []


@pytest.mark.asyncio
async def test_delete_tag_invalid(test_session):
    res = await delete_tag_by_name(test_session, "nature")
    assert res is False
