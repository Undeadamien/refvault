import pytest

from src.services.images import *
from src.services.tags import *

payloads = [
    ImageCreate(url="https://example.com/test_00.jpg", name="test", tags=["0", "1"]),
    ImageCreate(url="https://example.com/test_01.jpg", name="test", tags=["2", "3"]),
]


@pytest.mark.asyncio
async def test_get_all_tags(test_session, test_user):
    expected = set()
    for payload in payloads:
        await create_image(test_session, test_user.id, payload)
        expected.update(payload.tags)
    tags = await get_user_tags(test_session, test_user.id)
    assert {t.name for t in tags} == expected


@pytest.mark.asyncio
async def test_get_create_tag(test_session):
    tag = await get_or_create_tag(test_session, "test")
    assert tag.name == "test"
