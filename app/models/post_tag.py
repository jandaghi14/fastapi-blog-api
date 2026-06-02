from app.db.base import Base
from sqlalchemy import Column, Integer, ForeignKey


class PostTag(Base):
    __tablename__ = "posts_tags"

    post_id = Column(Integer, ForeignKey('posts.id'),
                     nullable=False, primary_key=True)

    tag_id = Column(Integer, ForeignKey('tags.id'),
                    nullable=False, primary_key=True)
