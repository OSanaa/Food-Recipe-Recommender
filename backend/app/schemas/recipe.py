from pydantic import BaseModel

class RecipeCreate(BaseModel):
    name: str 
    instructions: str
    link: str | None = None
    author: str
    source: str

class RecipeResponse(RecipeCreate):
    id: int