import { useState } from 'react'
import { useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import RecipeCard from './components/RecipeCard'
import RecipeDetail from './components/RecipeDetail'
import RecipeFilter from './components/RecipeFilter'
import RecipeForm from './components/RecipeForm'
import './App.css'

function App() {
  const [recipes, setRecipes] = useState([])
  const [selectedArea, setSelectedArea] = useState('')
  const [areas, setAreas] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('')
  const [categories, setCategories] = useState([])
  const [selectedRecipe, setSelectedRecipe] = useState(null)
  const [search, setSearch] = useState("")
  const [showForm, setShowForm] = useState(false)


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
    <div>
      <h1>Food Recipe Recommender</h1>
      {showForm ? (<RecipeForm onBack={() => setShowForm(false)} onSubmitSuccess={fetchRecipes}/>
      ) : selectedRecipe ? (
      <RecipeDetail recipe={selectedRecipe} onBack={() => setSelectedRecipe(null)} />
      ) : (
      <div>
        <button onClick={() => setShowForm(!showForm)}>Create Recipe</button>
        <br/>
        <input type='text'
        placeholder='Search recipes'
        value={search}
        onChange={e => setSearch(e.target.value)}/>
        <RecipeFilter areas={areas}
        categories={categories}
        selectedArea={selectedArea}
        selectedCategory={selectedCategory}
        setSelectedArea={setSelectedArea}
        setSelectedCategory={setSelectedCategory}/>
        
        {recipes
        .filter(recipe => recipe.name.toLowerCase().includes(search.toLowerCase()))
        .map(recipe => (
          <RecipeCard key={recipe.id}
          recipe={recipe}
          onClick={() => setSelectedRecipe(recipe)}/>
          ))
        }
      </div>
        )}    
    </div>
  )
}

export default App
