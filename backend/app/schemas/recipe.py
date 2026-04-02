from pydantic import BaseModel, ConfigDict

class IngredientCreate(BaseModel):
    name: str
    quantity: str | None = None
    unit: str | None = None

class RecipeCreate(BaseModel):
    name: str 
    instructions: str
    link: str | None = None
    author: str
    area: str | None = None
    category: str | None = None
    source: str
    ingredients: list[IngredientCreate] = []

class IngredientResponse(BaseModel):
    id: int
    name: str
    quantity: str | None = None
    unit: str | None = None

class RecipeResponse(RecipeCreate):
    id: int
    ingredients: list[IngredientResponse] = []
    model_config = ConfigDict(from_attributes=True)