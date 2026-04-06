from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_session
from app.models.recipe import Recipe, Ingredient
from app.schemas.recipe import RecipeCreate, RecipeResponse, IngredientCreate, IngredientResponse

router = APIRouter()

@router.post("/recipes", response_model=RecipeResponse)
async def create_recipe(recipe: RecipeCreate, db: AsyncSession = Depends(get_session)):
    recipe_dict = recipe.model_dump()
    new_ingredients_list = recipe_dict.pop("ingredients")
    new_recipe = Recipe(**recipe_dict)
    existing = await db.execute(
            select(Recipe).where(Recipe.name == new_recipe.name)
            )
    if existing.scalars().first():
        raise HTTPException(status_code=409, detail="Recipe already exists")
    db.add(new_recipe)
    await db.flush()
    for ingredient in new_ingredients_list:
        ingredient['recipe_id'] = new_recipe.id
        db.add(Ingredient(**ingredient))
    await db.commit()
    await db.refresh(new_recipe)
    return(new_recipe)

@router.get("/recipes", response_model=list[RecipeResponse])
async def get_all_recipes(area: str | None = None, category: str | None = None, db: AsyncSession = Depends(get_session)):
    query = select(Recipe).options(selectinload(Recipe.ingredients))
    if area:
        query = query.where(Recipe.area == area)
    if category:
        query = query.where(Recipe.category == category)
    result = await db.execute(query)
    return(result.scalars().all())

@router.get("/recipes/{id}",response_model=RecipeResponse)
async def get_recipe_by_id(id : int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(Recipe).options(selectinload(Recipe.ingredients)).where(Recipe.id == id)
        )
    recipe = result.scalars().first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")    
    return(recipe)

@router.delete("/recipes/{id}")
async def delete_recipe_by_id(id: int, db: AsyncSession = Depends(get_session)):
    delete_recipe = await db.get(Recipe, id)
    if not delete_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    await db.delete(delete_recipe)
    await db.commit()
    return(f"Recipe with ID: {id} has been deleted")

@router.put("/recipes/{id}", response_model=RecipeResponse)
async def update_recipe_by_id(id: int, updated_recipe: RecipeCreate, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(Recipe).options(selectinload(Recipe.ingredients)).where(Recipe.id == id)
        )
    recipe_to_update = result.scalars().first()
    if not recipe_to_update:
        raise HTTPException(status_code=404, detail="Recipe not found")
    updated_recipe_dict = updated_recipe.model_dump()
    for key,value in updated_recipe_dict.items():
        setattr(recipe_to_update, key, value)
    
    await db.commit()
    await db.refresh(recipe_to_update)

    return(recipe_to_update)
