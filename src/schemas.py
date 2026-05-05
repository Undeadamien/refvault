from datetime import datetime
from typing import Annotated, List, Optional

from pydantic import AfterValidator, BaseModel, ConfigDict, HttpUrl

# Validate as HttpUrl, then convert to str
UrlStr = Annotated[HttpUrl, AfterValidator(str)]


class TagCreate(BaseModel):
    name: str


class TagResponse(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class ImageBase(BaseModel):
    url: UrlStr
    name: str


class ImageCreate(ImageBase):
    tags: List[str] = []


class ImageResponse(ImageBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: List[TagResponse] = []
    model_config = ConfigDict(from_attributes=True)


class ImageTagsUpdate(BaseModel):
    tags: List[str]
