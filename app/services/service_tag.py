from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.tag_repository import TagRepository
from app.repositories.post_tag_repository import PostTagRepository
from app.repositories.post_repository import PostRepository


class TagService:
    async def create(self,
                     tag_name,
                     session: AsyncSession):
        result = await TagRepository().get_by_name(tag_name, session)
        if result is None:
            return await TagRepository().create(tag_name, session)
        else:
            return False

    async def get_all(self,
                      sesssion: AsyncSession):
        return await TagRepository().get_all(sesssion)

    async def get_by_id(self,
                        tag_id: int,
                        session: AsyncSession):
        return await TagRepository().get_by_id(tag_id, session)

    async def update(self,
                     tag_id: int,
                     new_tag: str,
                     session: AsyncSession):
        result = await TagRepository().get_by_id(tag_id, session)
        if result is None:
            return None
        return await TagRepository().update(tag_id, new_tag, session)

    async def delete(self,
                     tag_id: int,
                     session: AsyncSession):
        result = await TagRepository().get_by_id(tag_id, session)
        if result is None:
            return None
        return await TagRepository().delete(tag_id, session)

    async def assign_tag_to_post(self,
                                 tag_id: int,
                                 post_id: int,
                                 session: AsyncSession):

        if await TagRepository().get_by_id(tag_id=tag_id, session=session) is None:
            return False
        if await PostRepository().get_by_id(post_id=post_id, session=session) is None:
            return False

        result = await PostTagRepository().get_post_tag(post_id=post_id, tag_id=tag_id, session=session)
        if result is not None:
            return None
        return await PostTagRepository().create(post_id=post_id, tag_id=tag_id, session=session)

    async def remove_tag_from_post(self,
                                   tag_id: int,
                                   post_id: int,
                                   session: AsyncSession):
        return await PostTagRepository().delete(post_id=post_id, tag_id=tag_id, session=session)
