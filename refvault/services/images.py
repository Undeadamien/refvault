import logging
from typing import List, Sequence

import httpx
from Pylette import extract_colors
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from refvault import models
from refvault.config import settings
from refvault.schemas import ImageCreate
from refvault.services.tags import get_or_create_tag

logger = logging.getLogger(__name__)


async def extract_palette(url: str) -> List[str]:
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        res = await client.get(str(url))
        res.raise_for_status()
    palette = extract_colors(res.content, palette_size=5)
    hexs = [color.hex for color in palette.colors]
    return hexs


async def add_color_palette(image_id: int, url: str, db: AsyncSession):
    try:
        hexs = await extract_palette(url)
    except Exception as e:
        logger.warning("palette extraction failed for image %d: %s", image_id, e)
        return
    img = await db.get(models.Image, image_id)
    if img is None:
        return
    img.palette = hexs
    await db.commit()


async def get_all_images(
    db: AsyncSession,
    user_id: int,
    page: int = 1,
    per_page: int = settings.pagination_size,
) -> tuple[Sequence[models.Image], int]:
    base = select(models.Image).where(models.Image.user_id == user_id)
    count_q = select(func.count()).select_from(base.subquery())
    total = (await db.execute(count_q)).scalar_one()
    q = base.offset((page - 1) * per_page).limit(per_page)
    res = await db.execute(q)
    images = res.scalars().all()
    return images, total


async def get_image_by_id(
    db: AsyncSession,
    user_id: int,
    image_id: int,
) -> models.Image | None:
    res = await db.execute(
        select(models.Image)
        .where(models.Image.id == image_id)
        .where(models.Image.user_id == user_id)
    )
    return res.scalar_one_or_none()


# todo: check for duplicate url
async def create_image(
    db: AsyncSession,
    user_id: int,
    payload: ImageCreate,
) -> models.Image:
    img = models.Image(url=payload.url, name=payload.name, user_id=user_id)
    img.tags = [await get_or_create_tag(db, name) for name in payload.tags]
    db.add(img)
    await db.commit()
    await db.refresh(img)
    return img


async def delete_image_by_id(
    db: AsyncSession,
    user_id: int,
    image_id: int,
) -> bool:
    img = await get_image_by_id(db, user_id, image_id)
    if not img:
        return False
    await db.delete(img)
    await db.commit()
    return True


async def update_image_tags(
    db: AsyncSession,
    user_id: int,
    image_id: int,
    tags: list[str],
) -> models.Image | None:
    img = await get_image_by_id(db, user_id, image_id)
    if not img:
        return None
    img.tags = [await get_or_create_tag(db, name) for name in tags]
    await db.commit()
    await db.refresh(img)
    return img
