from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case, cast, Numeric
from sqlalchemy.orm import selectinload
from app.database import get_session
from app.models.recipe import Recipe, Ingredient
from app.schemas.recipe import RecipeCreate, RecipeResponse, IngredientSearch, IngredientMatchResponse

router = APIRouter()

@router.get("/ingredients")
async def get_distinct_ingredients(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Ingredient.name).distinct().order_by(Ingredient.name))
    return result.scalars().all()

@router.post("/ingredients/match", response_model=list[IngredientMatchResponse])
async def ingredient_match(ingredient_list: IngredientSearch, db: AsyncSession = Depends(get_session)):

    ingredients = ingredient_list.ingredients
    
    matched = func.sum(
        case((Ingredient.name.in_(ingredients), 1), else_=0)
        )

    pct = func.round(cast(100.0 * matched / func.count(), Numeric), 2)

    query = (
        select(
            Recipe.id,
            Recipe.name.label("recipe_name"),
            func.count().label("total_ingredient_count"),
            matched.label("ingredient_match_count"),
            pct.label("percentage_matched")
        )
        .join(Ingredient, Recipe.id == Ingredient.recipe_id)
        .group_by(Recipe.id)
        .having(matched > 0)
        .order_by(pct.desc())
        .limit(10)
    )

    result = await db.execute(query)
    rows = result.all()

    return rows