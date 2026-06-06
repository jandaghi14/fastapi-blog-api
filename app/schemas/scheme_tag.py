from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagResponse(TagCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
