import asyncio
import logging
from typing import List, Optional, Sequence

import httpx
from Pylette import extract_colors
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from refvault import models
from refvault.config import settings
from refvault.database import SessionLocal
from refvault.schemas import ImageCreate
from refvault.services.tags import get_or_create_tag

logger = logging.getLogger(__name__)


async def extract_palette(path: str) -> List[str]:
    if path.startswith("/uploads/"):
        data = (settings.upload_dir / path.removeprefix("/uploads/")).read_bytes()
    else:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            res = await client.get(str(path))
            res.raise_for_status()
            data = res.content
    palette = await asyncio.to_thread(extract_colors, data, palette_size=5)
    hexs = [color.hex for color in palette.colors]
    return hexs


async def add_color_palette(image_id: int, path: str):
    try:
        hexs = await extract_palette(path)
    except Exception as e:
        logger.warning("palette extraction failed for image %d: %s", image_id, e)
        return
    async with SessionLocal() as db:
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
    q: Optional[str] = None,
) -> tuple[Sequence[models.Image], int]:
    base = select(models.Image).where(models.Image.user_id == user_id)
    if q:
        pattern = f"%{q}%"
        base = base.where(
            models.Image.name.ilike(pattern)
            | models.Image.tags.any(models.Tag.name.ilike(pattern))
        )
    count_q = select(func.count()).select_from(base.subquery())
    total = (await db.execute(count_q)).scalar_one()
    query = base.offset((page - 1) * per_page).limit(per_page)
    res = await db.execute(query)
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


async def create_image(
    db: AsyncSession,
    user_id: int,
    payload: ImageCreate,
) -> models.Image:
    img = models.Image(
        url=payload.url, name=payload.name, user_id=user_id, source=payload.source
    )
    img.tags = [await get_or_create_tag(db, name) for name in payload.tags]
    db.add(img)
    await db.commit()
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
    return img
