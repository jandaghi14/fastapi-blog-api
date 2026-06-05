from sqlalchemy.ext.asyncio import AsyncSession


from app.repositories.user_repository import UserRepository
from app.core import security
from app.schemas import scheme_user
from app.core.jwt import Token


class UserService:

    async def user_register(self,
                            data: scheme_user.UserRegister,
                            session: AsyncSession):

        user_repository = UserRepository()
        result = await user_repository.get_by_username(data.username, session)
        if result is not None:
            return False
        else:
            hashed_password = security.hash_password(data.password)
            data.password = hashed_password
            new_made_user = await user_repository.create(data, session)
            return new_made_user

    async def user_login(self,
                         username,
                         plain_password,
                         session: AsyncSession):
        user_repository = UserRepository()

        result = await user_repository.get_by_username(username, session)

        if result is not None:
            if security.verify_password(plain_password, result.password):
                token = Token().create_access_token(result)
                return token
            else:
                return False

        else:
            return None
