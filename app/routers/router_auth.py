from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.scheme_user import UserRegister
from app.db.session import get_db
from app.models.model_user import User
from app.services.service_user import UserService
from app.core.dependencies import get_current_user
from app.core.limiter import limiter
from fastapi import HTTPException


router_auth = APIRouter(prefix='/auth', tags=['Authentication'])


@router_auth.post('/user_register')
async def user_register(data: UserRegister, session: AsyncSession = Depends(get_db)):
    result = await UserService().user_register(data, session)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=400, detail=f"Username '{data.username}' already exists!")


@router_auth.post('/login')
@limiter.limit("5/minute")
async def user_login(request: Request,
                     data: OAuth2PasswordRequestForm = Depends(),
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


@router_auth.post('/user/promote/{user_id}')
async def promote_user_endpoint(user_id: int,
                                current_user: User = Depends(get_current_user),
                                session: AsyncSession = Depends(get_db)):

    if current_user.role != 'admin':
        raise HTTPException(
            status_code=400, detail="Only admins can promote users")
    result = await UserService().promote_user(user_id=user_id, session=session)
    if result:
        return {'message': f"User with ID '{user_id}' promoted to admin successfully!"}
