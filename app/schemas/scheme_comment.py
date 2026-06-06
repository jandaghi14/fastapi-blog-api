from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CommentBase(BaseModel):
    content: str
    is_published: bool = True


class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    owner_id: int
    post_id: int
    model_config = ConfigDict(from_attributes=True)


class CommentCreate(CommentBase):
    post_id: int


class CommentUpdate(CommentBase):
    pass
