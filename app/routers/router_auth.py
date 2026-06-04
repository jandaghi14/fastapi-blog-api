from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.scheme_user import UserRegister
from app.db.session import get_db
from app.services.service_user import UserService
from fastapi import HTTPException

router_auth = APIRouter(prefix='/auth', tags=['Authentication'])


@router_auth.post('/user_register')
async def user_register(data: UserRegister, session: AsyncSession = Depends(get_db)):
    result = await UserService().user_register(data, session)
    if result:
        return {"message": f"Username '{data.username}' registered successfully!"}
    else:
        raise HTTPException(
            status_code=400, detail=f"Username '{data.username}' already exists!")


@router_auth.post('/login')
async def user_login(data: OAuth2PasswordRequestForm = Depends(),
                     session: AsyncSession = Depends(get_db)):
    result = await UserService().user_login(data.username, data.password, session)
    if result:
        return {"access_token": result,
                "token_type": "bearer"}

    if result is None:
        raise HTTPException(
            status_code=400, detail="Wrong username")

    if not result:
        raise HTTPException(
            status_code=401, detail="username or password is wrong")
