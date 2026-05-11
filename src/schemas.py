from datetime import datetime
from typing import Annotated, Any, List, Optional

from pydantic import BaseModel, BeforeValidator, ConfigDict, HttpUrl, TypeAdapter

from src.models import Tag


def validate_url(url: str):
    return str(TypeAdapter(HttpUrl).validate_python(url))


def tag_to_str(v: Any) -> str:
    name = v.name if isinstance(v, Tag) else str(v)
    return name.strip().capitalize()


UrlStr = Annotated[str, BeforeValidator(validate_url)]
TagStr = Annotated[str, BeforeValidator(tag_to_str)]


class TagCreate(BaseModel):
    name: TagStr


class ImageBase(BaseModel):
    url: UrlStr
    name: str


class ImageCreate(ImageBase):
    tags: List[TagStr] = []


class ImageResponse(ImageBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: List[TagStr] = []
    model_config = ConfigDict(from_attributes=True)


class ImageTagsUpdate(BaseModel):
    tags: List[TagStr]
