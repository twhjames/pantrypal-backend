import streamlit as st
import os
from typing import Generator
from groq import Groq

#Page set up
st.set_page_config(page_icon="🧑‍🍳", layout="wide",
                   page_title="PantryPals Recipe Helper")

st.title("PantryPals Recipe Helper")
st.subheader("Let's Cook up some Recipes!", divider='rainbow', anchor = False)

#Groq initialisation
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"],
)

# Initialize chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = None

# Define model details
models = {
    "gemma2-9b-it": {"name": "Gemma2-9b-it", "tokens": 8192, "developer": "Google"},
    "llama-3.3-70b-versatile": {"name": "LLaMA3.3-70b-versatile", "tokens": 128000, "developer": "Meta"},
    "llama-3.1-8b-instant" : {"name": "LLaMA3.1-8b-instant", "tokens": 128000, "developer": "Meta"},
    "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
    "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}


# --- Sidebar for Ingredients ---
with st.sidebar:
    st.header("🍳 Pantry Input")
    ingredients = st.text_area("Enter your ingredients (comma-separated)",
                                placeholder="e.g. eggs, tomato, cheese, pasta")
    button = st.button("Suggest Recipe")
    

    st.markdown("### 💡 Example Prompts")
    st.markdown("- What's a quick vegetarian dinner?")
    st.markdown("- Make a lunch with rice and chicken")
    st.markdown("- I want a 15-minute pasta recipe")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    """Yield chat response content from the Groq API response."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def handle_prompt(prompt: str):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            max_tokens=32768,
            stream=True
        )

        with st.chat_message("assistant", avatar="🤖"):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)

        if isinstance(full_response, str):
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            combined_response = "\n".join(str(item) for item in full_response)
            st.session_state.messages.append({"role": "assistant", "content": combined_response})
    except Exception as e:
        st.error(e, icon="🚨")

# Handle sidebar recipe suggestion
if button and ingredients.strip():
    generated_prompt = f"I have the following ingredients: {ingredients.strip()}. Give me recipes using these ingredients?"
    handle_prompt(generated_prompt)

# Handle chat input (main input box at bottom)
if prompt := st.chat_input("Enter your prompt here..."):
    handle_prompt(prompt)