import { useState } from 'react'

export default function RecipeForm({onBack, onSubmitSuccess}){

    const [formData, setFormData] = useState({
        name : '',
        author : '',
        area : '',
        category : '',
        instructions : '',
        source : 'user',
        // ingredients : []
    });

    function submitToApi(formData){
        fetch("http://localhost:8000/recipes", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            onSubmitSuccess()
            onBack()
        })
    }
    
    const addIngredient = () => {
        setFormData({
            ...formData,
            ingrediets: [...formData.ingredients, {name: "", quantity: "", unit: ""}]
        })
    }
    
    const handleSubmit = (e) => {
        e.preventDefault();
        alert(`Submitted Name: ${formData.name}`)
        console.log(formData)
        submitToApi(formData)
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    }

    const handleIngredientChange = (index, e) => {
        const updatedIngredients = formData.ingredients.map((ing, i) =>
        i === index ? { ...ing, [e.target.name]: e.target.value} : ing
        )
        setFormData({... formData, ingredients: updatedIngredients})    
    }

    return (
        
        <div className="form">
            <button onClick={onBack}>Back</button>
            <form onSubmit={handleSubmit}>
                <label>Recipe Name: 
                    <input type="text"
                    name='name'
                    value={formData.name}
                    onChange={handleChange}
                    />
                </label>
                <br/>
                <label>Author:
                    <input type="text"
                    name='author'
                    value={formData.author}
                    onChange={handleChange}
                    />
                </label>
                <br/>
                <label>Area:
                    <input type="text"
                    name='area'
                    value={formData.area}
                    onChange={handleChange}
                    />
                </label>
                <br/>
                <label>Category:
                    <input type="text"
                    name='category'
                    value={formData.category}
                    onChange={handleChange}
                    />
                </label>
                <br/>
                <label>Instructions:
                    <input type="text"
                    name='instructions'
                    value={formData.instructions}
                    onChange={handleChange}
                    />
                </label>
                <br/>
                <label>Source:
                    <input type="text"
                    name='source'
                    placeholder='user'
                    value={formData.source}
                    onChange={handleChange}
                    />
                </label>
                <br/>
                <label>Ingredients:
                    <input type="text"
                    name='ingredients'
                    value={formData.ingredient}
                    onChange={handleChange}
                    />
                </label>
                <br/>
                <button type="submit" name="button" value="submit">Submit</button>
            </form>
        </div>
    )
}