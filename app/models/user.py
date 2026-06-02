from app.db.base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default='user')
    is_active = Column(Boolean, nullable=False, default=True)
