from sqlalchemy.ext.asyncio import AsyncSession

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
