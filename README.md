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

### 3. Run the API Server Locally

Start the FastAPI development server using Uvicorn:

```bash
uvicorn main:app --reload
```

- This will start the backend API at: [http://localhost:8000](http://localhost:8000)
- Access the interactive API docs (Swagger UI) at: [http://localhost:8000/docs](http://localhost:8000/docs)
- For alternative ReDoc docs: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 4. Creating a Feature Branch

To contribute a new feature or fix, follow this branching workflow:

```bash
# 1. Switch to the main branch and pull the latest changes
git checkout main
git pull origin main

# 2. Create a new feature branch
git checkout -b feature/your-feature-name
```

#### Branch Naming Conventions
Use prefixes based on the purpose of your work:
- `feature/` – for new features (e.g., `feature/recipe-recommender`)
- `bugfix/` – for bug fixes (e.g., `bugfix/fix-expiry-date`)
- `refactor/` – for internal code cleanup
- `hotfix/` – for urgent production fixes

#### After Making Changes

```bash
git add .
git commit -m "feat: add recipe recommender logic"
git push origin feature/your-feature-name
```

Then open a **Pull Request (PR)** to merge it into `main` branch.

#### Git Commit Message Convention

We use **semantic commit prefixes** to keep history clean and meaningful.

| Prefix     | Use for...                                | Example                                 |
|------------|--------------------------------------------|-----------------------------------------|
| `feat:`    | A new feature                              | `feat: add LLaMA integration to chatbot` |
| `fix:`     | A bug fix                                  | `fix: correct expiry prediction logic`  |
| `refactor:`| Code restructuring, no feature or fix      | `refactor: move model logic to utils`   |
| `docs:`    | Documentation-only changes                 | `docs: update README with new endpoints`|
| `test:`    | Adding or updating tests                   | `test: add unit tests for pantry routes`|
| `chore:`   | Misc tasks (e.g., lint, config, cleanup)   | `chore: update dependencies`            |

This helps with:
- Cleaner commit history
- Easier changelogs
- Better collaboration in PRs


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

- [James Teo — Full Stack Software Engineer](https://www.linkedin.com/in/twhjames/)
- [Le Rui — Data Scientist](https://www.linkedin.com/in/le-rui-tay-7b6507272/)

---

## 📬 Feedback / Issues

Please submit issues via GitHub Issues:
https://github.com/twhjames/pantrypal-backend/issues
