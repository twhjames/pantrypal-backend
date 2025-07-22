# Receipt Pipeline: R&D Prototype for Automated Receipt Classification

This project explores an end-to-end Receipt Processing Pipeline, combining OCR extraction, AI-powered classification, and API serving.

## Project Structure

receipt_pipeline/
│
├── aws_lambda/
│ └── lambda_receipt_ocr.py # AWS Lambda function for OCR and basic receipt parsing using Textract and Comprehend.
│
└── fastapi/
└── main.py # FastAPI service for uploading receipt images, retrieving processed receipt data, and AI-based classification using LLM (Groq).

## Purpose

This R&D effort aims to:

-   Automate receipt data extraction from images using AWS Textract.
-   Process and store structured receipt data on AWS S3 and DynamoDB.
-   Classify individual receipt items into subcategories using LLM (Groq API).
-   Serve API endpoints via FastAPI for a smooth developer experience.

## Features

-   AWS Textract for automated OCR extraction of receipt data.
-   Groq API for LLM-powered item classification and constraint extraction.
-   FastAPI for quick and scalable API prototyping and serving.

## Components Explained

1. AWS Lambda (aws_lambda/lambda_receipt_ocr.py):

-   Handles image uploads to S3 and triggers Textract to extract receipt details.
-   Saves processed receipt metadata (Vendor, Date, Total, Line Items) to:
    -   S3 Bucket (for results)
    -   DynamoDB (for status tracking)

2. FastAPI Service (fastapi/main.py):

-   Provides API endpoints for:
    -   Uploading receipt images to AWS Lambda
    -   Retrieving receipt extraction results
    -   Classifying receipt items into food/non-food categories with subcategories via LLM (Groq).

## Technologies Used

| Component         | Tech Stack                         |
| ----------------- | ---------------------------------- |
| Cloud Processing  | AWS Lambda, Textract, S3, DynamoDB |
| Backend API       | FastAPI                            |
| AI Classification | Groq API (LLaMA3 70B)              |
| Environment Mgmt  | Python + dotenv                    |
| Infrastructure    | Local Development + AWS Cloud      |

## 🚀 How to Use

1. **Setup environment variables:**
   Create a .env file with:
   GROQ_API_KEY=your_groq_key
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret

Configure your AWS CLI or use IAM roles if deploying Lambda.

2. **Run FastAPI (for API routes):**
   cd fastapi
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

3. **Deploy Lambda (via AWS Console or AWS SAM):**
   Upload aws_lambda/lambda_receipt_ocr.py as your Lambda function.
