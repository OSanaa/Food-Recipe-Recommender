import { useState } from 'react'
import { useEffect } from 'react'
import RecipeRecommendation from './RecipeRecommendation';

export default function RecipeDetail({recipe, onBack, onClick}){
    const [logs, setLogs] = useState([])
    const [formData, setFormData] = useState({
        date_cooked: new Date().toISOString().slice(0, 16),
        rating: 0.0,
        notes: '',
        recipe_id: recipe.id
    });
    const [recipeRecommendation, setRecipeRecommendation] = useState([])

    // useEffect(() => {
    //     fetch(`http://localhost:8000/cooking-logs?recipe_id=${recipe.id}`)
    //     .then(res => res.json())
    //     .then(data => setLogs(data))
    // }, [recipe.id])
    useEffect(() => {
        fetchLogs()
        window.scrollTo(0, 0)
    }, [recipe.id])


    function fetchLogs() {
        fetch(`http://localhost:8000/cooking-logs?recipe_id=${recipe.id}`)
        .then(res => res.json())
        .then(data => setLogs(data))
    }

    function submitToApi(formData){
        fetch("http://localhost:8000/cooking-logs", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {fetchLogs()

        })
    }

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        })
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        alert(`Log Submitted. Date: ${formData.date_cooked}`)
        console.log(formData)
        submitToApi(formData)
    }

    return (
        <div className = "detail p-6 items-center gap-4 mb-2 space-y-2 max-w-3xl mx-auto">
            <button className="items-start border hover:bg-gray-200 rounded px-3 py-.5 cursor-pointer font-medium"
            onClick={onBack}>Back</button>
            <h2 className='text-2xl font-bold text-heading'>{recipe.name}</h2>
            <div className= 'mb-2 space-y-2'>
                <h3 className='text-xl font-medium'>Ingredients</h3>
                <ul className='max-w-md space-y-2 text-body list-disc list-inside'>
                    {recipe.ingredients.map(ing => (
                        <li key={ing.id}>{ing.quantity} {ing.name} </li>))
                    }
                </ul>
            </div>
            <div className='space-y-2'>
                <h3 className='text-xl font-medium'>Instructions</h3>
                <p>{recipe.instructions}</p>
                </div>
                <div>
                {logs.map((log) => (
                    <div className='log' key={log.id}>
                        <h2>Cooking Log</h2>
                        <p>Date Cooked: {log.date_cooked}</p>
                        <p>Rating: {log.rating}</p>
                        <p>Notes: {log.notes}</p>
                    </div>
                    )
                )}
            </div>
            <div className='max-w-md'>
                <h3 className="text-xl font-medium mb-2">Review the recipe</h3>
                <form onSubmit={handleSubmit}>
                    <div>
                        <label className="block text-sm font-medium mb-1">Date Cooked:</label>
                            <input className="w-full px-3 py-2 border rounded text-sm" 
                                type='datetime-local'
                                name="date_cooked"
                                value={formData.date_cooked}
                                onChange={handleChange}
                            />
                    </div>
                    <div>
                    <label className='block text-sm font-medium mb-1'>Rating out of 5:</label>
                        <input className='w-full px-3 py-2 border rounded text-sm'
                            type="number"
                            name='rating'
                            min='0'
                            max='5'
                            step="0.1"
                            placeholder='5.0'
                            value={formData.rating}
                            onChange={handleChange}
                        />
                    </div>
                    <div>
                    <label className='block text-sm font-medium mb-1'>Cooking Notes:</label>
                        <textarea
                            className='w-full px-3 py-2 border rounded text-sm'
                            name="notes"
                            value={formData.notes}
                            onChange={handleChange}
                            rows={4}
                            cols={50}
                        />
                    </div>
                <button
                    className='mr-2 bg-apricot-cream/50 hover:bg-apricot-cream cursor-pointer text-black text-sm font-medium  py-1.5 px-3 rounded'
                    type="submit"
                    name="button"
                    value="submit">Submit
                </button>
                </form>
            </div>
            <div>
                <RecipeRecommendation 
                recipe_id={recipe.id}
                onClick={onClick}
                />
            </div>
        </div>
    )
}