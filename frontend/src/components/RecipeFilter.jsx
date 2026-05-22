export default function RecipeFilter({areas, categories, selectedArea, selectedCategory, setSelectedArea, setSelectedCategory}){
    return (
    <div className="recipeFilter flex gap-4 ">
        <select
        className="mr-2 border rounded pl-2 py-1.5 px-1 cursor-pointer text-black text-sm font-medium"
        value={selectedArea}
        onChange={e => setSelectedArea(e.target.value)}>
            <option value="">All Areas</option>
            {areas.map(area => (
                <option key={area} value={area}>{area}</option>
            ))}
        </select>
        <select
        className="mr-2 border rounded pl-2 py-1.5 px-1 cursor-pointer text-black text-sm font-medium"
        value={selectedCategory}
        onChange={e => setSelectedCategory(e.target.value)}>
            <option value="">All Categories</option>
            {categories.map(category => (
                <option key={category} value={category}>{category}</option>
            ))}
        </select>
    </div>
    )
}