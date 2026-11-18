
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from the .env file
load_dotenv()

# Create connection to OpenAI

load_dotenv()

# Check the local .env file first
api_key = os.getenv("OPENAI_API_KEY")

# If not found, check Streamlit Cloud secrets
if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    raise RuntimeError(
        "OpenAI API key not found. Check your .env file "
        "or Streamlit Cloud Secrets."
    )

client = OpenAI(api_key=api_key)




from datetime import date


def generate_recipes(inventory, servings=2, max_extra_ingredients=3):

    ingredient_list = []

    for item in inventory:
        name = item[1]
        quantity = item[3]
        unit = item[4]

        # Expiration date is column 6 in our database
        expiration = item[6]

        if expiration:
            try:
                expiration_date = date.fromisoformat(str(expiration))
                days_remaining = (expiration_date - date.today()).days

                if days_remaining < 0:
                    expiration_info = (
                        f"EXPIRED {abs(days_remaining)} days ago"
                    )
                elif days_remaining == 0:
                    expiration_info = "EXPIRES TODAY"
                else:
                    expiration_info = (
                        f"Expires in {days_remaining} days"
                    )

            except ValueError:
                expiration_info = "Expiration date unknown"
        else:
            expiration_info = "No expiration date provided"

        ingredient_list.append(
            f"- {name}: {quantity} {unit} ({expiration_info})"
        )

    ingredients = "\n".join(ingredient_list)

    prompt = f"""
    You are PantryPal, a helpful and creative meal planning assistant.

    The user's current inventory:

    {ingredients}

    Generate exactly THREE different recipe suggestions.

    Recipe 1: USE IT BEFORE IT'S GONE
    - Prioritize ingredients closest to expiration.
    - Give special priority to ingredients expiring today or soon.
    - Never recommend using expired ingredients.

    Recipe 2: MAKE THE MOST OF WHAT YOU HAVE
    - Use as many of the user's existing ingredients as practical.
    - Minimize the need for additional ingredients.

    Recipe 3: SURPRISE ME
    - Suggest something creative, interesting, and appealing.
    - Use ingredients from the inventory, but be imaginative.

    Requirements for ALL three recipes:
    - Make each recipe serve {servings} people.
    - Use no more than {max_extra_ingredients} additional ingredients.
    - Clearly separate available ingredients from missing ingredients.
    - Never pretend the user owns an ingredient that isn't listed.
    - Include preparation time and cooking time.
    - Include numbered cooking instructions.
    - Identify which existing ingredients should be used soon.

    Format each recipe with:
    - Recipe name
    - Recipe style
    - Short description
    - Available ingredients
    - Additional ingredients needed
    - Preparation time
    - Cooking time
    - Cooking instructions
    """

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )

    return response.output_text
