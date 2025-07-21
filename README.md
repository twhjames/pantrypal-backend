# PantryPal Backend

**PantryPal** is a smart pantry assistant that helps users manage their grocery inventory, predict expiry dates, get personalized recipe suggestions, and interact with a conversational assistant for food-related queries.

This repository contains the **FastAPI backend** services powering the PantryPal system. It exposes RESTful APIs for inventory management, recipe recommendation, and a chatbot powered by a local LLaMA model.

---

## 📚 Table of Contents

-   [🚀 Features](#-features)
-   [🛠️ Tech Stack](#️-tech-stack)
-   [🧱 Software Architecture](#-software-architecture)
-   [📁 Project Structure Overview](#-project-structure-overview)
-   [⚙️ Developer Setup](#️-developer-setup)
-   [🔐 Environment Variables](#-environment-variables)
-   [🧑‍💻 Developer Guide](#-developer-guide)
-   [📦 API Endpoints](#-api-endpoints)
-   [🧪 Running Tests](#-running-tests)
-   [🪵 Logging](#-logging)
-   [✨ Future Improvements](#-future-improvements)
-   [📄 License](#-license)
-   [👥 Contributors](#-contributors)
-   [📬 Feedback / Issues](#-feedback--issues)

---

## 🚀 Features

-   🧺 Pantry Management System
    -   Track grocery items, categories, quantities, and purchase dates
    -   Predict expiry dates with static heuristics or dynamic supermarket-specific logic
-   🍽️ Recipe Recommendation Engine and Conversational Chatbot
    -   Powered by **LLaMA** via the **Groq API**, grounded on recipe and pantry expiry data
-   🔐 Account Management System
    -   User registration, login, logout, update, and delete
    -   Token-based authentication with JWT
    -   Secure password hashing and session management

---

## 🛠️ Tech Stack

| Layer              | Technology                                         |
| ------------------ | -------------------------------------------------- |
| Framework          | FastAPI (Python 3.12+)                             |
| Database           | SQLite (development)                               |
| ORM                | SQLAlchemy                                         |
| Recommender Engine | LLaMA via Groq API (hosted inference)              |
| Authentication     | JWT (via `python-jose`) + bcrypt                   |
| API Documentation  | Swagger (auto-generated)                           |
| Admin Panel        | SQLAdmin + Tabler UI                               |
| Migrations         | Alembic                                            |
| Logging            | Python `logging` (via custom `AppLoggingProvider`) |
| Testing            | `pytest`, `pytest-asyncio`, `httpx`, `coverage`    |

---

## 🧱 Software Architecture

The PantryPal backend follows the **Hexagonal Architecture** (also known as **Ports and Adapters**) pattern to ensure modularity, testability, and clear separation of concerns. It is organized around feature-first modules (e.g. `chatbot`, `pantry`) and cleanly separates the business logic from infrastructure code.

The key architectural layers include:

-   **Core (Domain Layer)**: Contains the business logic and service rules for each feature. It defines abstract interfaces (ports) to interact with external systems or infrastructure without depending on specific implementations.
-   **Ports**: Abstract interfaces used by services to access databases, LLMs, OCR tools, or other external systems.
-   **Adapters**: Concrete implementations of ports — such as SQLAlchemy accessors, Groq LLM clients, or OCR adapters.
-   **Application (Controllers)**: Use-case coordinators that bridge the HTTP layer and the core services. These do request handling, validation, and service orchestration.
-   **API Layer (Routers and Schemas)**: Defines FastAPI routes and Pydantic schemas used for request and response validation.
-   **Playground**: Internal scripts and UI prototypes for LLM prompt engineering and R&D (e.g., Streamlit chatbot).

This modular design allows for:

-   Easy substitution of adapters (e.g., replacing Tesseract with Google Vision API)
-   Reuse of core logic across APIs, CLIs, or background jobs
-   Simplified unit testing by mocking ports during test execution

---

## 📁 Project Structure Overview

The file structure reflects the Hexagonal Architecture principles outlined above, organizing code around feature modules (like `chatbot`, `pantry`) and layering them across core domain logic, application services, and framework-specific interfaces.

This overview helps you navigate the folders and understand where to implement or extend new features.

### 🗂️ Folder Layout and Responsibilities

| Path                                       | Description                                                             |
| ------------------------------------------ | ----------------------------------------------------------------------- |
| `alembic/`                                 | Alembic migration environment and versioned DB migration scripts        |
| `logs/`                                    | Runtime log files generated by `AppLoggingProvider`                     |
| `playground/`                              | R&D space: Streamlit prototypes, prompt engineering, and internal tools |
| `src/app/`                                 | App setup: middleware, logging, global config, and FastAPI `main.py`    |
| `src/core/common/`                         | Shared utilities: enums, constants, timestamps, validation helpers      |
| `src/core/base/`                           | Abstract base domain models (`@dataclass`) used across features         |
| `src/core/<feature>/services/`             | Pure business logic (no dependencies on web/infra)                      |
| `src/core/<feature>/accessors/`            | Abstract interfaces (ports) for DB, LLM, or external systems            |
| `src/core/<feature>/ports/`                | Outbound interfaces (e.g., LLM, OCR, file storage)                      |
| `src/core/<feature>/specs.py`              | Data transfer specs (DTOs, query structures)                            |
| `src/core/<feature>/models.py`             | Domain models (not tied to SQLAlchemy or DB)                            |
| `src/core/<feature>/modules.py`            | DI bindings for each feature (e.g., `injector.Module`)                  |
| `src/pantrypal_api/<feature>/routers/`     | FastAPI route definitions per feature                                   |
| `src/pantrypal_api/<feature>/schemas/`     | Pydantic models for validation and serialization                        |
| `src/pantrypal_api/<feature>/controllers/` | Controllers: bridge HTTP input with core services                       |
| `src/pantrypal_api/<feature>/accessors/`   | Concrete DB access logic (e.g., SQLAlchemy ORM queries)                 |
| `src/pantrypal_api/<feature>/adapters/`    | Prompt templates, response formatters, API adapters                     |
| `src/pantrypal_api/admin/<feature>/`       | SQLAdmin UI: feature-specific admin panel views                         |
| `src/pantrypal_api/base/`                  | SQLAlchemy base model declarations for infrastructure ORM               |
| `tests/<feature>/`                         | Unit and integration tests for services, controllers, and adapters      |

> 💡 Note: Alembic is intentionally placed outside the main application (`src/`) to treat it as a standalone dev tool.
> 👉 This separation avoids coupling database migration logic with the core domain or dependency injection system, preserving Hexagonal Architecture principles and modularity.

---

### 📄 Top-Level Files

| File                      | Description                                                          |
| ------------------------- | -------------------------------------------------------------------- |
| `.env`                    | Environment variables (e.g., DB URL, API keys) for local development |
| `.flake8`                 | Linting rules for `flake8`                                           |
| `.gitignore`              | Git version control exclusion rules                                  |
| `.pre-commit-config.yaml` | Git pre-commit hook config (e.g., black, isort, flake8)              |
| `LICENSE`                 | Project license (e.g., Apache 2.0)                                   |
| `pantrypal.db`            | SQLite development DB (excluded in production)                       |
| `pyproject.toml`          | Tool configuration: black, isort, pytest, etc.                       |
| `README.md`               | Documentation entry point                                            |
| `requirements.txt`        | Python package dependencies                                          |
| `alembic.ini`             | Alembic configuration file (includes DB connection and script paths) |

---

### 📦 Module Responsibilities

| Module          | Description                                                                |
| --------------- | -------------------------------------------------------------------------- |
| `account`       | Manages user registration, login, update, deletion, and JWT authentication |
| `admin`         | SQLAdmin views for managing `chatbot` and `configuration` models           |
| `chatbot`       | Handles LLM-based chat, recipe suggestions, and multi-turn conversations   |
| `configuration` | Stores runtime config values editable via the admin panel                  |
| `common`        | Shared constants, enums, datetime helpers, and secret providers            |
| `expiry`        | Predicts expiry dates based on item category or supermarket-specific logic |
| `logging`       | Provides centralized application logging using the Python `logging` module |
| `pantry`        | Manages pantry item CRUD operations and user grocery inventory             |
| `storage`       | Abstracts storage layers (e.g., DB providers, cloud object stores)         |

---

> 🧠 Note: This structure scales well with additional modules and promotes separation of concerns across core logic, HTTP interface, and infrastructure.

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
uvicorn src.app.main:app --reload
```

-   This will start the backend API at: [http://localhost:8000](http://localhost:8000)
-   Access the interactive API docs (Swagger UI) at: [http://localhost:8000/docs](http://localhost:8000/docs)
-   For alternative ReDoc docs: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🔐 Environment Variables

PantryPal uses environment variables to configure database connections and external services. These variables should be defined in a `.env` file at the project root.

| Variable                    | Description                                                           |
| --------------------------- | --------------------------------------------------------------------- |
| `DATABASE_URL`              | Async DB URL for FastAPI (e.g., `sqlite+aiosqlite:///./pantrypal.db`) |
| `ALEMBIC_DATABASE_URL`      | Sync DB URL for Alembic (e.g., `sqlite:///./pantrypal.db`)            |
| `GROQ_API_KEY`              | API key for Groq LLM provider                                         |
| `CHATBOT_MODEL`             | Model name for Groq/Gemma/LLaMA                                       |
| `CHATBOT_MAX_TOKENS`        | Max tokens in chatbot response (e.g., 1024)                           |
| `CHATBOT_MAX_CHAT_HISTORY`  | Number of past messages to include in context                         |
| `AUTH_SECRET_KEY`           | Secret key for signing JWT tokens                                     |
| `AUTH_ALGORITHM`            | Algorithm for JWT signing (e.g., `HS256`)                             |
| `AUTH_TOKEN_EXPIRY_MINUTES` | Token expiry duration in minutes (e.g., `1440`)                       |
| `ADMIN_USERNAME`            | Username for the admin account                                        |
| `ADMIN_EMAIL`               | Email for the admin account                                           |
| `ADMIN_PASSWORD`            | Password for the admin account                                        |

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

### Database Migrations

PantryPal uses **Alembic** to manage database schema migrations in a version-controlled and reproducible manner.

Alembic works in tandem with our SQLAlchemy models to track and apply schema changes over time.

#### Adding a New Database Table

To add a new table:

1. **Define the model** in the relevant module:

    - Add your SQLAlchemy model to `src/pantrypal_api/<feature>/models.py`
    - Use standard SQLAlchemy syntax for fields and relationships

2. **Register the model** for Alembic to detect:

    - Import it into `src/pantrypal_api/models.py`:
        ```python
        from src.pantrypal_api.<feature>.models import *  # noqa
        ```

3. **Generate and apply the migration**:
    ```bash
    alembic revision --autogenerate -m "add <your-table-name> table"
    alembic upgrade head
    ```

#### Common Alembic Commands

-   Revert the most recent migration:

    ```bash
    alembic downgrade -1
    ```

-   Upgrade to a specific revision:
    ```bash
    alembic upgrade <revision_id>
    ```

> ⚠️ Alembic reads metadata from `src/core/base/models.py` via `target_metadata` in `env.py`.
> ✅ Ensure all models are imported into `src/pantrypal_api/models.py` so Alembic can detect them.
> 📁 Migration scripts are stored in the `alembic/versions/` directory.

#### 🧠 Why Two Environment Variables?

PantryPal uses **SQLAlchemy with an async driver (`sqlite+aiosqlite`)** for the FastAPI app, while **Alembic requires a sync engine**. To support both, we define **two separate environment variables**:

```env
# .env
DATABASE_URL=sqlite+aiosqlite:///./pantrypal.db         # Used by the async FastAPI app
ALEMBIC_DATABASE_URL=sqlite:///./pantrypal.db           # Used by Alembic (sync)
```

In `alembic/env.py`, we explicitly load `ALEMBIC_DATABASE_URL` for migrations:

```python
import os
from dotenv import load_dotenv

load_dotenv()
ALEMBIC_DATABASE_URL = os.getenv("ALEMBIC_DATABASE_URL")
```

> ✅ This separation prevents runtime errors and ensures clean integration between Alembic and our async application architecture.

### Admin Interface

PantryPal includes a custom-styled **SQLAdmin** panel for managing core system resources through a user-friendly web interface.

Once the FastAPI server is running, access the admin dashboard at:
[http://localhost:8000/admin](http://localhost:8000/admin)

Use the SQLAdmin login form at `/admin/login` with your configured admin
credentials. After authenticating, a bearer token is stored in a secure cookie
and you can visit `/docs` to use Swagger with the same credentials.

The dashboard offers:

-   A customizable landing page with card-based UI powered by Tabler CSS
-   Intuitive CRUD operations for registered models like chat history and configuration values
-   Model-level filtering, sorting, searching, and export capabilities
-   An alternative to external tools like SQLite Browser or raw SQL queries

> **Admin Credentials**
>
> The admin dashboard is protected by credentials sourced from environment
> variables. Define `ADMIN_USERNAME`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD`
> in your `.env` file **before** starting the server. Missing values will
> prevent the application from booting. After setting these variables,
> run `python scripts/create_superuser.py` once to create the initial admin
> account.

Admin views are defined using SQLAdmin’s `ModelView` inheritance and registered via `PantryPalAdminSite` in:

```bash
src/pantrypal_api/admin/<feature>/admin.py
```

> 🧠 **Note**: All admin models inherit from a shared `PantryPalModelAdmin` base class that applies consistent UI behavior, searchability, and icon settings across the dashboard.

---

## 📦 API Endpoints

| Method | Endpoint                   | Description                        |
| ------ | -------------------------- | ---------------------------------- |
| POST   | /account/register          | Register a new user                |
| POST   | /account/login             | Login with email and password      |
| POST   | /account/logout            | Logout (use Authorization header)  |
| PUT    | /account/update            | Update user information            |
| DELETE | /account/delete            | Delete the user account            |
| POST   | /chatbot/recommend         | Get one-shot recipe recommendation |
| POST   | /chatbot/chat              | Start multi-turn conversation      |
| GET    | /chatbot/title-suggestions | Quick list of recipe title ideas   |
| GET    | /pantry/list               | Get all pantry items for a user    |
| POST   | /pantry/add                | Add new pantry items               |
| PUT    | /pantry/update             | Update existing pantry items       |
| POST   | /pantry/delete             | Delete pantry items by ID          |

Visit `/docs` for full Swagger documentation.

### Authenticating in Swagger UI

Access to `/docs` is restricted to admin users. Navigate to `/admin/login`, sign in with the credentials configured in your `.env`, and the server will set a cookie allowing you to open the Swagger
interface.

---

## 🧪 Running Tests

PantryPal's test suite is built with `pytest`, reflecting the project’s Hexagonal Architecture. It supports async testing using `pytest-asyncio`, `AsyncMock`, and `httpx.AsyncClient`, with a focus on isolating and integrating each feature module.

### 🗂️ Test Folder Overview

Tests are organized by feature and layer, mirroring the structure of the source code in `src/`. This keeps domain logic, adapters, and HTTP-facing interfaces cleanly separated.

| Module          | Layer         | Purpose                                                 |
| --------------- | ------------- | ------------------------------------------------------- |
| `account`       | `services`    | Auth logic (registration, login, token management)      |
|                 | `accessors`   | Database interactions for user accounts                 |
|                 | `adapters`    | Password hashing, token encoding                        |
|                 | `controllers` | API tests for `/account` routes                         |
| `chatbot`       | `services`    | Unit tests for chatbot business logic                   |
|                 | `accessors`   | Tests for chat history access layer (abstract or DB)    |
|                 | `adapters`    | Integration tests for LLM adapters (e.g. Groq)          |
|                 | `controllers` | API tests for `/chatbot` endpoints                      |
| `common`        | `adapters`    | Secret key provider implementation                      |
|                 | `utils`       | Tests for shared utilities (e.g., time, constants)      |
| `configuration` | `services`    | Runtime config update and retrieval logic               |
|                 | `accessors`   | DB access for config values                             |
| `expiry`        | `services`    | Predict expiry dates by category or supermarket logic   |
| `pantry`        | `services`    | Unit tests for pantry logic (add, update, delete items) |
|                 | `accessors`   | Tests for concrete DB access using SQLAlchemy           |
|                 | `controllers` | API tests for `/pantry/items` endpoints                 |
| `storage`       | `adapters`    | Storage layer (e.g., relational DB access)              |
| `conftest.py`   | —             | Shared fixtures for app, DB, and client setup           |

### ✅ Test Coverage

-   **Unit Tests** focus on core business logic in `src/core/<feature>/services/`, using mocks for external dependencies such as accessors or LLMs.
-   **Integration Tests** validate concrete implementations of ports/adapters (e.g., database accessors, Groq provider) to ensure proper system interactions.
-   **API Tests** use `httpx.AsyncClient` to test FastAPI routes asynchronously, covering authentication, chatbot functionality, and configuration endpoints.
-   **Admin Tests** verify that the SQLAdmin dashboard loads correctly and supports basic CRUD operations on registered models.

### 🧪 Running the Test Suite

To run all tests:

```bash
pytest tests
```

To run a specific test module:

```bash
pytest tests/chatbot/services/test_chatbot_service.py
```

### 🔍 Additional Tools

-   **Async tests** use `pytest-asyncio`
-   **Test client** is defined in `conftest.py` using `httpx.AsyncClient` for full app-level testing
-   **Coverage** reports can be generated using:

```bash
# 1. Run tests with coverage
coverage run -m pytest tests/

# 2. Show a terminal report
coverage report

# 3. Generate an HTML report
coverage html

# 4. Open it in browser
open htmlcov/index.html
```

> All tests are designed to be modular, fast, and consistent with the project’s separation of concerns. They can be run independently of external services by mocking interfaces like storage and LLMs.

---

## 🪵 Logging

PantryPal uses a custom logging adapter (`AppLoggingProvider`) that implements the `ILoggingProvider` interface.

-   **Location**: `src/pantrypal_api/logging/adapters/app_logging_provider.py`
-   **Backend**: Built on Python’s standard `logging` module
-   **Output**: Logs are written to `logs/pantrypal.log`
-   **Log Level**: Default is `WARNING` and above (i.e., `INFO` and `DEBUG` are skipped to conserve log space)
-   **Format**: `[LEVEL] TIMESTAMP — [TAG] Message | Extra: {...}`

> ⚠️ Avoid logging sensitive information like passwords, tokens, or PII.

#### Example usage in services

```python
self.logging_provider.warning("Login failed", extra_data={"email": spec.email}, tag="Auth")
```

---

## ✨ Future Improvements

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
