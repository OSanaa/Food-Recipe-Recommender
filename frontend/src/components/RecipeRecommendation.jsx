import { useState } from "react"
import { useEffect } from "react"
import RecipeCard from './RecipeCard'
import RecipeDetail from "./RecipeDetail"

export default function RecipeRecommendation({recipe_id, onClick}){
      const [recipeRecommendationList, setRecipeRecommendationList] = useState([])
    //   const [selectedRecipe, setSelectedRecipe] = useState(null)

      useEffect(() => {
        fetchRecommendedRecipe()
      }, [recipe_id])

      const fetchRecommendedRecipe = () => {
        fetch(`http://localhost:8000/recipes/${recipe_id}/similar`)
        .then(res => res.json())
        .then(data => setRecipeRecommendationList(data))
      }

    return (
        <div>
            <h3 className='text-xl font-medium'>More like this:</h3>
            <div className="grid gird-cols-5 gap-4">
                {recipeRecommendationList.map(recipe => (
                    // <p> {recipe.name}</p>
                    <RecipeCard key={recipe.id}
                    recipe={recipe}
                    onClick={() => onClick(recipe)}/>
                ))}
            </div>
        </div>
    )
}
