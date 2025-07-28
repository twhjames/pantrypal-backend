---
layout: default
title: Architecture
nav_order: 5
---

# Architecture

PantryPal follows the **Hexagonal Architecture** (Ports and Adapters). Core domain logic is isolated from infrastructure through well-defined interfaces. Each feature module contains services, accessors, and adapters.

Main layers:

-   **Core Services**: Business logic and domain models
-   **Ports**: Abstract interfaces for databases, LLMs and other systems
-   **Adapters**: Concrete implementations of ports such as SQLAlchemy accessors or the Groq client
-   **Controllers**: Coordinate requests and invoke services
-   **API Layer**: FastAPI routers and Pydantic schemas

This modular design keeps codebase maintainable and testable.
