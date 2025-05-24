# PantryPal Backend

**PantryPal** is a smart pantry assistant that helps users manage their grocery inventory, predict expiry dates, get personalized recipe suggestions, and interact with a conversational assistant for food-related queries.

This repository contains the **FastAPI backend** services powering the PantryPal system. It exposes RESTful APIs for inventory management, recipe recommendation, and a chatbot powered by a local LLaMA model.

---

## 🚀 Features

- 📦 Inventory Management (Home Inventory Management System - HIMS)
- 🍽️ Recipe Recommendation Engine and Conversational Chatbot
  - Powered by a local **LLaMA** model using a recipe and shelf-life dataset

---

## 🛠️ Tech Stack

| Layer               | Technology                            |
|---------------------|----------------------------------------|
| Framework           | FastAPI (Python 3.12+)                 |
| Database            | SQLite (dev)|
| ORM                 | SQLAlchemy                            |
| Recommender Engine  | LLaMA (local, llama.cpp or HuggingFace) |
| API Documentation   | Swagger (auto-generated)              |
| Testing             | pytest                                |

---

## 📁 Project Structure

```
pantrypal-backend/
├── hims_api/
│   ├── routers/            # /pantry-items routes
│   ├── models.py           # Pydantic + ORM models
│   └── database.py         # DB setup and session config
├── recommender_api/
│   ├── recommender.py      # Core logic for recipe recommendations
│   ├── routes.py           # /recommend endpoint
├── chatbot/
│   ├── llama_llm.py        # LLaMA-based chatbot integration
│   └── routes.py           # /chatbot endpoint
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md
└── tests/                  # Unit/integration tests
```

---
## 🧑‍💻 Developer Guide

### 1. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application (Local Dev)

```bash
uvicorn main:app --reload
```

- Open API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📦 API Endpoints

| Method | Endpoint         | Description                          |
|--------|------------------|--------------------------------------|
| GET    | /pantry/items    | Get all pantry items                 |
| POST   | /pantry/items    | Add new item from receipt            |
| GET    | /recommend       | Get recipe suggestions               |
| POST   | /chatbot         | Ask chatbot a question               |


---
## 🧪 Running Tests

$ pytest

---

### ✨ Future Improvements

- Integrate Huawei Account Kit for user authentication
- Enhance recipe ranking with advanced ML techniques
- Add Redis caching for LLM chatbot performance

---

## 📄 License

This project is licensed under the **Apache 2.0 License**.

---

## 👥 Contributors

- James Teo — Project Lead / Backend Developer

---

## 📬 Feedback / Issues

Please submit issues via GitHub Issues:
https://github.com/twhjames/pantrypal-backend/issues
