from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models


async def get_all_tags(db: AsyncSession) -> Sequence[models.Tag]:
    res = await db.execute(select(models.Tag))
    return res.scalars().all()


async def get_or_create_tag(db: AsyncSession, name: str) -> models.Tag:
    name = name.strip().lower()
    res = await db.execute(select(models.Tag).where(models.Tag.name == name))
    tag = res.scalar_one_or_none()
    if tag:
        return tag
    tag = models.Tag(name=name)
    db.add(tag)
    return tag


async def delete_tag_by_name(db: AsyncSession, name: str) -> bool:
    name = name.strip().lower()
    tag = await db.execute(select(models.Tag).where(models.Tag.name == name))
    tag = tag.scalar_one_or_none()
    if not tag:
        return False
    await db.delete(tag)
    await db.commit()
    return True
