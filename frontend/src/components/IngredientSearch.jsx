import { useState, useEffect } from 'react'
import RecipeDetail from "./RecipeDetail"

export default function IngredientSearch({ onSelectRecipe }) {
    const [allIngredients, setAllIngredients] = useState([])
    const [selected, setSelected] = useState([])
    const [matches, setMatches] = useState([])
    const [ingredientFilter, setIngredientFilter] = useState("")

    // Fetch all ingredients once on mount
    useEffect(() => {
        fetch("http://localhost:8000/ingredients")
            .then(res => res.json())
            .then(data => setAllIngredients(data))
    }, [])

    // Re-fetch matches whenever selection changes
    useEffect(() => {
        if (selected.length === 0) {
            setMatches([])
            return
        }

        fetch("http://localhost:8000/ingredients/match", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ingredients: selected })
        })
            .then(res => res.json())
            .then(data => setMatches(data))
    }, [selected])

    const toggleIngredient = (name) => {
        if (selected.includes(name)){
            setSelected(selected.filter(ing => ing !== name))
        } else {
            setSelected(prevItems => [...prevItems, name]);
        };
    }

    const handleRecipeClick = (recipeId) => {
        fetch(`http://localhost:8000/recipes/${recipeId}`)
        .then(response => response.json())
        .then(data => {onSelectRecipe(data)
        })
    }

    return (
        <div className="flex gap-6 pt-5">
            <div className="w-1/4 border-r pr-4">
                <h3 className="text-xl font-medium mb-2">Ingredients</h3>
                <input
                    className="w-full px-3 py-2 border rounded text-sm mb-3"
                    placeholder="Filter ingredients..."
                    value={ingredientFilter}
                    onChange={e => setIngredientFilter(e.target.value)}
                />
                <div className="max-h-[70vh] overflow-y-auto space-y-1">
                    {allIngredients
                        .filter(ing => ing.toLowerCase().includes(ingredientFilter.toLowerCase()))
                        .map(ing => (
                            <button
                                key={ing}
                                onClick={() => toggleIngredient(ing)}
                                className={`block w-full text-left px-2 py-1 rounded text-sm cursor-pointer ${
                                    selected.includes(ing)
                                        ? "bg-apricot-cream font-medium"
                                        : "hover:bg-gray-100"
                                }`}
                            >
                                {ing}
                            </button>
                        ))
                    }
                </div>
            </div>

            <div className="w-3/4">
                <h3 className="text-xl font-medium mb-2">
                    Matching Recipes {selected.length > 0 && `(${selected.length} selected)`}
                </h3>
                {matches.length === 0 ? (
                    <p className="text-gray-400">Select ingredients to see matching recipes</p>
                ) : (
                    <div className="space-y-3">
                        {matches.map(match => (
                            <div
                                key={match.id}
                                onClick={() => handleRecipeClick(match.id)}
                                className="bg-white rounded-lg shadow p-4 cursor-pointer hover:shadow-lg transition"
                            >
                                <h4 className="text-lg font-semibold">{match.recipe_name}</h4>
                                <p className="text-gray-600 text-sm">
                                    {match.ingredient_match_count} of {match.total_ingredient_count} ingredients · {match.percentage_matched}% match
                                </p>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}