from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.schemas.scheme_user import OwnerResponse


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    model_config = ConfigDict(from_attributes=True)
    owner: OwnerResponse


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None


class PostPaginatedResponse (BaseModel):
    total: int
    page: int
    pages: int
    size: int
    items: list[PostResponse]
    model_config = ConfigDict(from_attributes=True)
