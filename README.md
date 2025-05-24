# PantryPal Backend

**PantryPal** is a smart pantry assistant that helps users manage their grocery inventory, predict expiry dates, get personalized recipe suggestions, and interact with a conversational assistant for food-related queries.

This repository contains the **FastAPI backend** services powering the PantryPal system. It exposes RESTful APIs for inventory management, recipe recommendation, and a chatbot powered by a local LLaMA model.

---

## 🚀 Features

-   📦 Inventory Management (Home Inventory Management System - HIMS)
-   🍽️ Recipe Recommendation Engine and Conversational Chatbot
    -   Powered by a local **LLaMA** model using a recipe and shelf-life dataset

---

## 🛠️ Tech Stack

| Layer              | Technology                              |
| ------------------ | --------------------------------------- |
| Framework          | FastAPI (Python 3.12+)                  |
| Database           | SQLite (dev)                            |
| ORM                | SQLAlchemy                              |
| Recommender Engine | LLaMA (local, llama.cpp or HuggingFace) |
| API Documentation  | Swagger (auto-generated)                |
| Testing            | pytest                                  |

---

## 🧱 Software Architecture

The PantryPal backend follows the **Hexagonal Architecture** (also known as **Ports and Adapters**) pattern to ensure modularity, testability, and separation of concerns.

This architecture organizes the codebase into clearly defined layers:

-   **Domain Layer**: Contains core business logic, such as managing pantry items, predicting expiry dates, and generating recipe recommendations.
-   **Ports**: Abstract interfaces that define how the domain interacts with external systems (e.g., LLMs, OCR engines, supermarket APIs).
-   **Adapters**: Concrete implementations of those ports that connect the domain to real-world services like Groq (LLM), Tesseract (OCR), or mock supermarket APIs.
-   **Infrastructure Layer**: Handles persistence, database configuration, and other technical utilities.
-   **Application Layer**: Orchestrates domain logic and delegates tasks to ports and adapters via controllers.
-   **Interface Layer**: Exposes API endpoints via FastAPI and defines the system's external interaction points.

This design allows us to:

-   Easy substitution of external services without impacting core logic (e.g., swap Tesseract for Google Vision)
-   Reusability of domain logic across different interfaces (e.g., CLI, gRPC)
-   Easier unit testing with decoupled dependencies

---

## 📁 Project Structure

```
pantrypal-backend/
├── app/
│   ├── __init__.py
│
│   ├── domain/
│   │   ├── models/                  # SQLAlchemy models (DB tables)
│   │   │   ├── __init__.py
│   │   │   ├── pantry_item.py
│   │   │   ├── receipt.py
│   │   │   └── user.py
│   │   ├── services/                # Business logic (use cases)
│   │   │   ├── pantry_service.py         # Inventory management logic
│   │   │   ├── recommendation_service.py # Recipe generation logic
│   │   │   └── chatbot_service.py        # Conversation flow logic
│   │   └── ports/                   # Abstract Interfaces
│   │       ├── receipt_parser_port.py    # Interface for OCR service
│   │       ├── llm_client_port.py        # Interface for LLM
│   │       └── supermarket_client_port.py# Interface for supermarket sync
│
│   ├── adapters/                 # External implementations
│   │   ├── ocr/                  # OCR engines
│   │   │   └── tesseract_adapter.py
│   │   ├── llm/                  # LLM providers
│   │   │   ├── base.py           # Base LLM client interface
│   │   │   ├── groq_adapter.py   # Groq-specific implementation
│   │   │   └── openai_adapter.py # Optional OpenAI implementation
│   │   └── supermarket/          # External/Mock supermarket systems
│   │       └── mock_api_adapter.py
│
│   ├── infrastructure/          # Database and shared utilities
│   │   ├── database.py
│   │   └── repository.py
│
│   ├── application/             # Use case coordination (controllers)
│   │   └── controllers/
│   │       ├── pantry_controller.py
│   │       ├── receipt_controller.py
│   │       ├── recommender_controller.py
│   │       └── chatbot_controller.py
│
│   └── api/
│       ├── routers/                # FastAPI routes
│       │   ├── pantry.py
│       │   ├── receipt.py
│       │   ├── recommend.py
│       │   └── chatbot.py
│       ├── schemas/                # Pydantic schemas (API contracts)
│       │   ├── pantry.py
│       │   ├── receipt.py
│       │   └── user.py
│       └── main.py                 # FastAPI app entry point
│
├── tests/                       # Unit and integration tests
│   ├── domain/
│   ├── adapters/
│   └── routers/
│
├── .gitignore
├── README.md
├── requirements.txt
└── .env
```

### 📌 Layer Responsibility Summary

| Layer              | Purpose                                            | Example File                                     |
| ------------------ | -------------------------------------------------- | ------------------------------------------------ |
| **Domain**         | Core logic and business rules                      | `models/pantry_item.py`, `pantry_service.py`     |
| **Ports**          | Abstract interfaces for external systems           | `llm_client_port.py`, `receipt_parser_port.py`   |
| **Adapters**       | Concrete implementations for external dependencies | `groq_adapter.py`, `tesseract_adapter.py`        |
| **Infrastructure** | Database and config setup                          | `database.py`, `repository.py`                   |
| **Application**    | Coordinates domain logic and adapters              | `chatbot_controller.py`, `receipt_controller.py` |
| **API**            | FastAPI route handlers                             | `routers/chatbot.py`, `schemas/pantry.py`        |

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
uvicorn pantrypal_core_api.api.main:app --reload
```

-   This will start the backend API at: [http://localhost:8000](http://localhost:8000)
-   Access the interactive API docs (Swagger UI) at: [http://localhost:8000/docs](http://localhost:8000/docs)
-   For alternative ReDoc docs: [http://localhost:8000/redoc](http://localhost:8000/redoc)

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

-   `feature/` – for new features (e.g., `feature/recipe-recommender`)
-   `bugfix/` – for bug fixes (e.g., `bugfix/fix-expiry-date`)
-   `refactor/` – for internal code cleanup
-   `hotfix/` – for urgent production fixes

#### After Making Changes

```bash
git add .
git commit -m "feat: add recipe recommender logic"
git push origin feature/your-feature-name
```

Then open a **Pull Request (PR)** to merge it into `main` branch.

#### Git Commit Message Convention

We use **semantic commit prefixes** to keep history clean and meaningful.

| Prefix      | Use for...                               | Example                                  |
| ----------- | ---------------------------------------- | ---------------------------------------- |
| `feat:`     | A new feature                            | `feat: add LLaMA integration to chatbot` |
| `fix:`      | A bug fix                                | `fix: correct expiry prediction logic`   |
| `refactor:` | Code restructuring, no feature or fix    | `refactor: move model logic to utils`    |
| `docs:`     | Documentation-only changes               | `docs: update README with new endpoints` |
| `test:`     | Adding or updating tests                 | `test: add unit tests for pantry routes` |
| `chore:`    | Misc tasks (e.g., lint, config, cleanup) | `chore: update dependencies`             |

This helps with:

-   Cleaner commit history
-   Easier changelogs
-   Better collaboration in PRs

---

## 📦 API Endpoints

| Method | Endpoint      | Description               |
| ------ | ------------- | ------------------------- |
| GET    | /pantry/items | Get all pantry items      |
| POST   | /pantry/items | Add new item from receipt |
| GET    | /recommend    | Get recipe suggestions    |
| POST   | /chatbot      | Ask chatbot a question    |

---

## 🧪 Running Tests

```bash
pytest
```

---

## 📟 Developer Environment & Code Quality Setup

This project uses the following tools to ensure consistent code style and quality:

-   **black**: Code formatter
-   **flake8**: Linter for style and logical issues
-   **isort**: Automatically sorts and groups imports
-   **pre-commit**: Runs formatting and linting checks automatically before each commit

### ⚙️ Setup Steps

1. **Install the required tools**:

```bash
pip install black flake8 isort pre-commit
```

2. **Set up the pre-commit hook**:

A `.pre-commit-config.yaml` file is included at the project root. To enable the hook:

```bash
pre-commit install
```

3. **(Optional) Run all checks manually**:

```bash
pre-commit run --all-files
```

### 🧰 Configuration Files

-   `pyproject.toml`: Configuration for `black` and `isort`
-   `.flake8`: Configuration for `flake8`
-   `.pre-commit-config.yaml`: Defines pre-commit hook rules and tools

These checks run automatically each time you commit, helping enforce code quality and consistency across the project.

---

### ✨ Future Improvements

-   Integrate Huawei Account Kit for user authentication
-   Enhance recipe ranking with advanced ML techniques
-   Add Redis caching for LLM chatbot performance

---

## 📄 License

This project is licensed under the **Apache 2.0 License**.

---

## 👥 Contributors

-   [James Teo — Full Stack Software Engineer](https://www.linkedin.com/in/twhjames/)
-   [Le Rui — Data Scientist](https://www.linkedin.com/in/le-rui-tay-7b6507272/)

---

## 📬 Feedback / Issues

Please submit issues via GitHub Issues:
https://github.com/twhjames/pantrypal-backend/issues
