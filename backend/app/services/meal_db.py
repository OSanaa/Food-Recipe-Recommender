import httpx
import asyncio

async def fetch_meals_by_name(search):
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={search}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()

def transform_meal_to_recipe(meal):
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

# meals = asyncio.run(fetch_meals_by_name('chicken'))
# for meal in meals['meals']:
#     meals_formatted = transform_meal_to_recipe(meal)