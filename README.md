BatterBot - AI-Powered Baking Assistant

ABOUT: BatterBot is an AI-powered baking assistant that generates and modifies structured baking recipes through a chat-based web interface. The application combines a Streamlit frontend with a Python backend that interfaces with the OpenAI API, enforcing strict validation rules and schema constraints to ensure reliable recipe outputs. 

FEATURES:
    - Generate baking recipes from natural language prompts.
    - Supports modification requests like "make it vegan" or "remove chocolate chips".
    - Eforces a strict JSON output format for all recipes.
    - Validates the recipe structure and baking rules before displaying the results.
    - Implemented a chat-based interface with session memory for iterative interactions.
    - Ingredient formatting logic to improve readability.
    - 'Copy to Clipboard' functionality to easily copy the ingredient list.

TECH STACK:
Frontend:
    - Streamlit
    - HTML / CSS (custom styling)
    - JavaScript (clipboard interaction)
Backend:
    - Python
    - OpenAI API
    - Pydantic (schema validation)
    - Custom rule-based validation engine
Concepts & Architecture:
    - Client-server separation
    - Prompt engineering
    - Input validation and error handling
    - Session state management
    - Modular backend design

HOW IT WORKS:
    1. The user submits a prompt through the Streamlit chat interface (e.g., cinnamon rolls).
    2. The backend sends the prompt to the OpenAI API using a constrained system prompt.
    3. The AI returns a recipe in strict JSON format.
    4. The recipe is validated using a Pydantic schema and custom baking rules.
    5. If validation fails, feedback is sent to the model for correction.
    6. Validated recipes are formatted and displayed to the user.

RUNNING LOCALLY (HOW TO):
    1. Install dependencies: pip install -r requirements.txt
    2. Set your OpenAI API key: export OPENAI_API_KEY=your_api_key_here
    3. Run the app: streamlit run app.py

LIMITATIONS:
    - Does not calculate nutritional information.
    - Recipes are limited strictly to baked goods.
    - Requires an OpenAI API key and is subject to API rate limits.

FUTURE IMPROVEMENTS:
    - Add nutritional estimations.
    - Improve handling of non-recipe user queries (besides asking for its name and handling recipe queries that are NOT baked goods).
    - Deploy to a cloud platform for public access.

AUTHOR:
Ishika Ayyagari
University of Central Florida
