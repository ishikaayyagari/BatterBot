from pydantic import BaseModel, Field, validator
from typing import Dict

# INGREDIENT SCHEMA
class Ingredient(BaseModel):
    # Numeric amount (must be positive)
    amount: float = Field(
        ...,
        gt=0,
        description="Amount of the ingredient"
    )

    # Unit for the ingredient (grams, cups, etc.)
    unit: str = Field(
        ...,
        description="Unit of measurement"
    )


# RECIPE SCHEMA
class Recipe(BaseModel):
    # Recipe name
    name: str = Field(
        ...,
        description="Name of the recipe"
    )

    # Ingredients dictionary - key: ingredient name (string), value: ingredient object (amount and unit)
    ingredients: Dict[str, Ingredient] = Field(
        ...,
        description="Ingredients with amounts and units"
    )

    # Servings - must be a positive integer
    servings: int = Field(
        default=1,
        gt=0,
        description="Number of servings"
    )

    # Optional notes field
    notes: str = Field(
        default="",
        description="Additional recipe notes"
    )

    # VALIDATORS
    ("ingredients")
    # Ensures all ingredient amounts are positive
    def check_ingredient_amounts(cls, ingredients):
        for ingredient_name, ingredient in ingredients.items():
            if ingredient.amount <= 0:
                raise ValueError(
                    f"Ingredient '{ingredient_name}' must have a positive amount"
                )
        return ingredients

    # RECIPE METHODS    
    # Returns a new recipe instance with scaled ingredient amounts and servings
    def scale_recipe(self, factor: float):
        # Create a new dictionary with scaled ingredient amounts
        scaled_ingredients = {
            name: Ingredient(
                amount=ingredient.amount * factor,
                unit=ingredient.unit
            )
            for name, ingredient in self.ingredients.items()
        }

        # Return a new Recipe object
        return Recipe(
            name=self.name,
            ingredients=scaled_ingredients,
            servings=int(self.servings * factor),
            notes=self.notes
        )
