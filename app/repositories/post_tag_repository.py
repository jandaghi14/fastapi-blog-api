from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.model_post_tag import PostTag
from app.repositories.base_repository import BaseRepository


class PostTagRepository(BaseRepository):
    async def create(self,
                     post_id: int,
                     tag_id: int,
                     session: AsyncSession
                     ):
        new_post_tag = PostTag(post_id=post_id, tag_id=tag_id)

        session.add(new_post_tag)
        await session.commit()
        await session.refresh(new_post_tag)
        return new_post_tag

    async def delete(self,
                     tag_id: int,
                     post_id: int,
                     session: AsyncSession):
        fetched_tag = await session.execute(select(PostTag).where(PostTag.post_id == post_id).where(PostTag.tag_id == tag_id))
        result = fetched_tag.scalars().first()
        if result:
            await session.delete(result)
            await session.commit()
            return True
        else:
            return False

    async def get_post_tag(self,
                           post_id: int,
                           tag_id: int,
                           session: AsyncSession):
        fetched_data = await session.execute(select(PostTag).where(PostTag.post_id == post_id).where(PostTag.tag_id == tag_id))
        return fetched_data.scalars().first()

    async def get_by_id(self, *args, **kwargs):
        pass

    async def get_all(self, *args, **kwargs):
        pass

    async def update(self, *args, **kwargs):
        pass
