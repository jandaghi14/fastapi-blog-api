from pydantic import BaseModel, ConfigDict
from app.core.enums import Role
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: str


class UserRegister(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    role: Role
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class OwnerResponse(BaseModel):
    username: str
    model_config = ConfigDict(from_attributes=True)
