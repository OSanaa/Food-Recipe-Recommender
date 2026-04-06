from pydantic import BaseModel, ConfigDict
from datetime import datetime

class IngredientCreate(BaseModel):
    name: str
    quantity: str | None = None
    unit: str | None = None

class CookingLogCreate(BaseModel):
    date_cooked: datetime
    notes: str | None = None
    rating: float
    recipe_id: int

class RecipeCreate(BaseModel):
    name: str 
    instructions: str
    link: str | None = None
    author: str
    area: str | None = None
    category: str | None = None
    source: str
    ingredients: list[IngredientCreate] = []
    # cooking_log: list[CookingLogCreate] = []

class IngredientResponse(BaseModel):
    id: int
    name: str
    quantity: str | None = None
    unit: str | None = None

class RecipeResponse(RecipeCreate):
    id: int
    ingredients: list[IngredientResponse] = []
    model_config = ConfigDict(from_attributes=True)

