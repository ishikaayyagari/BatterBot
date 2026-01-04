# BatterBot ENTRY POINT:
# Takes user request, sends to BatterBot, prints final validated recipe.

# Import the main chat function from chatbot.py
from chatbot import batterbot_chat

# Formats recipe output for terminal-friendly display
def format_recipe(recipe: dict) -> str:
    lines = []

    # Recipe title
    lines.append(f"\n🍞 {recipe.get('name', 'Unnamed Recipe')}")
    lines.append(f"Servings: {recipe.get('servings', 'N/A')}\n")

    # Ingredients list
    lines.append("Ingredients:")
    for ingredient, details in recipe.get("ingredients", {}).items():
        amount = details.get("amount")
        unit = details.get("unit", "")
        lines.append(f"- {ingredient}: {amount} {unit}")

    # Optional notes
    notes = recipe.get("notes", "")
    if notes:
        lines.append("\nNotes:")
        lines.append(notes)

    return "\n".join(lines)

# Main function that runs BatterBot
def main():
    # Stores the current recipe state across turns
    current_recipe = None

    print("🧁 Welcome to BatterBotteeeeeee!")
    print("Enter a baking request (e.g., 'banana bread recipe').")
    print("Type 'exit' to quit.\n")

    # Conversation loop
    while True:
        # Get user input
        user_request = input("You: ").strip()

        # If user types exit:
        if user_request.lower() == "exit":
            print("👋 Goodbye!")
            break

        # If no recipe exists yet, generate one:
        if current_recipe is None:
            current_recipe = batterbot_chat(user_request)

        else:
            # If a recipe exists, ask the AI to modify it:
            modification_prompt = (
                "Here is the current recipe:\n"
                f"{current_recipe}\n\n"
                "Modify this recipe based on the following request:\n"
                f"{user_request}"
            )

            current_recipe = batterbot_chat(modification_prompt)

        # Print the updated recipe:
        print("\n🍰 Current Recipe:")
        print(format_recipe(current_recipe))


# Ensures main() only runs
if __name__ == "__main__":
    main()