from datetime import datetime
from typing import Annotated, Optional

from pydantic import AfterValidator, BaseModel, ConfigDict, HttpUrl

# Validate as HttpUrl, then convert to str
UrlStr = Annotated[HttpUrl, AfterValidator(str)]


class ImageBase(BaseModel):
    url: UrlStr


class ImageCreate(ImageBase):
    pass


class ImageResponse(ImageBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
