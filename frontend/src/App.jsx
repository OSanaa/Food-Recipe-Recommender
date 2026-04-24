import { useState } from 'react'
import { useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import RecipeCard from './components/RecipeCard'
import './App.css'

function App() {
  const [recipes, setRecipes] = useState([])
  const [area, setArea] = useState("")
  const [category, setCategory] = useState("")
  useEffect(() => {
    let url = "http://localhost:8000/recipes"
    const params = []
    if (area) params.push(`area=${area}`)
    if (category) params.push(`category=${category}`)
    if (params.length > 0) url += "?" + params.join("&")

    fetch(url)
      .then(response => response.json())
      .then(data => setRecipes(data))
  }, [area, category])

  return (
    <div>
      <h1>Food Recipe Recommender</h1>
      <label>
        Pick an area: 
        <select
        name="area"
        onChange={e => setArea(e.target.value)}
        >
          <option value="">All Areas</option>
          <option value="Japanese">Japanese</option>
          <option value="Italian">Italian</option>
        </select>
      </label>
      <hr />
      <label>
        Pick a category: 
        <select
        name="category"
        onChange={e => setCategory(e.target.value)}
        >
          <option value="">All Categories</option>
          <option value="Chicken">Chicken</option>
          <option value="Seafood">Seafood</option>
        </select>
      </label>
      {recipes.map(recipe => (
        <RecipeCard key={recipe.id} recipe={recipe}/>
      ))}
    </div>
  )
}

export default App
