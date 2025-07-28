---
layout: default
title: Developer Setup
nav_order: 6
---

# Developer Setup

## 1. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Run the API Server

```bash
uvicorn src.app.main:app --reload
```

Visit `http://localhost:8000/docs` for Swagger UI after starting the server.
