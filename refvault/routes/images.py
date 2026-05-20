from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from refvault.config import settings
from refvault.database import get_db
from refvault.routes.auth import get_current_user
from refvault.schemas import (
    ImageCreate,
    ImageResponse,
    ImageTagsUpdate,
    PaginatedImagesResponse,
    Pagination,
)
from refvault.services import images as image_service

router = APIRouter(prefix="/images")


@router.get("/", response_model=PaginatedImagesResponse)
async def get_images(
    page: int = Query(1, ge=1),
    per_page: int = Query(settings.pagination_size, ge=1),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    images, total = await image_service.get_all_images(db, user.id, page, per_page)
    last_page = max(1, (total + per_page - 1) // per_page)
    return PaginatedImagesResponse(
        items=[ImageResponse.model_validate(img) for img in images],
        meta=Pagination(
            current_page=page,
            last_page=last_page,
            per_page=per_page,
            total=total,
        ),
    )


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
