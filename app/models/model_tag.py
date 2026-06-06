from app.db.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    posts = relationship("Post", secondary="posts_tags", back_populates="tags")
