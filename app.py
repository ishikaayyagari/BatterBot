# FRONTEND using streamlit AKA all the fun stuff happens here
import streamlit as st
from src.chatbot import batterbot_chat
import streamlit.components.v1 as components

# Page config!
st.set_page_config(
    page_title="BatterBot 🧁",
    page_icon="🧁",
    layout="centered"
)

# Styling! Making it pink and pretty and cutesy
st.markdown(
    """
    <style>
    /* Background */
    .stApp {
        background-color: #ffeaf2;
    }

    html, body, div, span, p, li, ul, ol, strong, em, h1, h2, h3, h4 {
        color: #000000 !important;
    }

    /* Center main header */
    h1 {
        text-align: center;
    }

    /* Headers */
    h1, h2, h3, h4 {
        font-family: 'Trebuchet MS', sans-serif;
        font-weight: 800;
    }

    /* Subtitle */
    .subtitle {
        color: #000000 !important;
        font-size: 1.05rem;
        margin-top: -8px;
        margin-bottom: 24px;
        font-weight: 500;
        text-align: center;
    }

    /* Chat bubbles */
    [data-testid="chat-message-user"] * {
        background-color: #ffd6e8;
        color: #000000 !important;
        border-radius: 18px;
    }

    [data-testid="chat-message-assistant"] * {
        background-color: #ffffff;
        color: #000000 !important;
        border-radius: 18px;
    }

    /* Markdown content */
    [data-testid="stMarkdownContainer"] * {
        color: #000000 !important;
        opacity: 1 !important;
    }

    /* Lists */
    [data-testid="stMarkdownContainer"] ul li,
    [data-testid="stMarkdownContainer"] ol li {
        color: #000000 !important;
    }

    /* Strong / Servings / Tips */
    [data-testid="stMarkdownContainer"] strong {
        color: #000000 !important;
        font-weight: 700;
    }

    /* Chat input */
    textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    textarea::placeholder {
        color: #7a7a7a !important;
    }

    /* Spinner text */
    [data-testid="stSpinner"] * {
        color: #000000 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.title("🧁 BatterBot")
st.markdown(
    "<p class='subtitle'>Welcome to your personal AI baking assistant! What would you like a recipe for today?</p>",
    unsafe_allow_html=True
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_recipe" not in st.session_state:
    st.session_state.current_recipe = None

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("What should we bake today?")

MODIFICATION_KEYWORDS = [
    "make it", "replace", "without", "remove", "add",
    "substitute", "vegan", "gluten", "less", "more"
]

def is_modification_request(text: str) -> bool:
    return any(k in text.lower() for k in MODIFICATION_KEYWORDS)

# Detect questions about the assistant's identity
def is_name_question(text: str) -> bool:
    text = text.lower()
    return any(
        phrase in text
        for phrase in [
            "what is your name",
            "what's your name",
            "who are you",
            "your name",
            "who am i talking to",
            "name",
            "what are you",
            "do you know who you are",
        ]
    )

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Handle identity questions without calling the recipe backend
    if is_name_question(user_input):
        response = "My name is **Flan**. I’m your AI baking assistant."

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

    else:
        with st.chat_message("assistant"):
            loader = st.empty()
            loader.markdown(
                "<h4 style='color:black;'>🎂 Mixing the batter...</h4>",
                unsafe_allow_html=True
            )

            # Catch backend failures and return a friendly constraint message
            try:
                if (
                    st.session_state.current_recipe is None
                    or not is_modification_request(user_input)
                ):
                    recipe = batterbot_chat(user_input)
                else:
                    modification_prompt = (
                        "Here is the current recipe:\n"
                        f"{st.session_state.current_recipe}\n\n"
                        "Modify this recipe based on the following request:\n"
                        f"{user_input}"
                    )
                    recipe = batterbot_chat(modification_prompt)

                st.session_state.current_recipe = recipe
                loader.empty()

            except RuntimeError:
                loader.empty()
                response = (
                    "I specialize in baked goods like cakes, cookies, breads, and pastries. "
                    "I can’t generate recipes for non-baked desserts or items outside that scope."
                )

                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
                st.stop()

            response = f"""
### 🍞 {recipe['name']}
**Servings:** {recipe['servings']}

**Ingredients:**
"""
            for ingredient, data in recipe["ingredients"].items():
                response += f"- {ingredient}: {data['amount']}\n"

            if recipe.get("notes"):
                response += f"\n💡 **Tips:** {recipe['notes']}"

            st.markdown(response)

            # Copy ingredients
            ingredients_text = ""
            for ingredient, data in recipe["ingredients"].items():
                ingredients_text += f"- {ingredient}: {data['amount']}\\n"

            components.html(
                f"""
                <button onclick="navigator.clipboard.writeText(`{ingredients_text}`)"
                    style="
                        background-color:black;
                        color:white;
                        border:none;
                        border-radius:14px;
                        padding:8px 16px;
                        font-weight:700;
                        cursor:pointer;
                        margin-top:8px;
                    ">
                    📋 Copy Ingredients
                </button>
                """,
                height=60
            )

            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )
