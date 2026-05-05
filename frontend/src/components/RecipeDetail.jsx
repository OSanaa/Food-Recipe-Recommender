export default function RecipeDetail({recipe, onBack}){
    return (
        <div className = "detail">
            <button onClick={onBack}>Back</button>
            <h3>Ingredients and Instructions for {recipe.name}</h3>
            <ul>
                {recipe.ingredients.map(ing => (
                    <li key={ing.id}>{ing.quantity} {ing.name} </li>))
                }
            </ul>
            <p>{recipe.instructions}</p>
        </div>
    )
}