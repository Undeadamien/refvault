import pytest

from src.models import *


@pytest.mark.asyncio
async def test_get_tags(test_client, test_session):
    tag = Tag(name="manual-tag")
    test_session.add(tag)
    await test_session.commit()
    response = await test_client.get("/tags/")
    assert response.status_code == 200
    data = response.json()
    assert data and len(data) == 1
    assert data[0] == "Manual-tag"


@pytest.mark.asyncio
async def test_get_tags_empty(test_client):
    response = await test_client.get("/tags/")
    assert response.status_code == 200
    assert response.json() == []
