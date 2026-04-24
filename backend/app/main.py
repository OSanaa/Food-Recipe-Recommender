from fastapi import FastAPI
from app.routes.recipe import router as recipe_router
from app.routes.meal_db import router as meal_db_router
from app.routes.cooking_log import router as cooking_log_db_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Food Recipe Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Recipe Recommender API"}

app.include_router(recipe_router)
app.include_router(meal_db_router)
app.include_router(cooking_log_db_router)