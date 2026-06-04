from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.scheme_post import PostCreate
from app.models.model_user import User
from app.core.dependencies import get_current_user
from app.services.service_post import PostService

router_post = APIRouter(prefix='/post', tags=['Post'])


@router_post.post('/create_post')
async def create_post(post: PostCreate,
                      current_user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_db)):
    return await PostService().create_post(post, current_user, session)
