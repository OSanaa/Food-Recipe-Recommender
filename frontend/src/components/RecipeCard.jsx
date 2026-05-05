export default function RecipeCard({recipe, onClick}){
    return (
        <div className = "card" onClick={onClick}>
            <h2><b>{recipe.name}</b></h2>
            <p>{recipe.category}</p>
            <p>{recipe.area}</p>
            <p>{recipe.author}</p>
        </div>
    )
}
