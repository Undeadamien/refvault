import pytest

from refvault.models import Image, Tag, User


@pytest.mark.asyncio
async def test_user():
    user = User(username="alice", hashed_password=".")
    assert str(user) == "alice"


@pytest.mark.asyncio
async def test_tag():
    tag = Tag(name="nature")
    assert str(tag) == "nature"


@pytest.mark.asyncio
async def test_image():
    image = Image(url="placeholder", name="Beach", user_id=0)
    assert str(image) == "Beach"
