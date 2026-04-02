from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.meal_db import fetch_meals_by_name, transform_meal_to_recipe
from app.database import get_session
from app.models.recipe import Recipe, Ingredient

router = APIRouter()

@router.post("/meals/search/{search_term}")
async def upload_api_recipe(search_term: str, db: AsyncSession = Depends(get_session)):
    meals = await fetch_meals_by_name(search_term)
    for meal in meals['meals']:
        recipe_formatted, ingredients_formatted = transform_meal_to_recipe(meal)
        existing = await db.execute(
            select(Recipe).where(Recipe.name == recipe_formatted["name"])
            )
        
        if existing.scalars().first():
            continue
        else:
            new_recipe = Recipe(**recipe_formatted)
            db.add(new_recipe)
            await db.flush()
            for ingredient in ingredients_formatted:
                ingredient['recipe_id'] = new_recipe.id
                new_ingredient = Ingredient(**ingredient)
                db.add(new_ingredient)
    
    await db.commit()
    return {"message": f"Recipes for '{search_term}' saved successfully"}