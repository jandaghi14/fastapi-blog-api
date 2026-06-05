from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.models.model_user import User
from app.schemas import scheme_post
from app.repositories.post_repository import PostRepository


class PostService:
    async def create_post(self,
                          post: scheme_post.PostCreate,
                          user: User,
                          session: AsyncSession):
        result = await PostRepository().create(post,
                                               user.id,
                                               session)
        return result

    async def get_all_posts(self,
                            user: User,
                            session: AsyncSession):
        return await PostRepository().get_all_posts_of_the_user(user.id, session)

    async def get_post_by_id(self,
                             post_id: int,
                             user: User,
                             session: AsyncSession):
        return await PostRepository().get_by_id(post_id, user.id, session)

    async def update_post(self,
                          post_id: int,
                          new_post: scheme_post.PostUpdate,
                          user: User,
                          session: AsyncSession):
        result = await PostRepository().get_by_id(post_id, user.id, session)
        if result:
            return await PostRepository().update(post_id,  session, new_post)
        return result

    async def delete_post(self,
                          post_id: int,
                          user: User,
                          session: AsyncSession):
        result = await PostRepository().get_by_id(post_id, user.id, session)
        if result:
            return await PostRepository().delete(post_id,  session)
        return result

    async def search_post(self,
                          user: User,
                          session: AsyncSession,
                          title: Optional[str] = None,
                          is_published: Optional[bool] = None):
        return await PostRepository().search(user.id, session, title=title, is_published=is_published)
