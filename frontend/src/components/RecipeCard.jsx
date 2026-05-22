export default function RecipeCard({recipe, onClick}){
    return (
        <div className="bg-white rounded-lg shadow p-4 cursor-pointer hover:shadow-lg transition" onClick={onClick}>
            <h2 className="text-xl font-semibold"><b>{recipe.name}</b></h2>
            <p className="text-gray-600">{recipe.category} · {recipe.area}</p>
            <p className="text-gray-400 text-sm">{recipe.author}</p>
        </div>
    )
}
