from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserRegister
from app.db.session import get_db
from app.services.user_service import UserService

router_auth = APIRouter(prefix='/auth', tags=['Authentication'])


@router_auth.post('/user_register')
async def user_register(data: UserRegister, session: AsyncSession = Depends(get_db)):
    result = await UserService().user_register(data, session)
    return result


@router_auth.post('/login')
async def user_login(data: OAuth2PasswordRequestForm = Depends(),
                     session: AsyncSession = Depends(get_db)):
    result = await UserService().user_login(data.username, data.password, session)
    return result
