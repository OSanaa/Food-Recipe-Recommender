import { useState } from 'react'
import FormInput from './FormInput';

export default function RecipeForm({onBack, onSubmitSuccess}){

    const [formData, setFormData] = useState({
        name : '',
        author : '',
        area : '',
        category : '',
        instructions : '',
        source : 'user',
        ingredients : []
    });
    const [toggleAdd, setToggleAdd] = useState(false)

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
            ingredients: [...formData.ingredients, {name: "", quantity: "", unit: ""}]
        })
    }

    const handleIngredientDelete = (deleteIndex) => {
        setFormData(prevData => ({
            ...prevData, 
            ingredients: prevData.ingredients.filter((_,i) => i !== deleteIndex)}))
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
        setFormData({ ...formData, ingredients: updatedIngredients})    
    }

    return (
        <div className="detail p-6 items-center gap-4 mb-2 space-y-2 max-w-3xl mx-auto">
            <button className='btn-outline' 
            onClick={onBack}>Back</button>
            <div className='max-w-md'>
                <h3 className="text-xl font-medium mb-2">Create Recipe</h3>                
                <form onSubmit={handleSubmit} className='space-y-4'>
                    <FormInput label="Recipe Name:" name="name" value={formData.name} onChange={handleChange}/>
                    <FormInput label="Author:" name="author" value={formData.author} onChange={handleChange}/>
                    <FormInput label="Area:" name="area" value={formData.area} onChange={handleChange}/>
                    <FormInput label="Category:" name="category" value={formData.category} onChange={handleChange}/>
                    <FormInput label="Instructions:" type='textarea' name="instructions" value={formData.instructions} onChange={handleChange}/>
                    <FormInput label="Source:" placeholder="user" name="source" value={formData.source} onChange={handleChange}/>
                    <button className='btn-outline' type='button' onClick={addIngredient}>Add Ingredient</button>
                    {formData.ingredients.map((ing, index) => (
                        <div key={index} className="flex items-end gap-3">
                            <div className="flex-[2]">
                                <FormInput label="Ingredient Name:" name="name" value={ing.name} onChange={(e) => handleIngredientChange(index, e)}/>
                            </div>
                            <div className="w-20">
                                <FormInput label="Quantity:" name="quantity" value={ing.quantity} onChange={(e) => handleIngredientChange(index, e)}/>
                            </div>
                            <div className="w-20">
                                <FormInput label="Unit:" name="unit" value={ing.unit} onChange={(e) => handleIngredientChange(index, e)}/>
                            </div>
                            <button className='btn-outline' type='button' onClick={() => handleIngredientDelete(index)}>X</button>
                        </div>
                        )
                    )}
                    <button className='btn-primary' type="submit" name="button" value="submit">Submit</button>
                </form>
            </div>
        </div>
    )
}