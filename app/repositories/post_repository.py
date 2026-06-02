from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional
from app.models.post import Post
from app.repositories.base_repository import BaseRepository
from app.schemas import post


class PostRepository(BaseRepository):
    async def create(self,
                     data: post.PostCreate,
                     owner_id: int,
                     session: AsyncSession,
                     ):
        new_post = Post(owner_id=owner_id, **data.model_dump())
        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)
        return new_post

    async def get_by_id(self,
                        post_id: int,
                        session: AsyncSession,
                        ):
        result = await session.execute(select(Post).where(Post.id == post_id))
        return result.scalars().first()

    async def get_all(self,
                      session: AsyncSession):
        result = await session.execute(select(Post))
        return result.scalars().all()

    async def update(self,
                     post_id: int,
                     session: AsyncSession,
                     data: post.PostUpdate
                     ):
        await session.execute(update(Post)
                              .where(Post.id == post_id)
                              .values(**data.model_dump(exclude_unset=True)))
        await session.commit()
        return True

    async def delete(self,
                     post_id: int,
                     session: AsyncSession):
        result = await session.execute(select(Post).where(Post.id == post_id))
        fetched_post = result.scalars().first()
        if fetched_post:
            await session.delete(fetched_post)
            await session.commit()
            return True
        else:
            return False

    async def search(self,
                     session: AsyncSession,
                     title: Optional[str] = None,
                     is_published: Optional[bool] = None,
                     owner_id: Optional[int] = None,
                     ):
        query = select(Post)

        if title:
            query = query.where(Post.title.ilike(f"%{title}%"))
        if is_published is not None:
            query = query.where(Post.is_published == is_published)
        if owner_id:
            query = query.where(Post.owner_id == owner_id)

        result = await session.execute(query)
        return result.scalars().all()
