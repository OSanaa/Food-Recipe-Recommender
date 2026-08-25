# Pending Fixes and Updates

- Look into what the backend yields for the ingredient search function. There were duplicate ingredients that 
were showing up on the IngredientSearch component. Example: "Rice" vs "rice" were both popping up.
- Add a back button for the IngredientSearch component.
- Add a way to see what ingredients that were toggled in the IngredientSearch component
- None leaks into embedding text. Fix the build_recipe_text function to skip over None.