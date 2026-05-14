from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.routes.auth import get_current_user
from src.schemas import ImageCreate, ImageResponse, ImageTagsUpdate
from src.services import images as image_service

router = APIRouter(prefix="/images")


@router.get("/", response_model=List[ImageResponse])
async def get_images(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await image_service.get_all_images(db, user.id)


@router.post("/", response_model=ImageResponse)
async def post_image(
    payload: ImageCreate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await image_service.create_image(db, user.id, payload)


@router.get("/{id}", response_model=ImageResponse)
async def get_image(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    img = await image_service.get_image_by_id(db, user.id, id)
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    return img


@router.delete("/{id}", status_code=204)
async def delete_image(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    deleted = await image_service.delete_image_by_id(db, user.id, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Image not found")


@router.put("/{id}/tags", response_model=ImageResponse)
async def set_tags(
    id: int,
    payload: ImageTagsUpdate,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    img = await image_service.update_image_tags(db, user.id, id, payload.tags)
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    return img
