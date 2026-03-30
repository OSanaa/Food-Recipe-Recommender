
# class Component(Base):
#     """Represents a component for each recipe.

#     A component can be located in a store.

#     Attributes:
#         id: Primary key.
#         component_name: Name of the component.
#     """
#     __tablename__ = "component"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     component_name: Mapped[str] = mapped_column(String(50), nullable=False)

# class Unit(Base):
#     __tablename__ = "unit"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     unit: Mapped[str] = mapped_column(String(50), nullable=False)

# class ShoppingList(Base):
#     """Represents a shopping list.

#     Shopping lists can have multiple components and will have a total cost for 
#     all the items.

#     Attributes:
#         id: Primary key.
#         component_id: Foreign key referencing the component.
#         total_price: Total cost of the shopping list.
#     """
#     __tablename__ = "shopping_list"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     component_id: Mapped[int] = mapped_column(ForeignKey("component.id"))
#     user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
#     total_price: Mapped[float] = mapped_column(Numeric(5,2), nullable=True)
    
# class Store(Base):
#     """Represents a store.

#     Stores can have multiple 

#     Attributes:
#         id: Primary key.
#         component_id: Foreign key referencing component for the recipe.    
#     """
#     __tablename__ = "store"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     component_id: Mapped["Component"] = mapped_column(ForeignKey("component.id"))
#     component_price: Mapped[float] = mapped_column(Numeric(5,2), nullable=False)

# class User(Base):
#     """Represents a user

#     Users can have multiple recipes as well as multiple shopping lists.

#     Attributes:
#         id: Primary key.
#         recipe_id: Foreign key referencing the Recipe the user wrote.
#         shopping_list_id: Foreign key referncing the users shopping lists.
    
#     """
#     __tablename__ = "user"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)