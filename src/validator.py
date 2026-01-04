# Validator layer

# Import List and Dict for type hints
from typing import List, Dict

# Import ValidationError to catch schema issues
from pydantic import ValidationError

from src.recipe import Recipe
from src.rules import run_all_rules

# Validation results structure
# Validates raw recipe input using pydantic schema validation and baking rule checks
def validate_recipe_input(
    recipe_data: Dict,
    user_prompt: str  # ✅ ADDED
) -> Dict[str, List[str]]:

    # Initialize empty error containers
    schema_errors: List[str] = []
    rule_errors: List[str] = []

    # Schema validation (pydantic)
    try:
        # Ensure input is a dictionary
        if not isinstance(recipe_data, dict):
            raise TypeError("Recipe output is not a valid JSON object")

        # Attempt to create a Recipe object - automatically triggers pydantic validation
        recipe = Recipe(**recipe_data)

    except ValidationError as e:
        # If schema validation fails, collect error messages
        for error in e.errors():
            schema_errors.append(
                f"{error['loc'][0]}: {error['msg']}"
            )

        # If schema fails, do not run rules
        return {
            "schema_errors": schema_errors,
            "rule_errors": []
        }

    except Exception as e:
        # Catch any unexpected errors (malformed AI output, missing keys, etc.)
        schema_errors.append(
            f"Invalid recipe format: {str(e)}"
        )

        return {
            "schema_errors": schema_errors,
            "rule_errors": []
        }

    # 🔥 NEW: Semantic validation — recipe must match user intent
    prompt_keywords = set(user_prompt.lower().split())
    recipe_keywords = set(recipe.name.lower().split())

    if not prompt_keywords.intersection(recipe_keywords):
        rule_errors.append(
            f"Recipe name '{recipe.name}' does not match the request."
        )

    # Rule-based validation
    # Run baking rules on validated ingredients
    try:
        rule_errors.extend(run_all_rules(recipe.ingredients))
    except Exception as e:
        rule_errors.append(
            f"Rule validation error: {str(e)}"
        )

    # Final result:
    return {
        "schema_errors": schema_errors,
        "rule_errors": rule_errors
    }
