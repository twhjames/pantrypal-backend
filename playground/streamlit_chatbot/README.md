# PantryPals Recipe Helper (Streamlit Playground)

This is an internal **Streamlit UI prototype** for the PantryPal system that allows users to experiment with recipe generation and food-related chat using ingredients they have on hand.

Built for LLM experimentation and UX prototyping using models hosted via **Groq API**, powered by **Streamlit**, and configured with environment variables through `.env`.

---

## Features

-   Chat interface powered by local or Groq-hosted LLaMA/Mixtral models
-   Ingredient-to-recipe prompting (via sidebar)
-   Conversational memory using session state
-   `.env`-based secure API key handling
-   Developer-friendly and easily modifiable for prompt engineering

---

## Tech Stack

| Component    | Tool/Library                                           |
| ------------ | ------------------------------------------------------ |
| UI Framework | [Streamlit](https://streamlit.io)                      |
| LLM Backend  | [Groq Python SDK](https://github.com/groq/groq-python) |
| Environment  | `python-dotenv` for loading secrets                    |
| Language     | Python 3.12+                                           |

---

## Environment Setup

1. Create a `.env` file in your project root:

```bash
GROQ_API_KEY=your_actual_api_key_here
```

2. Install dependencies (within your virtual environment):

```bash
pip install streamlit groq python-dotenv
```

---

## Running the App

1. Activate your virtual environment if needed:

```bash
source venv/bin/activate
```

2. Then launch the Streamlit interface:

```bash
streamlit run playground/pantrypal_streamlit_chatbot.py
```

3. Access the app at http://localhost:8501

---

## Example Prompts

-   What's a quick vegetarian dinner?
-   Make a lunch with rice and chicken.
-   I want a 15-minute pasta recipe.
