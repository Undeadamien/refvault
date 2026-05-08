from typing import Sequence

import models
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_tags(db: AsyncSession) -> Sequence[models.Tag]:
    res = await db.execute(select(models.Tag))
    return res.scalars().all()


async def get_or_create_tag(db: AsyncSession, name: str) -> models.Tag:
    res = await db.execute(select(models.Tag).where(models.Tag.name == name))
    tag = res.scalar_one_or_none()
    if not tag:
        tag = models.Tag(name=name)
        db.add(tag)
        await db.flush()
    return tag
