"""Unit tests for the TheMealDB → recipe transformation logic.""" 

import pytest
from app.services.meal_db import transform_meal_to_recipe

@pytest.fixture
def meal():
    return {
        "idMeal": "53483",
        "strMeal": "Acaraje black-eyed pea fritters with shrimp filling",
        "strMealAlternate": None,
        "strCategory": "Seafood",
        "strArea": None,
        "strCountry": "Brazil",
        "strInstructions": "step 1\r\nMake the filling by placing the onion, ginger, garlic, chilli, and some salt into food processor. Pur\u00e9e until smooth. Heat the oil in a frying pan and pour the pur\u00e9e into it. Fry for 5 mins or until cooked through. Add the prawns, tomatoes and chopped coriander. Squeeze in the lime and add salt to taste. Cook for 3 mins, or until the prawns have cooked through. Remove from the heat.\r\n\r\nstep 2\r\nDrain and rinse the black-eyed peas. Pour into a food processor with the garlic and chili. Pur\u00e9e until smooth. Scrape into a bowl and add the onion, flour, salt, chilli powder and baking powder. Mix and roll into 16 balls.\r\n\r\nstep 3\r\nHeat the oven to 190C/170C fan/gas 5. Heat 8cm of the palm or vegetable oil in a wok or small heavy pan. When a small piece of bread sizzles, drop 4-5 balls into the oil. Fry until golden and crisp, about 4-5 mins. Drain on kitchen paper and repeat until they are all finished. You can keep them warm in the oven while you finish. Slice the fritters open down the centre and spoon the prawn filling in. Serve with hot sauce.",
        "strMealThumb": "https:www.themealdb.com/images/media/meals/dxs5t71782678369.jpg",
        "strTags": None,
        "strYoutube": "",
        "strIngredient1": "Black Eyed Peas",
        "strIngredient2": "Garlic",
        "strIngredient3": "Green Chilli",
        "strIngredient4": "Red Onions",
        "strIngredient5": "Plain Flour",
        "strIngredient6": "Salt",
        "strIngredient7": "Chilli Powder",
        "strIngredient8": "Baking Powder",
        "strIngredient9": "Vegetable Oil",
        "strIngredient10": "Red Onions",
        "strIngredient11": "Ginger",
        "strIngredient12": "Garlic",
        "strIngredient13": "Red Chilli",
        "strIngredient14": "Raw tiger prawns",
        "strIngredient15": "Vegetable Oil",
        "strIngredient16": "Plum Tomatoes",
        "strIngredient17": "Coriander",
        "strIngredient18": "Lime",
        "strIngredient19": "",
        "strIngredient20": "",
        "strMeasure1": "800g",
        "strMeasure2": "1 clove",
        "strMeasure3": "1",
        "strMeasure4": "1 small finely diced",
        "strMeasure5": "2 tablespoons",
        "strMeasure6": "1 tsp",
        "strMeasure7": "1 tsp",
        "strMeasure8": "1 tsp",
        "strMeasure9": "For frying",
        "strMeasure10": "1 sliced",
        "strMeasure11": "1 tablespoon chopped",
        "strMeasure12": "2 cloves",
        "strMeasure13": "1 chopped",
        "strMeasure14": "150g",
        "strMeasure15": "1 tablespoon",
        "strMeasure16": "2",
        "strMeasure17": "1 tablespoon chopped",
        "strMeasure18": "Juice of 1",
        "strMeasure19": "",
        "strMeasure20": "",
        "strSource": "https://www.bbcgoodfood.com/recipes/caraje-black-eyed-pea-fritters-shrimp-filling",
        "strImageSource": None,
        "strCreativeCommonsConfirmed": None,
        "dateModified": "2026-06-28 21:24:02"
    }

def meal_helper(filled=None):
    """Build a TheMealDB shaped meal dict with all 20 slots present.

    Fills the first N strIngredient/strMeasure slots from `filled` and leaves
    the rest empty, so a test can declare only the ingredients it cares about.
    """
    filled = filled or [] # [] if filled is None
    ingredients = {f"strIngredient{i}": "" for i in range (1,21)}
    measure = {f"strMeasure{i}": "" for i in range (1,21)}
    recipe_filler = {"strMeal": "Recipe 1 Name",
                     "strInstructions": "step 1: Bake",
                     "strSource" : "recipeFoodRecs.com",
                     "strArea": None,
                     "strCategory": "Seafood",
                    }

    meal_filler = recipe_filler | ingredients | measure 

    for i, value in enumerate(filled, start=1):
        meal_filler[f"strIngredient{i}"] = value
        meal_filler[f"strMeasure{i}"] = "1 tbsp"

    return meal_filler

def test_meal_transform_success(meal):    
    recipe, ingredients = transform_meal_to_recipe(meal)
    assert recipe["name"] == "Acaraje black-eyed pea fritters with shrimp filling"
    assert recipe["category"] == "Seafood"

def test_transform_excludes_empty_ingredients(meal):
    # 20 slots, 2 empty, no dedupe -> 18. The duplicates are intentional.
    recipe, ingredients = transform_meal_to_recipe(meal)
    assert len(ingredients) == 18

@pytest.mark.parametrize("ingredient_names, expected_count", [
    pytest.param(["Fries", "Patty", "Bun"], 3, id="three_ingredients"),
    pytest.param([], 0, id="empty"),
    pytest.param(["Garlic","Garlic"], 2, id="duplicates")
])
def test_transform_meal_count(ingredient_names, expected_count):
    meal_filler = meal_helper(ingredient_names)
    recipe, ingredients = transform_meal_to_recipe(meal_filler)
    assert len(ingredients) == expected_count