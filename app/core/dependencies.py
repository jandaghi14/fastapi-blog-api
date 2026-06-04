from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.core.jwt import Token
from app.core.config import settings_jwt
from app.repositories.user_repository import UserRepository
from app.db.session import get_db

SECRET_KEY = settings_jwt.JWT_SECRET_KEY
ALGORITHM = settings_jwt.JWT_ALGORITHM


oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_current_user(session: AsyncSession = Depends(get_db),
                           token: str = Depends(oauth_scheme),
                           ):
    try:
        decoded_token = Token().decode_token_access(token)
        user_obj = await UserRepository().get_by_username(decoded_token.get('sub'), session)
        return user_obj
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token")
