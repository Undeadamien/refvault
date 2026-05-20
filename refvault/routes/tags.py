from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from refvault.database import get_db
from refvault.routes.auth import get_current_user
from refvault.schemas import TagStr
from refvault.services import tags as tag_service

router = APIRouter(prefix="/tags")


@router.get("/", response_model=List[TagStr])
async def get_tags(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    return await tag_service.get_user_tags(db, user.id)
