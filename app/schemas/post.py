from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    model_config = ConfigDict(from_attributes=True)


class PostCreate(PostBase):
    pass
