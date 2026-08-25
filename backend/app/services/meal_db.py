import httpx
import asyncio

async def fetch_meals_by_name(search):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={search}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()

def transform_meal_to_recipe(meal):
    """Convert a raw TheMealDB meal dict into a recipe and ingredient structure.

    Reads the 20 flat strIngredient/strMeasure slots and folds the non-empty
    ones into a list, discarding empty padding slots. Does not deduplicate.

    Args:
        meal: A single TheMealDB meal dict that excludes the {"meals": [...]} envelope.
              Must contain all 20 strIngredient/strMeasure keys.

    Returns:
        A (recipe, ingredients) tuple: recipe is a dict of scalar fields;
        recipe is a dict of recipe metadata;
        ingredients is a list of {"name", "quantity", "unit"} dicts.
    """
    recipe = {
        "name" : meal['strMeal'],
        "instructions": meal['strInstructions'],
        "link": meal['strSource'],
        'author': 'Author Unknown',
        'area': meal['strArea'],
        'category': meal['strCategory'],
        'source': 'themealdb'
        }

    ingredients = []
    for i in range(1,21):        
        if meal[f'strIngredient{i}'] not in (None, "", " "):        
            temp_dict = {
                "name": meal[f"strIngredient{i}"],
                "quantity": meal[f"strMeasure{i}"],
                "unit": None
                }
            ingredients.append(temp_dict)
    print(ingredients)
    return(recipe, ingredients)