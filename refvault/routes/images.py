import json
import mimetypes
import uuid
from pathlib import Path
from typing import Optional

import httpx
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
)
from pydantic import HttpUrl, TypeAdapter
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
from refvault.services import cache
from refvault.services import images as image_service

router = APIRouter(prefix="/images")


@router.get("/", response_model=PaginatedImagesResponse)
async def get_images(
    page: int = Query(1, ge=1),
    per_page: int = Query(settings.pagination_size, ge=1),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    cache_key = cache.key("images", "list", str(user.id), str(page), str(per_page))
    cached = await cache.get(cache_key)
    if cached is not None:
        return PaginatedImagesResponse(**cached)

    images, total = await image_service.get_all_images(db, user.id, page, per_page)
    last_page = max(1, (total + per_page - 1) // per_page)
    result = PaginatedImagesResponse(
        items=[ImageResponse.model_validate(img) for img in images],
        meta=Pagination(
            current_page=page,
            last_page=last_page,
            per_page=per_page,
            total=total,
        ),
    )
    await cache.set(cache_key, result.model_dump(mode="json"))
    return result


@router.post("/", response_model=ImageResponse)
async def post_image(
    background_task: BackgroundTasks,
    name: str = Form(...),
    tags: str = Form("[]"),
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    if not file and not url:
        raise HTTPException(400, "provide file or url")
    if file and url:
        raise HTTPException(400, "provide file or source url not both")

    if file:
        if file.filename is None:
            raise HTTPException(400, "missing filename")
        ext = Path(file.filename).suffix.lower()
        data = await file.read()
        source = None
    else:
        if url is None:
            raise HTTPException(400, "missing url")
        try:
            TypeAdapter(HttpUrl).validate_python(url)
        except Exception:
            raise HTTPException(422, "invalid URL")
        source = url
        async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
            res = await client.get(url)
            res.raise_for_status()
            data = res.content
        ext = (
            Path(url).suffix.lower()
            or mimetypes.guess_extension(res.headers.get("content-type", ""))
            or ""
        )

    if ext not in settings.allowed_extensions:
        raise HTTPException(400, f"unsupported file type: {ext}")
    if len(data) > settings.max_upload_size:
        raise HTTPException(400, "file too large")

    rel = Path(str(user.id)) / f"{uuid.uuid4().hex}{ext}"
    dest = settings.upload_dir / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)

    img = await image_service.create_image(
        db,
        user.id,
        ImageCreate(
            url=f"/uploads/{rel}", name=name, tags=json.loads(tags), source=source
        ),
    )
    await cache.delete_pattern(cache.key("images", "list", str(user.id), "*"))
    await cache.delete_pattern(cache.key("tags", "list", str(user.id)))
    background_task.add_task(image_service.add_color_palette, img.id, img.url, db)
    return img


@router.get("/{id}", response_model=ImageResponse)
async def get_image(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    cache_key = cache.key("images", "detail", str(user.id), str(id))
    cached = await cache.get(cache_key)
    if cached is not None:
        return ImageResponse(**cached)

    img = await image_service.get_image_by_id(db, user.id, id)
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    result = ImageResponse.model_validate(img)
    await cache.set(cache_key, result.model_dump(mode="json"))
    return result


@router.delete("/{id}", status_code=204)
async def delete_image(
    id: int,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    img = await image_service.get_image_by_id(db, user.id, id)
    if not img:
        raise HTTPException(status_code=404, detail="Image not found")
    if img.url.startswith("/uploads"):
        (settings.upload_dir / img.url.removeprefix("/uploads/")).unlink(
            missing_ok=True
        )
    await db.delete(img)
    await db.commit()
    await cache.delete_pattern(cache.key("images", "list", str(user.id), "*"))
    await cache.delete(cache.key("images", "detail", str(user.id), str(id)))
    await cache.delete_pattern(cache.key("tags", "list", str(user.id)))


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
    await cache.delete_pattern(cache.key("images", "list", str(user.id), "*"))
    await cache.delete(cache.key("images", "detail", str(user.id), str(id)))
    await cache.delete_pattern(cache.key("tags", "list", str(user.id)))
    return img
