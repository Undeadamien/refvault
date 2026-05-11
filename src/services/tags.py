from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models


async def get_all_tags(db: AsyncSession) -> Sequence[models.Tag]:
    res = await db.execute(select(models.Tag))
    return res.scalars().all()


async def get_or_create_tag(db: AsyncSession, name: str) -> models.Tag:
    res = await db.execute(select(models.Tag).where(models.Tag.name == name))
    tag = res.scalar_one_or_none()
    if tag:
        return tag
    tag = models.Tag(name=name)
    db.add(tag)
    return tag
