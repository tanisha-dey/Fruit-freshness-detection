import os
import streamlit as st
import google.generativeai as genai
import random
from datetime import datetime, timedelta

# Configure page
st.set_page_config(
    page_title="RECIPE GENIE",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

        body {
            background-color:rgb(247, 248, 250); /* Dark blue background */
            color:rgb(2, 22, 43);
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
        }

        .stApp {
            background-color: transparent;
        }

        .title {
            font-size: 3.5em;
            font-weight: 700;
            color:rgb(2, 14, 27);
            text-align: center;
            margin-top: 2rem;
            text-shadow: 0 2px 4px rgba(88, 166, 255, 0.8);
        }

        .content {
            display: flex;
            justify-content: space-between;
            gap: 2rem;
            margin-top: 2rem;
        }

        .ingredients-box {
            flex: 1;
            background-color: #0d253f; /* Slightly lighter blue */
            border-radius: 10px;
            padding: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            max-width: 400px;
        }

        .ingredients-title {
            font-size: 2.0em;
            font-weight: 700;
            color: #58a6ff;
            text-align: center;
            margin-bottom: 1rem;
        }

        .ingredient-container {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: center;
        }

        .ingredient-box {
            background-color: #112b45;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 1rem;
            color: #c9d1d9;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            width: 150px; /* Increased width */
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .ingredient-box:hover {
            transform: scale(2.05);
            box-shadow: 0 4px 8px rgba(88, 166, 255, 0.7);
            background-color: #1b3858;
        }

        .ingredient-name {
            font-weight: 700;
            color: #ffffff;
        }

        .ingredient-expiry {
            color: #f85149;
            font-weight: 700;
        }

        .recipes-title {
            font-size: 3.0em;
            font-weight: 700;
            color: #58a6ff;
            text-align: center;
            margin-bottom: 1rem;
        }

        .recipe-container {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .recipe-box {
            background-color:rgb(246, 251, 255);
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 1rem;
            color: #39d0ff; /* Bright teal color for recipes */
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .recipe-box:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(88, 166, 255, 0.7);
            background-color:rgb(4, 17, 31);
        }

        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header with title
st.markdown("""
    <div class="title">Recipe Genie</div>
""", unsafe_allow_html=True)

# Simulated data for ingredients and expiration days
def fetch_ingredients_from_backend():
    # Mock data: a list of ingredients with random expiration dates
    ingredients = [
        {"name": "Tomato", "days_to_expiry": random.randint(1, 9)},
        {"name": "Banana", "days_to_expiry": random.randint(1, 6)},
        {"name": "Capsicum", "days_to_expiry": random.randint(1, 10)},
        {"name": "Orange", "days_to_expiry": random.randint(1, 5)},
        {"name": "Potato", "days_to_expiry": random.randint(1, 7)},
        {"name": "Apple", "days_to_expiry": random.randint(1, 4)},
        {"name": "Cucumber", "days_to_expiry": random.randint(1, 5)},
    ]
    return ingredients

# Filter ingredients close to expiration (within 5 days)
def filter_expiring_ingredients(ingredients, days_threshold=4):
    expiring_ingredients = []
    for item in ingredients:
        if 0 < item["days_to_expiry"] <= days_threshold:
            expiring_ingredients.append(item)
    return expiring_ingredients

# Existing Gemini AI configuration
GEMINI_API_KEY = "AIzaSyCTazG70YGC5kFrbdn2fSY72s4iArt5Y5A"  # Replace with your Gemini API key
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are a master chef with extensive knowledge of culinary arts. Provide creative recipes based on the given ingredients. Be friendly and descriptive.",
)

# Modified get_recipes function
def get_recipes(ingredients):
    ingredients_str = ", ".join([item["name"] for item in ingredients])
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [f"I have {ingredients_str}. Can you suggest some creative recipes?"],
            },
            {
                "role": "user",
                "parts": ["Please give detailed recipes with names, descriptions, and preparation steps."],
            }
        ]
    )
    response = chat_session.send_message(f"I have {ingredients_str}. Suggest me three recipes with details.")

    # Display results in styled container
    sanitized_response = response.text.replace("*", "<strong>").replace("\n", "<br>")
    st.markdown(f"""
        <div class="recipes-title">Your Recipe Suggestions</div>
        <div class="recipe-container">
            {sanitized_response}
        </div>
    """, unsafe_allow_html=True)

# Fetch ingredients and filter based on expiration date
ingredients = fetch_ingredients_from_backend()
expiring_ingredients = filter_expiring_ingredients(ingredients)

st.markdown("<div class='content'>", unsafe_allow_html=True)
if expiring_ingredients:
    # Display the list of expiring ingredients
    st.markdown("""
        <div class="ingredients-box">
            <div class="ingredients-title">Expiring Ingredients</div>
            <div class="ingredient-container">
    """, unsafe_allow_html=True)
    for item in expiring_ingredients:
        st.markdown(f"""
            <div class="ingredient-box">
                <span class="ingredient-name">{item['name']}</span><br>
                <span class="ingredient-expiry">{item['days_to_expiry']} days left</span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Generate recipe suggestions next to ingredients
    with st.container():
        st.markdown("<div class='recipes-box'>", unsafe_allow_html=True)
        get_recipes(expiring_ingredients)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("No ingredients are about to expire within the next 5 days.")
st.markdown("</div>", unsafe_allow_html=True)
