from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.session import get_db
from app.schemas.scheme_post import PostCreate, PostUpdate
from app.models.model_user import User
from app.core.dependencies import get_current_user
from app.services.service_post import PostService

router_post = APIRouter(prefix='/post', tags=['Post'])


@router_post.post('/create_post')
async def create_post(post: PostCreate,
                      current_user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_db)):
    return await PostService().create_post(post, current_user, session)


@router_post.get('/get_all_posts')
async def get_all_posts_endpoint(current_user: User = Depends(get_current_user),
                                 session: AsyncSession = Depends(get_db)
                                 ):
    return await PostService().get_all_posts(current_user, session)


@router_post.get('/get_post_by_id/{post_id}')
async def get_post_by_id_endpoint(post_id: int,
                                  current_user: User = Depends(
                                      get_current_user),
                                  session: AsyncSession = Depends(get_db)):
    result = await PostService().get_post_by_id(post_id, current_user, session)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=404, detail="The post does not exist for the user")


@router_post.get('/search')
async def search_endpoint(title: Optional[str] = None,
                          is_published: Optional[bool] = None,
                          current_user: User = Depends(
        get_current_user),
        session: AsyncSession = Depends(get_db)):

    return await PostService().search_post(current_user, session, title, is_published)


@router_post.put('/update_post/{post_id}')
async def update_post_endpoint(post_id: int,
                               new_post: PostUpdate,
                               current_user: User = Depends(get_current_user),
                               session: AsyncSession = Depends(get_db),
                               ):
    result = await PostService().update_post(post_id, new_post, current_user, session)
    if result:
        return {"message": f"Post with ID '{post_id}' updated successfully!"}
    elif result is None:
        raise HTTPException(
            status_code=404, detail=f"Post with ID {post_id} for User '{current_user.username}' does not exists")
    elif result == False:
        raise HTTPException(
            status_code=401, detail=f"Post with ID {post_id} does not belong to User '{current_user.username}' "
        )


@router_post.delete('/delete_post/{post_id}')
async def delete_post_endpoint(post_id: int,
                               current_user: User = Depends(get_current_user),
                               session: AsyncSession = Depends(get_db),
                               ):
    result = await PostService().delete_post(post_id, current_user, session)

    if result:
        return {"message": f"Post with ID '{post_id}' deleted successfully!"}
    elif result is None:
        raise HTTPException(
            status_code=404, detail=f"Post with ID {post_id} for User '{current_user.username}' does not exists")
    elif result == False:
        raise HTTPException(
            status_code=401, detail=f"Post with ID {post_id} does not belong to User '{current_user.username}' "
        )
