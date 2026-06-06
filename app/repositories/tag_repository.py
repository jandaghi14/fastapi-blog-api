from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.model_tag import Tag
from app.repositories.base_repository import BaseRepository


class TagRepository(BaseRepository):
    async def create(self,
                     tag_name: str,
                     session: AsyncSession
                     ):
        new_tag = Tag(name=tag_name)

        session.add(new_tag)
        await session.commit()
        await session.refresh(new_tag)
        return new_tag

    async def get_all(self,
                      session: AsyncSession):
        result = await session.execute(select(Tag))
        return result.scalars().all()

    async def get_by_id(self,
                        tag_id: int,
                        session: AsyncSession):
        result = await session.execute(select(Tag).where(Tag.id == tag_id))
        return result.scalars().first()

    async def get_by_name(self,
                          tag_name: str,
                          session: AsyncSession):
        result = await session.execute(select(Tag).where(Tag.name == tag_name))
        return result.scalars().first()

    async def update(self,
                     tag_id: int,
                     new_tag: str,
                     session: AsyncSession):
        await session.execute(update(Tag).where(Tag.id == tag_id).values(name=new_tag))
        await session.commit()
        return True

    async def delete(self,
                     tag_id,
                     session: AsyncSession):
        fetched_tag = await session.execute(select(Tag).where((Tag.id == tag_id)))
        result = fetched_tag.scalars().first()
        if result:
            await session.delete(result)
            await session.commit()
            return True
        else:
            return False
