from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.model_user import User
from app.core.dependencies import get_current_user
from app.services.service_tag import TagService

router_tag = APIRouter(prefix='/tag', tags=['Tag'])


@router_tag.post('/create_tag')
async def create_tag(name: str,
                     current_user: User = Depends(get_current_user),
                     session: AsyncSession = Depends(get_db)):
    result = await TagService().create(name, session)
    if not result:
        raise HTTPException(
            status_code=400, detail=f"Tag with name '{name}' already exist.")
    else:
        return result


@router_tag.get('/get_all')
async def get_all(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_db)):
    return await TagService().get_all(session)


@router_tag.get('/get_by_id')
async def get_by_id(tag_id: int,
                    current_user: User = Depends(get_current_user),
                    session: AsyncSession = Depends(get_db)):
    result = await TagService().get_by_id(tag_id, session)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=404, detail=f"Tag with ID '{tag_id}' not found.")


@router_tag.put('/update')
async def update(tag_id: int,
                 new_tag: str,
                 current_user: User = Depends(get_current_user),
                 session: AsyncSession = Depends(get_db)):
    result = await TagService().update(tag_id=tag_id, new_tag=new_tag, session=session)
    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Tag with name '{tag_id}' not found.")
    else:
        return result


@router_tag.delete('/delete')
async def delete(tag_id: int,
                 current_user: User = Depends(get_current_user),
                 session: AsyncSession = Depends(get_db)):
    result = await TagService().delete(tag_id=tag_id, session=session)
    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Tag with ID '{tag_id}' not found.")
    else:
        return result


@router_tag.post('/assign_tag_to_post')
async def assign_tag_to_post(tag_id: int,
                             post_id: int,
                             current_user: User = Depends(get_current_user),
                             session: AsyncSession = Depends(get_db)):
    result = await TagService().assign_tag_to_post(tag_id=tag_id, post_id=post_id, session=session)
    if result is False:
        raise HTTPException(
            status_code=404, detail=f"Either tag or id does not exist.")
    if result is None:
        raise HTTPException(
            status_code=400, detail=f"Tag '{tag_id}' with Post '{post_id}' already exists.")

    return result


@router_tag.delete('/remove_tag_from_post')
async def remove_tag_from_post(tag_id: int,
                               post_id: int,
                               current_user: User = Depends(get_current_user),
                               session: AsyncSession = Depends(get_db)):
    result = await TagService().remove_tag_from_post(tag_id=tag_id, post_id=post_id, session=session)
    if result:
        return result
    else:
        raise HTTPException(
            status_code=404, detail="Tag-post assignment not found.")
