from typing import List

from database import get_db
from fastapi import APIRouter, Depends
from schemas import TagResponse
from sqlalchemy.ext.asyncio import AsyncSession

from services import tags as tag_service

router = APIRouter(prefix="/tags")


@router.get("/", response_model=List[TagResponse])
async def get_tags(db: AsyncSession = Depends(get_db)):
    return await tag_service.get_all_tags(db)
