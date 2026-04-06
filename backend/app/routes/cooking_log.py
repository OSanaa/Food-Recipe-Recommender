from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_session
from app.models.recipe import Recipe, CookingLog
from app.schemas.cooking_log import CookingLogCreate, CookingLogResponse


router = APIRouter()

@router.post("/cooking-logs", response_model=CookingLogResponse)
async def create_new_cooking_log(cooking_log: CookingLogCreate, db: AsyncSession = Depends(get_session)):
    new_cooking_log = CookingLog(**cooking_log.model_dump())
    db.add(new_cooking_log)
    await db.commit()
    await db.refresh(new_cooking_log)
    return(new_cooking_log)

@router.get("/cooking-logs", response_model=list[CookingLogResponse])
async def get_all_cooking_log(recipe_id: int | None = None, db: AsyncSession = Depends(get_session)):
    query = select(CookingLog)
    if recipe_id:
        query = query.where(CookingLog.recipe_id == recipe_id)
    result = await db.execute(query)
    return (result.scalars().all())

@router.get("/cooking-logs/{id}", response_model=CookingLogResponse)
async def get_cooking_log_by_id(id : int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(CookingLog).where(CookingLog.id == id))
    cooking_log = result.scalars().first()
    if not cooking_log:
        raise HTTPException(status_code=404, detail="Cooking log not found")
    return(cooking_log)

@router.delete("/cooking-logs/{id}")
async def delete_cooking_logs_by_id(id: int, db: AsyncSession = Depends(get_session)):
    delete_cooking_logs = await db.get(CookingLog, id)
    if not delete_cooking_logs:
        raise HTTPException(status_code=404, detail="Cooking log not found")
    await db.delete(delete_cooking_logs)
    await db.commit()
    return(f"Cooking log with ID: {id} has been deleted")

@router.put("/cooking-logs/{id}", response_model=CookingLogResponse)
async def update_recipe_by_id(id: int, updated_cooking_log: CookingLogCreate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(CookingLog).where(CookingLog.id == id)
        )
    cooking_log_to_update = result.scalars().first()
    if not cooking_log_to_update:
        raise HTTPException(status_code=404, detail="Cooking Log not found")
    updated_cooking_log_dict = updated_cooking_log.model_dump()
    for key,value in updated_cooking_log_dict.items():
        setattr(cooking_log_to_update, key, value)
    await db.commit()
    await db.refresh(cooking_log_to_update)
    return(cooking_log_to_update)
