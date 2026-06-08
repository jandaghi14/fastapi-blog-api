from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.scheme_comment import CommentCreate, CommentUpdate
from app.models.model_user import User
from app.core.dependencies import get_current_user
from app.services.service_comment import CommentService

router_comment = APIRouter(prefix='/comment', tags=['Comment'])


@router_comment.post('/create_comment')
async def create_comment(data: CommentCreate,
                         current_user: User = Depends(get_current_user),
                         session: AsyncSession = Depends(get_db)):
    result = await CommentService().create(current_user, data, session)
    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Post with ID '{data.post_id}' does not exist.")
    else:
        return result


@router_comment.get('/get_by_id/{comment_id}')
async def get_by_id_comment(comment_id: int,
                            current_user: User = Depends(get_current_user),
                            session: AsyncSession = Depends(get_db)):
    result = await CommentService().get_by_id(comment_id, session)
    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Comment with ID '{comment_id}' does not exist.")
    else:
        return result


@router_comment.get('/get_by_post_id/{post_id}')
async def get_by_post_id(post_id: int,
                         current_user: User = Depends(
                             get_current_user),
                         session: AsyncSession = Depends(get_db)):

    result = await CommentService().get_by_post_id(current_user, post_id, session)
    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Post with ID '{post_id}' does not exist.")
    else:
        return result


@router_comment.put('/update/{comment_id}')
async def update_comment(comment_id: int,
                         data: CommentUpdate,
                         current_user: User = Depends(get_current_user),
                         session: AsyncSession = Depends(get_db)):

    result = await CommentService().update(comment_id, current_user, data, session)

    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Comment with ID '{comment_id}' does not exist.")
    elif not result:
        raise HTTPException(
            status_code=401, detail=f"Comment with ID '{comment_id} does not belong to user'{current_user.id}'"
        )
    else:
        return result


@router_comment.delete('/delete/{comment_id}')
async def delete_comment(comment_id: int,
                         current_user: User = Depends(get_current_user),
                         session: AsyncSession = Depends(get_db)):

    result = await CommentService().delete(comment_id, current_user, session)

    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Comment with ID '{comment_id}' does not exist.")
    elif not result:
        raise HTTPException(
            status_code=401, detail=f"Comment with ID '{comment_id} does not belong to user'{current_user.id}'"
        )
    else:
        return result
