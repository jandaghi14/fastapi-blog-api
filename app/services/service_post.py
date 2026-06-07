from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import math
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
                            session: AsyncSession,
                            page,
                            size):
        offset = (page-1)*size
        result = await PostRepository().get_all(session, offset=offset, size=size)
        return {
            "total": result[0],
            "page": page,
            "pages": math.ceil(result[0]/size),
            "size": size,
            "items": result[1]
        }

    async def get_post_by_id(self,
                             post_id: int,
                             user: User,
                             session: AsyncSession):
        return await PostRepository().get_by_id(post_id, session)

    async def update_post(self,
                          post_id: int,
                          new_post: scheme_post.PostUpdate,
                          user: User,
                          session: AsyncSession):
        result = await PostRepository().get_by_id(post_id, session)
        if result is None:
            return None
        if result and result.owner_id == user.id:
            return await PostRepository().update(post_id,  session, new_post)
        return result

    async def delete_post(self,
                          post_id: int,
                          user: User,
                          session: AsyncSession):
        result = await PostRepository().get_by_id(post_id, session)
        if result is None:
            return None
        if result and result.owner_id == user.id:
            return await PostRepository().delete(post_id,  session)
        return False

    async def search_post(self,
                          user: User,
                          session: AsyncSession,
                          title: Optional[str] = None,
                          is_published: Optional[bool] = None):
        return await PostRepository().search(session, title=title, is_published=is_published)

    async def search_tag_title(self,
                               session: AsyncSession,
                               title: Optional[str] = None,
                               tag: Optional[str] = None,):
        return await PostRepository().search_tag_title(title=title, tag=tag, session=session)
