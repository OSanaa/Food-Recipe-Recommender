from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_session
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeResponse

router = APIRouter()

@router.post("/recipes")
async def create_recipe(recipe: RecipeCreate, db: AsyncSession = Depends(get_session)):
    new_recipe = Recipe(**recipe.model_dump())
    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)
    return(new_recipe)

@router.get("/recipes")
async def get_all_recipes(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Recipe))
    return(result.scalars().all())

@router.get("/recipes/{id}")
async def get_recipe_by_id(id : int, db: AsyncSession = Depends(get_session)):
    
    result = await db.get(Recipe, id)    
    if not result:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return(result)

@router.delete("/recipes/{id}")
async def delete_recipe_by_id(id: int, db: AsyncSession = Depends(get_session)):
    delete_recipe = await db.get(Recipe, id)
    if not delete_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")    
    await db.delete(delete_recipe)
    await db.commit()
    return(f"Recipe with ID: {id} has been deleted")

@router.put("/recipes/{id}")
async def update_recipe_by_id(id: int, updated_recipe: RecipeCreate, db: AsyncSession = Depends(get_session)):
    recipe_to_update = await db.get(Recipe, id)
    if not recipe_to_update:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    updated_recipe_dict = updated_recipe.model_dump()
    for key,value in updated_recipe_dict.items():
        setattr(recipe_to_update, key, value)
    
    await db.commit()
    await db.refresh(recipe_to_update)

    return(recipe_to_update)
