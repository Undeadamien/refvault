from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import models
from src.schemas import ImageCreate
from src.services.tags import get_or_create_tag


async def get_all_images(db: AsyncSession) -> Sequence[models.Image]:
    res = await db.execute(select(models.Image))
    return res.scalars().all()


async def get_image_by_id(db: AsyncSession, image_id: int) -> models.Image | None:
    res = await db.execute(select(models.Image).where(models.Image.id == image_id))
    return res.scalar_one_or_none()


async def create_image(db: AsyncSession, payload: ImageCreate) -> models.Image:
    img = models.Image(url=payload.url, name=payload.name)
    img.tags = [await get_or_create_tag(db, name) for name in payload.tags]
    db.add(img)
    await db.commit()
    await db.refresh(img)
    return img


async def delete_image_by_id(db: AsyncSession, image_id: int) -> bool:
    img = await get_image_by_id(db, image_id)
    if not img:
        return False
    await db.delete(img)
    await db.commit()
    return True


async def update_image_tags(
    db: AsyncSession, image_id: int, tags: list[str]
) -> models.Image | None:
    img = await get_image_by_id(db, image_id)
    if not img:
        return None
    img.tags = [await get_or_create_tag(db, name) for name in tags]
    await db.commit()
    await db.refresh(img)
    return img
