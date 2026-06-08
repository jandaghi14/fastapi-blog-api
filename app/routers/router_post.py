from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.session import get_db
from app.schemas.scheme_post import PostCreate, PostUpdate, PostResponse, PostPaginatedResponse
from app.models.model_user import User
from app.core.dependencies import get_current_user
from app.services.service_post import PostService
from app.core.logger import logger
router_post = APIRouter(prefix='/post', tags=['Post'])


@router_post.post('/create_post', response_model=PostResponse)
async def create_post(post: PostCreate,
                      current_user: User = Depends(get_current_user),
                      session: AsyncSession = Depends(get_db)):
    user_id = current_user.id
    result = await PostService().create_post(post, current_user, session)
    logger.info(
        f"User {user_id} created a post - router_post - create_post")
    return result


@router_post.get('/get_all_posts', response_model=PostPaginatedResponse)
async def get_all_posts_endpoint(current_user: User = Depends(get_current_user),
                                 session: AsyncSession = Depends(get_db,),
                                 page: int = 1,
                                 size: Optional[int] = 5,
                                 ):

    return await PostService().get_all_posts(current_user, session=session, page=page, size=size)


@router_post.get('/get_post_by_id/{post_id}', response_model=PostResponse)
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


@router_post.get('/search', response_model=list[PostResponse])
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
    return await PostService().update_post(post_id, new_post, current_user, session)


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
    elif result is False:
        raise HTTPException(
            status_code=401, detail=f"Post with ID {post_id} does not belong to User '{current_user.username}' "
        )


@router_post.get('/search_tag_title', response_model=list[PostResponse])
async def search_tag_title_endpoint(title: Optional[str] = None,
                                    tag: Optional[str] = None,
                                    current_user: User = Depends(
        get_current_user),
        session: AsyncSession = Depends(get_db)):
    if title is None and tag is None:
        raise HTTPException(
            status_code=400, detail="Provide at least a title or a tag to search.")

    result = await PostService().search_tag_title(session, title, tag)

    return result
