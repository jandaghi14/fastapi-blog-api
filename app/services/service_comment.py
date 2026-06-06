from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.model_user import User
from app.schemas import scheme_comment
from app.repositories.comment_repository import CommentRepository
from app.repositories.post_repository import PostRepository


class CommentService:
    async def create(self,
                     current_user: User,
                     data: scheme_comment.CommentCreate,
                     session: AsyncSession
                     ):
        result = await PostRepository().get_by_id(data.post_id, session=session)
        if result:
            return await CommentRepository().create(current_user.id, data, session)
        else:
            return result

    async def get_by_id(self,
                        comment_id: int,
                        session: AsyncSession
                        ):
        return await CommentRepository().get_by_id(comment_id, session)

    async def update(self,
                     comment_id: int,
                     current_user: User,
                     data: scheme_comment.CommentUpdate,
                     session: AsyncSession
                     ):
        result = await CommentRepository().get_by_id(comment_id, session)
        if result is None:
            return None
        if result.owner_id == current_user.id:
            return await CommentRepository().update(comment_id, data, session)
        return False

    async def delete(self,
                     comment_id: int,
                     current_user: User,
                     session: AsyncSession
                     ):
        result = await CommentRepository().get_by_id(comment_id, session)
        if result is None:
            return None
        if result.owner_id == current_user.id:
            return await CommentRepository().delete(comment_id, session)
        return False

    async def get_by_post_id(self,
                             current_user: User,
                             post_id: int,
                             session: AsyncSession
                             ):
        result = await PostRepository().get_by_id(post_id,  session)
        if result:
            return await CommentRepository().get_by_post_id(post_id, session)
        return result
