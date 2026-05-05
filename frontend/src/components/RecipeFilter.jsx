export default function RecipeFilter({areas, categories, selectedArea, selectedCategory, setSelectedArea, setSelectedCategory}){
    return (
    <div className="recipeFilter">
        <label>Pick an area: 
            <select
            value={selectedArea}
            onChange={e => setSelectedArea(e.target.value)}>
                <option value="">All Areas</option>
                {areas.map(area => (
                    <option key={area} value={area}>{area}</option>
                ))}
            </select>
        </label>
        <br/>
        <label>Pick a category: 
            <select
            value={selectedCategory}
            onChange={e => setSelectedCategory(e.target.value)}>
                <option value="">All Categories</option>
                {categories.map(category => (
                    <option key={category} value={category}>{category}</option>
                ))}
            </select>
        </label>
    </div>
    )
}