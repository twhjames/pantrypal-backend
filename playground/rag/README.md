# Recipe Retrieval-Augmented Generation (RAG) - R&D Prototype

This project is an experimental **Retrieval-Augmented Generation (RAG)** pipeline that combines **vector search** with **LLM-powered constraint extraction** to recommend recipes based on user prompts. It leverages **FAISS** for semantic retrieval, **Groq LLM** for natural language understanding, and **pandas** for structured filtering.

---

## Project Structure

```
rag/
├── recipes_metadata.pkl    # Pickled pandas DataFrame containing recipe metadata with nutrition facts and text embeddings
├── recipes.index           # FAISS index file containing pre-computed recipe embeddings
└── retrieval.py            # Retrieval pipeline combining FAISS search, LLM constraint extraction, and result filtering
```

---

## Purpose

This R&D prototype explores how **semantic search** can be combined with **LLM constraint extraction** to:

-   Retrieve **semantically similar recipes** to a user query.
-   **Extract structured constraints** (e.g., calories, sugar, fat limits) from natural language using LLMs.
-   **Filter recipes** based on these constraints to return relevant, healthier, or goal-specific options.

---

## Features

-   **FAISS Vector Search**: Efficient retrieval of semantically similar recipes.
-   **LLM Constraint Extraction**: Uses Groq LLM to parse natural language constraints (e.g., “low sugar”, “under 500 calories”).
-   **Metadata Filtering**: Applies nutritional filters on the recipe metadata after initial retrieval.
-   **Pluggable Embedding Model**: Uses `sentence-transformers` (MiniLM) for embeddings.

---

## How It Works

1. **User Input** → Provide any free-text prompt like:

    - _“Quick dinner under 500 calories”_
    - _“High protein, low carb lunch”_

2. **Constraint Extraction** → LLM extracts nutritional constraints from prompt:

    ```json
    {
        "calories": { "max": 500 },
        "protein": { "min": 30 },
        "sugar": { "max": 5 }
    }
    ```

3. **Semantic Retrieval** → Compute embeddings from the prompt and retrieve top-K nearest recipes using FAISS.

4. **Filtering** → Further filter the top-K based on nutrition constraints in the metadata.

5. **Return Result** → A list of recipe recommendations matching both similarity and nutritional goals.

---

## Quick Start

### 1. Install Requirements

```bash
pip install faiss-cpu pandas sentence-transformers python-dotenv groq
```

### 2. Setup Environment

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key
```

### 3. Example Usage (Python Console)

```python
from retrieval import retrieve_similar_recipes

results = retrieve_similar_recipes("High protein lunch under 600 calories", top_k=20)
print(results)
```

---

## Technologies Used

| Component            | Technology                          |
| -------------------- | ----------------------------------- |
| Vector Search        | FAISS                               |
| Embedding Model      | SentenceTransformers (MiniLM-L6-v2) |
| Language Model (LLM) | Groq API (LLaMA 3.3 70B)            |
| Structured Filtering | pandas                              |
| Data Storage         | Pickle (.pkl), FAISS Index          |
