from fastapi import FastAPI
from app.routes.recipe import router

app = FastAPI(title="Food Recipe Recommender API")

@app.get("/")
def read_root():
    return {"message": "Recipe Recommender API"}

app.include_router(router)
