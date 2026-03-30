from fastapi import FastAPI

app = FastAPI(title="Food Recipe Recommender API")

@app.get("/")
def read_root():
    return {"message": "Recipe Recommender API"}