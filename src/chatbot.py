# BatterBot chatbot - the AI brain
# Talks to the OpenAI API, asks the AI to generate recipes, parses the AI output, 
# validates the generated recipes, asks the AI to fix mistakes.

import json
import os
from openai import OpenAI

# My imports
from src.validator import validate_recipe_input
from src.formatter import format_ingredient


# OpenAI client setup
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError(
        "OPENAI_API_KEY not found. Please set it in your terminal."
    )

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# System prompt! 
SYSTEM_PROMPT = """
You are BatterBot with name "Ishika", an expert baking assistant.

You can do TWO things:
1. Generate a NEW baking recipe from scratch
2. MODIFY an EXISTING recipe if one is provided

IMPORTANT BEHAVIOR RULES:
- If the user provides an existing recipe and asks for a change, you MUST modify that recipe
- If NO recipe is provided, generate a brand new one
- Do NOT ignore user intent
- Preserve structure and ingredients unless changes are requested

You must output baking recipes in STRICT JSON format.
Do not include explanations or extra text.

RULES:
- Output ONLY valid JSON
- Ingredients must be a dictionary
- Each ingredient must include an amount AND a unit
- Ingredient amounts must be positive numbers
- Servings must be a positive integer

EDITING RULES:
- Replace incompatible ingredients when required (e.g., vegan)
- Maintain proper baking balance (fat, sugar, liquid, structure)
- Do NOT leave required categories empty

JSON FORMAT:
{
  "name": "Recipe Name",
  "ingredients": {
    "ingredient name": {
      "amount": number,
      "unit": "measurement unit"
    }
  },
  "servings": number,
  "notes": "optional"
}
"""


# Recipe generation
def generate_recipe_from_prompt(user_prompt: str) -> dict:

    print("user prompt: ", user_prompt)
    print("system prompt", SYSTEM_PROMPT)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    print("GPT RESPI: ", response)

    raw = response.choices[0].message.content.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError(f"AI returned invalid JSON:\n{raw}")


# Main chat loop - incorporates self-correcting logic
def batterbot_chat(user_prompt: str, max_attempts: int = 3) -> dict:
    attempt = 1
    feedback = ""

    while attempt <= max_attempts:
        print(f"\nAttempt {attempt}...")

        full_prompt = user_prompt
        if feedback:
            full_prompt += f"\n\nFix the following issues:\n{feedback}"

        try:
            recipe_data = generate_recipe_from_prompt(full_prompt)
        except ValueError as e:
            feedback = str(e)
            attempt += 1
            continue

        validation_result = validate_recipe_input(recipe_data, user_prompt)

        if (
            not validation_result["schema_errors"]
            and not validation_result["rule_errors"]
        ):
            print("Recipe validated successfully.")

            # Format ingredient amounts
            for ingredient, data in recipe_data["ingredients"].items():
                recipe_data["ingredients"][ingredient]["amount"] = format_ingredient(
                    data["amount"],
                    data["unit"]
                )

            return recipe_data

        feedback_messages = (
            validation_result["schema_errors"]
            + validation_result["rule_errors"]
        )

        print("Validation failed:")
        for msg in feedback_messages:
            print(f"- {msg}")

        feedback = "\n".join(feedback_messages)
        attempt += 1

    raise RuntimeError(
        "BatterBot could not generate a valid recipe after multiple attempts."
    )
