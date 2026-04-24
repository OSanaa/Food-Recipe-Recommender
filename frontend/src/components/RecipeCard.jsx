export default function RecipeCard({recipe}){
    return (
        <div className = "card">
            <h2><b>{recipe.name}</b></h2>
            <p>{recipe.category}</p>
            <p>{recipe.area}</p>
            <p>{recipe.author}</p>
        </div>
    )
}
