# RULES ENGINE
# Domain-specific baking logic

from typing import Dict, List

# Ingredient categories:    
CATEGORY_KEYWORDS = {
    "flour": ["flour"],
    "fat": ["butter", "oil", "shortening"],
    "sugar": ["sugar", "honey", "syrup"],
    "liquid": ["milk", "water", "cream"],
    "binder": ["egg"],
    "fruit_binder": ["banana", "applesauce", "pumpkin"]
}

# Categorization:
# Assigns ingredients to baking categories using keyword-based matching
def categorize_ingredients(
    ingredients: Dict[str, object]
) -> Dict[str, List[str]]:

    # Initialize an empty list for each category
    categories_found = {
        category: []
        for category in CATEGORY_KEYWORDS
    }

    # Loop through each ingredient name
    for ingredient in ingredients:
        # Normalize ingredient name to lowercase
        ingredient_lower = ingredient.lower()

        # Check each category and keywords
        for category, keywords in CATEGORY_KEYWORDS.items():

            # Returns true if ANY keyword
            if any(keyword in ingredient_lower for keyword in keywords):
                categories_found[category].append(ingredient)

    return categories_found


# Rule 1: Required categories (flexible)
# Ensures the recipe has sufficient structural components to bake properly
def check_required_categories(
    ingredients: Dict[str, object]
) -> List[str]:
    
    errors = []

    # Only these categories are truly required for baked goods
    REQUIRED_CATEGORIES = ["flour", "sugar"]

    # Categorize the ingredients
    categories = categorize_ingredients(ingredients)

    # Loop through required categories only
    for category in REQUIRED_CATEGORIES:
        if not categories.get(category):
            errors.append(
                f"Missing required ingredient category: {category}"
            )

    return errors


# Sugar:Flour ratio
# Ensures that sugar amount does not exceed flour amount by weight. This affects the structure of the final product.
def check_sugar_flour_ratio(
    ingredients: Dict[str, object]
) -> List[str]:

    errors = []

    # Default to 0 if ingredient not present
    flour_amount = 0
    sugar_amount = 0

    # Loop through ingredients to add up totals
    for ingredient, ingredient_data in ingredients.items():
        ingredient_lower = ingredient.lower()

        amount = ingredient_data.amount

        if "flour" in ingredient_lower:
            flour_amount += amount

        if "sugar" in ingredient_lower:
            sugar_amount += amount

    # Apply the rule
    if sugar_amount > flour_amount:
        errors.append(
            "Sugar amount exceeds flour amount. May cause structural issues."
        )

    return errors


# Main rules
# Runs all baking rules and will return a combines list of errors/warnings
def run_all_rules(
    ingredients: Dict[str, object]
) -> List[str]:

    errors = []

    # Run each rule and collect results
    errors.extend(check_required_categories(ingredients))
    errors.extend(check_sugar_flour_ratio(ingredients))

    return errors
