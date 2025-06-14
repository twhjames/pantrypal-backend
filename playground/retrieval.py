# retrieval.py
import faiss
import pandas as pd
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import random
import os
import json
from dotenv import load_dotenv
load_dotenv() 

# Load metadata
with open("../../Data/recipes_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

# Load FAISS index
faiss_index = faiss.read_index("../../Data/recipes.index")

# Using LLM to extract possible constraints to help reduce the metadata df
def extract_constraints_from_prompt(user_input: str) -> dict:
    instruction = f"""
    You are a helpful assistant.
    Your task is to extract **numeric constraints** from a user prompt.

    Return constraints **only if they are clearly stated**.  
    If a constraint is not specified, leave it as `null` (i.e., None).

    Return the result as **valid JSON** with the following format:

    {{
    "calories": {{"min": null, "max": null}},                  // in kcal
    "total_fat": {{"min": null, "max": null}},                 // in % daily value (PDV)
    "sugar": {{"min": null, "max": null}},                     // in % PDV
    "sodium": {{"min": null, "max": null}},                    // in % PDV
    "protein": {{"min": null, "max": null}},                   // in % PDV
    "saturated_fat": {{"min": null, "max": null}},             // in % PDV
    "total_carbohydrates": {{"min": null, "max": null}},       // in % PDV
    "n_steps": {{"min": null, "max": null}},                   // number of steps in cooking the dish
    "n_ingredients": {{"min": null, "max": null}}              // number of ingredients in cooking the dish
    }}

    ### Units:
    - **Calories** are measured in **kcal**.  
    - All other nutritional fields are measured in **percent daily value (%DV)**.
    - If a user specifies grams or milligrams, **convert to %DV** using standard assumptions:
      - Fat: 78g = 100% DV
      - Sugar: 50g = 100% DV
      - Sodium: 2300mg = 100% DV
      - Protein: 50g = 100% DV
      - Saturated fat: 20g = 100% DV
      - Carbohydrates: 275g = 100% DV

    ### Examples:
    Prompt: “I want under 500 calories and at least 10g of protein.”
    Output:
    {{
    "calories": {{"min": null, "max": 500}},
    "protein": {{"min": 20, "max": null}},  // 10g is 20% DV
    ...
    }}

    Prompt: “Low sugar and sodium, like under 5%”
    Output:
    {{
    "sugar": {{"min": null, "max": 5}},
    "sodium": {{"min": null, "max": 5}},
    ...
    }}

    """

    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts structured constraints."},
            {"role": "user", "content": instruction},
            {"role": "user", "content": f"Prompt: {user_input}"}
        ],
        temperature=0
    )

    try:
        response_content = completion.choices[0].message.content
        constraints = json.loads(response_content)
        return constraints
    except Exception as e:
        print(f"Failed to parse constraints: {e}")
        # Return default empty constraints if parsing fails
        return {
            "calories": {"min": None, "max": None},                  
            "total_fat": {"min": None, "max": None},                 
            "sugar": {"min": None, "max": None},                     
            "sodium": {"min": None, "max": None},                   
            "protein": {"min": None, "max": None},                   
            "saturated_fat": {"min": None, "max": None},            
            "total_carbohydrates": {"min": None, "max": None},
            "n_steps": {"min": None, "max": None},
            "n_ingredients": {"min": None, "max": None}
        }

# Filters the metadata based on users prompts
def filter_by_constraints(df, constraints):
    filtered = df.copy()
    for key, bounds in constraints.items():
        if bounds["min"] is not None:
            filtered = filtered[filtered[key] >= bounds["min"]]
        if bounds["max"] is not None:
            filtered = filtered[filtered[key] <= bounds["max"]]
    return filtered

def get_embedding(text: str) -> np.ndarray:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode([text]).astype("float32")
    return query_embedding

def retrieve_similar_recipes(text, top_k=20):
    constraints = extract_constraints_from_prompt(text)

    query_embedding = get_embedding(text)

    D, I = faiss_index.search(query_embedding, top_k)
    relevant_df = metadata.iloc[I[0], :]
    filtered_df = filter_by_constraints(relevant_df, constraints)

    results = []
    for _, row in filtered_df.iterrows():
        results.append({
            "name": row["name"],
            "text": row["text_for_embedding"],
            "id": row["id"]
        })
    return results

# Optional: alternative retrieve function with random sampling to avoid repetitive results
def retrieve_similar_recipes_sampled(query_embedding, top_k=50, display_k=5):
    distances, indices = faiss_index.search(query_embedding, top_k)
    results = metadata.iloc[indices[0], :].copy()
    results["distance"] = distances[0]
    results = results.sort_values("distance")
    sampled_results = results.sample(n=min(display_k, len(results)), random_state=random.randint(0, 1000))
    return sampled_results
