from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.models.model_user import User
from app.repositories.base_repository import BaseRepository
from app.schemas import scheme_user


class UserRepository(BaseRepository):

    async def create(self,
                     data: scheme_user.UserRegister,
                     session: AsyncSession
                     ):
        new_user = User(**data.model_dump())
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    async def get_by_id(self,
                        id: int,
                        session: AsyncSession):
        result = await session.execute(select(User).where(User.id == id))
        return result.scalars().first()

    async def get_all(self, session: AsyncSession):
        result = await session.execute(select(User))
        return result.scalars().all()

    async def update(self,
                     id: int,
                     session: AsyncSession,
                     data: scheme_user.UserUpdate
                     ):
        await session.execute(
            update(User)
            .where(User.id == id)
            .values(**data.model_dump(exclude_unset=True))
        )
        await session.commit()
        return True

    async def delete(self,
                     id: int,
                     session: AsyncSession):
        result = await session.execute(select(User).where(User.id == id))
        user = result.scalars().first()
        if user:
            await session.delete(user)
            await session.commit()
            return True
        else:
            return False

    async def get_by_username(self,
                              username: str,
                              session: AsyncSession
                              ):
        result = await session.execute(select(User).where(User.username == username))
        return result.scalars().first()
