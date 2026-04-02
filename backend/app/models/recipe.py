from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.database import Base

class Recipe(Base):
    """Represents food recipes.

    Attributes:
        id: Primary Key
        name: Name of the recipe.
        instructions: The step by step of how to create the recipe.
        link: If the recipe was from an external site.
        author: The creator of the recipe.
        area: The area in which the food is from.
        category: The food category.
        source: Distinction of if the recipe was from external source or from a user.
    
    """
    __tablename__ = "recipe"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    instructions: Mapped[str] = mapped_column(Text, nullable=False)
    link: Mapped[str] = mapped_column(String(1000), nullable=True)
    author: Mapped[str] = mapped_column(String(50),nullable=False)
    area: Mapped[str] = mapped_column(String(50), nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=True)
    source: Mapped[str] = mapped_column(String(10), nullable=False)
    ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="recipe")
    
class Ingredient(Base):
    """Represents the ingredients that make up the recipe.

    Attributes:
        id: Primary key.
        name: Name of the ingredient.
        quantity: Quantity for each ingredient.
        unit: The unit used to measure each ingredient.
        recipe_id: Foreign key referencing recipe.
        
    """
    __tablename__ = "ingredient"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[str] = mapped_column(String(50), nullable=True)
    unit: Mapped[str] = mapped_column(String(50), nullable=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"))
    recipe: Mapped['Recipe'] = relationship(back_populates="ingredients")

class CookingLog(Base):
    """Represents the cooking log for users who cooked the recipe.

    Attributes:
        id: Primary key.
        date_cooked: The date the recipe was cooked.
        notes: Notes that the user may have.
        rating: A rating the user gives the recipe.
        recipe_id: Foreign key referencing recipe.
    """
    __tablename__ = "cooking_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date_cooked: Mapped[datetime] = mapped_column(DateTime,nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    rating: Mapped[float] = mapped_column(Numeric(2,1), nullable=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipe.id"))