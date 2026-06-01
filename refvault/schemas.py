from datetime import datetime
from typing import Annotated, Any, List, Optional

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    field_validator,
)

from refvault.models import Tag


def tag_to_str(v: Any) -> str:
    name = v.name if isinstance(v, Tag) else str(v)
    return name.strip().lower()


TagStr = Annotated[str, BeforeValidator(tag_to_str)]


class TagCreate(BaseModel):
    name: TagStr


# todo: define proper validation
class UserCreate(BaseModel):
    username: Annotated[
        str, Field(min_length=3, max_length=10, pattern=r"^[a-zA-Z0-9]+$")
    ]
    password: Annotated[str, Field(min_length=3)]

    @field_validator("username", "password", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str):
        return v.strip()


class ImageBase(BaseModel):
    url: str
    name: str


class ImageCreate(ImageBase):
    tags: List[TagStr] = []
    source: Optional[str] = None


class ImageResponse(ImageBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: List[TagStr] = []
    palette: Optional[List[str]] = None
    source: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class ImageTagsUpdate(BaseModel):
    tags: List[TagStr]


class Token(BaseModel):
    access_token: str
    token_type: str


class Pagination(BaseModel):
    current_page: int
    last_page: int
    per_page: int
    total: int


class PaginatedImagesResponse(BaseModel):
    items: List[ImageResponse]
    meta: Pagination
