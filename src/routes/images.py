from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
from database import get_db
from schemas import ImageCreate, ImageResponse, ImageTagsUpdate

router = APIRouter(prefix="/images")


async def get_or_create_tag(name: str, db: AsyncSession) -> models.Tag:
    res = await db.execute(select(models.Tag).where(models.Tag.name == name))
    tag = res.scalar_one_or_none()
    if not tag:
        tag = models.Tag(name=name)
        db.add(tag)
        await db.flush()
    return tag


@router.get("/", response_model=List[ImageResponse])
async def get_images(db: AsyncSession = Depends(get_db)):
    images = await db.execute(select(models.Image))
    return images.scalars().all()


@router.post("/", response_model=ImageResponse)
async def post_image(payload: ImageCreate, db: AsyncSession = Depends(get_db)):
    img = models.Image(url=payload.url, name=payload.name)
    img.tags = [await get_or_create_tag(name, db) for name in payload.tags]
    db.add(img)
    await db.commit()
    await db.refresh(img)
    return img


@router.get("/{id}", response_model=ImageResponse)
async def get_image(id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(models.Image).where(models.Image.id == id))
    img = res.scalar_one_or_none()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    return img


@router.put("/{id}/tags", response_model=ImageResponse)
async def set_tags(
    id: int, payload: ImageTagsUpdate, db: AsyncSession = Depends(get_db)
):
    res = await db.execute(select(models.Image).where(models.Image.id == id))
    img = res.scalar_one_or_none()
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    img.tags = [await get_or_create_tag(name, db) for name in payload.tags]
    await db.commit()
    await db.refresh(img)
    return img
