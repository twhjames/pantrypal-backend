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

The PantryPal backend follows the **Hexagonal Architecture** (also known as **Ports and Adapters**) pattern to ensure modularity, testability, and clear separation of concerns. It is organized around feature-first modules (e.g., `hims`, `chatbot`) and cleanly separates the business logic from infrastructure code.

The key architectural layers include:

-   **Core (Domain Layer)**: Contains the business logic and service rules for each feature. It defines abstract interfaces (ports) to interact with external systems or infrastructure without depending on specific implementations.
-   **Ports**: Abstract interfaces used by services to access databases, LLMs, OCR tools, or other external systems.
-   **Adapters**: Concrete implementations of ports — such as SQLAlchemy accessors, Groq LLM clients, or OCR adapters.
-   **Application (Controllers)**: Use-case coordinators that bridge the HTTP layer and the core services. These do request handling, validation, and service orchestration.
-   **API Layer (Routers and Schemas)**: Defines FastAPI routes and Pydantic schemas used for request and response validation.
-   **Infrastructure Layer**: Shared utilities such as database session management, configuration loading, and logging.
-   **Playground**: Internal scripts and UI prototypes for LLM prompt engineering and R&D (e.g., Streamlit chatbot).

This modular design allows for:

-   Easy substitution of adapters (e.g., replacing Tesseract with Google Vision API)
-   Reuse of core logic across APIs, CLIs, or background jobs
-   Simplified unit testing by mocking ports during test execution

---

## 📁 Project Structure

```
pantrypal-backend/
├── src/
│
│   ├── core/                                # Feature-agnostic domain logic and abstract contracts
│   │   ├── hims/                            # Home Inventory Management System domain layer
│   │   │   ├── accessors/                   # DB access interfaces (ports) for inventory
│   │   │   └── services/                    # Business logic for pantry management
│   │   └── chatbot/                         # Chatbot domain logic and interfaces
│   │       ├── ports/                       # LLM communication interfaces
│   │       └── services/                    # Prompt orchestration and session logic
│
│   ├── pantrypal_api/                       # Framework-specific and implementation logic
│   │   ├── hims/                            # HIMS FastAPI feature implementation
│   │   │   ├── routers/                     # Route definitions (e.g., /pantry/items)
│   │   │   ├── schemas/                     # Pydantic models for request/response validation
│   │   │   ├── controllers/                 # Request coordination and service delegation
│   │   │   ├── accessors/                   # Concrete DB implementations (e.g., SQLAlchemy)
│   │   │   └── adapters/                    # External tools (OCR, supermarket APIs)
│   │   └── chatbot/                         # Chatbot API and integration logic
│   │       ├── routers/                     # Chatbot-related FastAPI routes
│   │       ├── schemas/                     # Pydantic request/response models
│   │       ├── controllers/                 # Input/output coordination with core logic
│   │       ├── accessors/                   # Groq or other LLM implementations
│   │       └── adapters/                    # Prompt templates and transformation tools
│   │   └── main.py                          # Application entry point with FastAPI setup
│   |
│   └── infrastructure/                      # Shared, low-level technical concerns
│
├── playground/                              # Internal tools and R&D prototypes
│   └── pantrypal_streamlit_chatbot.py       # Streamlit UI for recipe and chat testing
│
├── tests/                                   # Automated tests for core and API logic
│   ├── hims/                                # HIMS-related test suites
│   │   ├── services/                        # Test pantry service logic
│   │   ├── accessors/                       # Test DB interactions
│   │   └── controllers/                     # Test API-level controller logic
│   └── chatbot/                             # Chatbot-related test suites
│       ├── services/                        # Test chatbot prompt/session logic
│       ├── accessors/                       # Test LLM access implementations
│       └── controllers/                     # Test chatbot controller orchestration
│
├── .env                                     # Runtime environment variables
├── .gitignore
├── .pre-commit-config.yaml                  # Git hook configuration for formatting/linting
├── pyproject.toml                           # Tool configuration (e.g., black, isort)
├── requirements.txt
└── README.md
```

---

## ⚙️ Developer Setup

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
uvicorn pantrypal_api.main:app --reload
```

-   This will start the backend API at: [http://localhost:8000](http://localhost:8000)
-   Access the interactive API docs (Swagger UI) at: [http://localhost:8000/docs](http://localhost:8000/docs)
-   For alternative ReDoc docs: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📟 Code Quality & Tooling

This project uses the following tools to ensure consistent code style and quality:

-   **black**: Code formatter
-   **flake8**: Linter for style and logical issues
-   **isort**: Automatically sorts and groups imports
-   **pre-commit**: Runs formatting and linting checks automatically before each commit

### Setup Steps

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

### Configuration Files

-   `pyproject.toml`: Configuration for `black` and `isort`
-   `.flake8`: Configuration for `flake8`
-   `.pre-commit-config.yaml`: Defines pre-commit hook rules and tools

These checks run automatically each time you commit, helping enforce code quality and consistency across the project.

---

## 🧑‍💻 Developer Guide

### Branching Strategy

To contribute a new feature or fix, follow this branching workflow:

```bash
# 1. Switch to the main branch and pull the latest changes
git checkout main
git pull origin main

# 2. Create a new feature branch
git checkout -b feature/your-feature-name
```

### Branch Naming Conventions

Use prefixes based on the purpose of your work:

-   `feature/` – for new features (e.g., `feature/recipe-recommender`)
-   `bugfix/` – for bug fixes (e.g., `bugfix/fix-expiry-date`)
-   `refactor/` – for internal code cleanup

### After Making Changes

```bash
git add .
git commit -m "feat: add recipe recommender logic"
git push origin feature/your-feature-name
```

Then open a **Pull Request (PR)** to merge it into `main` branch.

### Git Commit Message Convention

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
