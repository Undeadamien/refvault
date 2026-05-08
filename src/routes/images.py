from typing import List

from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from schemas import ImageCreate, ImageResponse, ImageTagsUpdate
from sqlalchemy.ext.asyncio import AsyncSession

from services import images as image_service

router = APIRouter(prefix="/images")


@router.get("/", response_model=List[ImageResponse])
async def get_images(db: AsyncSession = Depends(get_db)):
    return await image_service.get_all_images(db)


@router.post("/", response_model=ImageResponse)
async def post_image(payload: ImageCreate, db: AsyncSession = Depends(get_db)):
    return await image_service.create_image(db, payload)


@router.get("/{id}", response_model=ImageResponse)
async def get_image(id: int, db: AsyncSession = Depends(get_db)):
    img = await image_service.get_image_by_id(db, id)
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    return img


@router.put("/{id}/tags", response_model=ImageResponse)
async def set_tags(
    id: int, payload: ImageTagsUpdate, db: AsyncSession = Depends(get_db)
):
    img = await image_service.update_image_tags(db, id, payload.tags)
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    return img
