import pytest

from src.services.images import *
from src.services.tags import *

payloads = [
    ImageCreate(url="https://example.com/test_00.jpg", name="test", tags=["0", "1"]),
    ImageCreate(url="https://example.com/test_01.jpg", name="test", tags=["2", "3"]),
]


@pytest.mark.asyncio
async def test_get_all_tags(test_session):
    expected = []
    for payload in payloads:
        await create_image(test_session, payload)
        expected.extend(payload.tags)
    tags = await get_all_tags(test_session)
    # todo: need improvements
    assert sorted(t for t in expected) == sorted(t.name for t in tags)


@pytest.mark.asyncio
async def test_get_create_tag(test_session):
    # todo: replace `get_all_tags`
    empty = len(await get_all_tags(test_session)) == 0
    assert empty
    tag = await get_or_create_tag(test_session, "test")
    assert tag.name == "test"
    res = await get_all_tags(test_session)
    assert len(res) == 1 and "test" == res[0].name
