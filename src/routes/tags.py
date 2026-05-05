from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
from database import get_db
from schemas import TagResponse

router = APIRouter(prefix="/tags")


@router.get("/", response_model=List[TagResponse])
async def get_tags(db: AsyncSession = Depends(get_db)):
    tags = await db.execute(select(models.Tag))
    return tags.scalars().all()
