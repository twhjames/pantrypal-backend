---
layout: default
title: Features
nav_order: 4
---

# Features

## Pantry Management

-   Track grocery items, categories, quantities and purchase dates
-   Predict expiry dates using static heuristics or supermarket-specific logic

## Recipe Recommendation & Chatbot

-   Powered by **LLaMA** via the **Groq API**, grounded on recipe and pantry data
-   Supports single prompt recommendations and multi-turn conversations

## Account Management

-   User registration, login, logout, update and delete
-   Token-based authentication using JWT
-   Secure password hashing and session management

## Receipt Processing Pipeline

-   Short-lived AWS S3 upload URLs for receipt images
-   POC microservice (AWS API Gateway + Lambda) for uploading receipts and polling results
-   AWS Textract OCR to extract receipt content
-   Webhook to classify OCR results and add items to the pantry
