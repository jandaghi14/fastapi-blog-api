from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, or_
from typing import Optional
from app.models.model_post import Post
from app.models.model_tag import Tag
from app.repositories.base_repository import BaseRepository
from app.schemas import scheme_post


class PostRepository(BaseRepository):
    async def create(self,
                     data: scheme_post.PostCreate,
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

    async def get_all_posts_of_the_user(self,
                                        user_id: int,
                                        session: AsyncSession):

        result = await session.execute(select(Post).where(Post.owner_id == user_id))
        return result.scalars().all()

    async def update(self,
                     post_id: int,
                     session: AsyncSession,
                     data: scheme_post.PostUpdate
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
                     ):
        query = select(Post)

        if title:
            query = query.where(Post.title.ilike(f"%{title}%"))
        if is_published is not None:
            query = query.where(Post.is_published == is_published)

        result = await session.execute(query)
        return result.scalars().all()

    async def search_tag_title(self,
                               session: AsyncSession,

                               title: Optional[str] = None,
                               tag: Optional[str] = None,
                               ):
        if title is None and tag is None:
            return []

        conditions = []
        if title is not None:
            conditions.append(Post.title.ilike(f"%{title}%"))
        if tag is not None:
            conditions.append(Tag.name.ilike(f"%{tag}%"))

        result = await session.execute(
            select(Post)
            .outerjoin(Post.tags)
            .where(or_(*conditions))
            .distinct()
        )
        return result.scalars().all()
