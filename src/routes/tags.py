from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.schemas import TagResponse
from src.services import tags as tag_service

router = APIRouter(prefix="/tags")


@router.get("/", response_model=List[TagResponse])
async def get_tags(db: AsyncSession = Depends(get_db)):
    return await tag_service.get_all_tags(db)
