---
layout: default
title: API Reference
nav_order: 7
---

# API Reference

| Method | Endpoint                   | Description                     |
| ------ | -------------------------- | ------------------------------- |
| POST   | /account/register          | Register a new user             |
| POST   | /account/login             | Login with email and password   |
| POST   | /account/logout            | Logout authenticated user       |
| PUT    | /account/update            | Update user information         |
| DELETE | /account/delete            | Delete the user account         |
| POST   | /chatbot/recommend         | One-shot recipe recommendation  |
| POST   | /chatbot/chat              | Multi-turn conversation         |
| GET    | /chatbot/title-suggestions | Quick recipe title ideas        |
| GET    | /pantry/list               | Get all pantry items            |
| POST   | /pantry/add                | Add new pantry items            |
| PUT    | /pantry/update             | Update pantry items             |
| POST   | /pantry/delete             | Delete pantry items             |
| POST   | /receipt/presigned-url     | Obtain an S3 upload URL         |
| POST   | /receipt/webhook           | Webhook for receipt OCR results |

Detailed request and response schemas are available via the Swagger UI at `/docs` once the API server is running.
