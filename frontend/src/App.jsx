import { useState } from 'react'
import { useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import RecipeCard from './components/RecipeCard'
import RecipeDetail from './components/RecipeDetail'
import RecipeFilter from './components/RecipeFilter'
import RecipeForm from './components/RecipeForm'
import IngredientSearch from './components/IngredientSearch'

function App() {
  const [recipes, setRecipes] = useState([])

  const [selectedArea, setSelectedArea] = useState('')
  const [areas, setAreas] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('')
  const [categories, setCategories] = useState([])
  const [selectedRecipe, setSelectedRecipe] = useState(null)
  const [search, setSearch] = useState("")
  const [showForm, setShowForm] = useState(false)
  const [view, setView] = useState("browse")

  const fetchRecipes = () => {
    let url = "http://localhost:8000/recipes"
    const params = []
    if (selectedArea) params.push(`area=${selectedArea}`)
    if (selectedCategory) params.push(`category=${selectedCategory}`)
    if (params.length > 0) url += "?" + params.join("&")

    fetch(url)
      .then(response => response.json())
      .then(data => setRecipes(data))
  }

  useEffect(() => {

    let areaUrl = "http://localhost:8000/recipes/areas"
    fetch(areaUrl)
    .then(response => response.json())
    .then(data => setAreas(data))

    let categoryUrl = "http://localhost:8000/recipes/categories"
    fetch(categoryUrl)
    .then(response => response.json())
    .then(data => setCategories(data))
    fetchRecipes()

  }, [selectedArea, selectedCategory])


  return (
    <div className="bg-white p-6 pt-15">
      <nav className="border-b w-full z-20 top-0 start-0 border-default fixed bg-white p-4 flex justify-between items-center">
        <h1 className="self-center text-burnt-beat text-xl text-heading font-serif whitespace-nowrap">
          Food Recipe Recommender
        </h1>
        <div className="flex items-center gap-4">
          <button className="mr-2 bg-apricot-cream/50 hover:bg-apricot-cream cursor-pointer text-black text-sm font-medium  py-1.5 px-3 rounded"
          onClick={() => { setView("form"); setSelectedRecipe(null) }}>
            Create Recipe
          </button>
          <button className="mr-2 bg-apricot-cream/50 hover:bg-apricot-cream cursor-pointer text-black text-sm font-medium py-1.5 px-3 rounded"
          onClick={() => { setView("ingredientSearch"); setSelectedRecipe(null) }}>
            Ingredient Search
          </button>
          {view === "browse" && !selectedRecipe && (
            <RecipeFilter areas={areas}
            categories={categories}
            selectedArea={selectedArea}
            selectedCategory={selectedCategory}
            setSelectedArea={setSelectedArea}
            setSelectedCategory={setSelectedCategory}/>
          )}
        <input type='text'
          className="mr-2 pl-2 pr-1 py-1 border rounded text-black" 
          placeholder='Search recipes'
          value={search}
          onChange={e => setSearch(e.target.value)}/>
        </div>
      </nav>
      <div>
        {selectedRecipe ? (
          <RecipeDetail recipe={selectedRecipe} onBack={() => setSelectedRecipe(null)} onClick={(recipe) => setSelectedRecipe(recipe)}/>
        ) : view === "form" ? (
          <RecipeForm onBack={() => setView("browse")} onSubmitSuccess={fetchRecipes}/>
        ) : view === "ingredientSearch" ? (
          <IngredientSearch onSelectRecipe={(recipe) => setSelectedRecipe(recipe)} />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4 pt-5">
            {recipes
              .filter(recipe => recipe.name.toLowerCase().includes(search.toLowerCase()))
              .map(recipe => (
                <RecipeCard key={recipe.id} recipe={recipe} onClick={() => setSelectedRecipe(recipe)}/>
              ))
            }
          </div>
      )}
      </div>
    </div>
  )
}

export default App
