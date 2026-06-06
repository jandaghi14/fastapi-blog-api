from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional
from app.models.model_comment import Comment
from app.repositories.base_repository import BaseRepository
from app.schemas import scheme_comment


class CommentRepository(BaseRepository):

    async def create(self,
                     user_id: int,
                     data: scheme_comment.CommentCreate,
                     session: AsyncSession
                     ):
        new_comment = Comment(owner_id=user_id, **data.model_dump())
        session.add(new_comment)
        await session.commit()
        await session.refresh(new_comment)
        return new_comment

    async def get_by_id(self,
                        comment_id: int,
                        session: AsyncSession

                        ):
        result = await session.execute(select(Comment).where(Comment.id == comment_id))
        return result.scalars().first()

    async def get_all(self, *args, **kwargs):
        raise NotImplementedError

    async def update(self,
                     comment_id: int,
                     data: scheme_comment.CommentUpdate,
                     session: AsyncSession,
                     ):
        await session.execute(update(Comment).where(Comment.id == comment_id).values(**data.model_dump(exclude_unset=True)))
        await session.commit()
        return True

    async def delete(self,
                     comment_id,
                     session: AsyncSession):
        result = await session.execute(select(Comment).where(Comment.id == comment_id))
        fetched_comment = result.scalars().first()
        if fetched_comment:
            await session.delete(fetched_comment)
            await session.commit()
            return True
        else:
            return False

    async def get_by_post_id(self,
                             post_id: int,
                             session: AsyncSession
                             ):
        result = await session.execute(select(Comment).where(Comment.post_id == post_id))
        return result.scalars().all()
