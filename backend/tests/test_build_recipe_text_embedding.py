"""Unit tests for the recipe text embedding logic."""

import pytest
from app.services.embeddings import build_recipe_text

class RecipeObjectTest:

    def __init__(self, name, category, area, ingredients=None):
        self.name = name
        self.category = category
        self.area = area
        self.ingredients = ingredients if ingredients is not None else []

class IngredientObjectTest:

    def __init__(self, name, measure=0, unit=0):
        self.name = name
        self.measure = measure
        self.unit = unit

def ingredient_helper(test_ingredients):
    """Build a Ingredients shaped object populated based on parameter
    
    Fills multiple Ingredient Objects based on the number of ingredients indicated 
    or an empty if 0 is passed.
    """
    return [IngredientObjectTest(name=i) for i in test_ingredients]

@pytest.mark.parametrize("recipe_object, ingredient_object, expected_recipe_text", [
    pytest.param(RecipeObjectTest(name="Spaghetti and Meatballs", category="Pasta", area="Italian"),
                ["Meatballs", "Onion", "Spaghetti Noodles"], 
                "Spaghetti and Meatballs Pasta Italian Meatballs Onion Spaghetti Noodles",
                id="happy_path"
                ),
    pytest.param(RecipeObjectTest(name="Spaghetti and Meatballs", category="Pasta", area="Italian"),
                [],
                "Spaghetti and Meatballs Pasta Italian ",  # trailing space: " ".join([]) == ""
                id="empty_ingredients",
                ),
    pytest.param(RecipeObjectTest(name="Spaghetti and Meatballs", category="Pasta", area=None),
                ["Meatballs", "Onion", "Spaghetti Noodles"],
                "Spaghetti and Meatballs Pasta None Meatballs Onion Spaghetti Noodles",  # TODO: None leaks into embedding text
                id="none_area",
                ),
    ])
def test_build_recipe_text(recipe_object, ingredient_object, expected_recipe_text):
    recipe_object.ingredients = ingredient_helper(ingredient_object)
    recipe_text = build_recipe_text(recipe_object)
    assert recipe_text == expected_recipe_text

