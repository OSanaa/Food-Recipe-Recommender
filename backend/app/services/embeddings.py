from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(recipe_text: str):
    return model.encode(recipe_text).tolist()

def build_recipe_text(recipe):
    ingredients = " ".join([ing.name for ing in recipe.ingredients])
    return f"{recipe.name} {recipe.category} {recipe.area} {ingredients}"