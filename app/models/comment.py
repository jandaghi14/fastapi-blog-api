from app.db.base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False,
                        server_default=func.now())
    is_published = Column(Boolean, nullable=False, default=True)
    owner_id = Column(Integer, ForeignKey('users.id'),
                      nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'),
                     nullable=False)
