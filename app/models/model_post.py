from app.db.base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False,
                        server_default=func.now())
    is_published = Column(Boolean, nullable=False, default=True)
    owner_id = Column(Integer, ForeignKey('users.id'),
                      nullable=False)
    tags = relationship('Tag', secondary='posts_tags', back_populates="posts")
