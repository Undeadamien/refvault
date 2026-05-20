from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from refvault import models


async def get_user_tags(db: AsyncSession, user_id: int) -> Sequence[models.Tag]:
    res = await db.execute(
        select(models.Tag)
        .join(models.image_tags)
        .join(models.Image)
        .where(models.Image.user_id == user_id)
        .distinct()
    )
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
