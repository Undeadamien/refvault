from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ImageBase(BaseModel):
    url: str


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
