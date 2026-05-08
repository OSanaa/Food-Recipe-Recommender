import { useState } from 'react'
import { useEffect } from 'react'

export default function RecipeDetail({recipe, onBack}){
    const [logs, setLogs] = useState([])
    const [formData, setFormData] = useState({
        date_cooked: new Date().toISOString().slice(0, 16),
        rating: 0.0,
        notes: '',
        recipe_id: recipe.id
    });

    // useEffect(() => {
    //     fetch(`http://localhost:8000/cooking-logs?recipe_id=${recipe.id}`)
    //     .then(res => res.json())
    //     .then(data => setLogs(data))
    // }, [recipe.id])
    useEffect(() => {
        fetchLogs()
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
        <div className = "detail">
            <button onClick={onBack}>Back</button>
            <h3>Ingredients and Instructions for {recipe.name}</h3>
            <ul>
                {recipe.ingredients.map(ing => (
                    <li key={ing.id}>{ing.quantity} {ing.name} </li>))
                }
            </ul>
            <p>{recipe.instructions}</p>
            <br/>
            {logs.map((log) => (
                <div className='log' key={log.id}>
                    <h2>Cooking Log</h2>
                    <p>Date Cooked: {log.date_cooked}</p>
                    <p>Rating: {log.rating}</p>
                    <p>Notes: {log.notes}</p>
                </div>
                )
            )}

            <div className='form'>
                <form onSubmit={handleSubmit}>
                    <label>Date Cooked: 
                        <input type='datetime-local'
                            name="date_cooked"
                            value={formData.date_cooked}
                            onChange={handleChange}
                        />
                    </label>
                    <br/>
                    <label>Rating out of 5:
                        <input type="number"
                            name='rating'
                            min='0'
                            max='5'
                            step="0.1"
                            value={formData.rating}
                            onChange={handleChange}
                        />
                    </label>
                    <br/>
                    <label>Cooking Notes: 
                        <textarea
                            name="notes"
                            value={formData.notes}
                            onChange={handleChange}
                            rows={4}
                            cols={50}
                        />
                    </label>
                    <br/>
                <button type="submit" name="button" value="submit">Submit</button>
                </form>
            </div>
        </div>
    )
}