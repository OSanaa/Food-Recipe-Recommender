from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_session
from app.services.embeddings import generate_embedding, build_recipe_text
from app.schemas.recipe import RecipeResponse
from app.models.recipe import Recipe

router = APIRouter()

@router.post("/create_embeddings")
async def create_embeddings(db: AsyncSession = Depends(get_session)):
    query = select(Recipe).options(selectinload(Recipe.ingredients))
    result = await db.execute(query)
    recipes = result.scalars().all()
    
    for recipe in recipes:
        recipe_text = build_recipe_text(recipe)
        embedding = generate_embedding(recipe_text)
        if recipe.embedding == None:
            recipe.embedding = embedding

    await db.commit()
    return(f"Text embeddings have been added")

@router.get("/recipes/{id}/similar", response_model=list[RecipeResponse])
async def get_similar_recipe_recommendations(id : int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(
        select(Recipe).options(selectinload(Recipe.ingredients)).where(Recipe.id == id)
    )
    recipe = result.scalars().first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    if recipe.embedding is None:
        raise HTTPException(status_code=404, detail="Recipe does not have text embeddings enabled")
    
    similar_result = await db.execute(
        select(Recipe).options(selectinload(Recipe.ingredients)).order_by(Recipe.embedding.l2_distance(recipe.embedding)).offset(1).limit(5)
    ) 
    similar_recipe = similar_result.scalars().all()
    return(similar_recipe)