# Clinical bert webapp

## Overview

This project is a web application that integrates Optical Character Recognition (OCR) and Named Entity Recognition (NER) functionalities. It includes a FastAPI backend for handling API requests and a Streamlit frontend for user interaction.

## Folder Structure

The project directory is organized as follows:

mvp/

│

├── backend/ # Backend directory containing FastAPI application

│ ├── app/

│ │ ├── api/

│ │ │ ├── v1/

│ │ │ │ ├── endpoints/

│ │ │ │ │ ├── ocr.py # OCR endpoint for handling image uploads and text extraction

│ │ │ │ │ └── ner.py # NER endpoint for handling clinical text and bert model

│ │ │ │ │ └── auth.py # the endpoint for handling authentication and 

│ │ │ │ │ └── translate.py # the endpoint for handling text translation

│ │ │ └── api.py # API router setup

│ │ ├── core/

│ │ │ └── security.py # Security utilities such as password hashing

│ │ ├── models/

│ │ │ └── user.py # Database models

│ │ │ └── database.py # Database connection and setup

│ │ ├── schemas/

│ │ │ └── user.py # Pydantic schemas for request and response validation

│ │ ├── main.py # FastAPI application entry point, here you should include all the endpoints paths

│ │

│ └── requirements.txt # Python dependencies for the backend
│

├── frontend/ # Frontend directory containing Streamlit application

│ ├── pages/

│ │ ├── home.py # Home page with functionality for uploading images and testing endpoints

│ │ ├── entity_detail.py # Page for displaying entity details (if applicable)

│ │ ├── user_profile.py # Page for user profile management (if applicable)

│ │ ├── admin.py # Page for admin functionalities (if applicable)

│ │ └── alerts.py # Page for displaying alerts (if applicable)

│ ├── app.py # Entry point for the Streamlit application, should include all pages here

│ 
├── .gitignore # Git ignore file to exclude files from version control

├── README.md # This README file

└── docker-compose.yml # Docker Compose configuration (if applicable)

└── requirements.txt # Python dependencies for the backend, run pip install


1. Install dependencies:
Navigate to mvp directory and run:
`pip install -r requirements.txt`


2. To run fastapi server, navigate to backend directory and run:
`uvicorn app.main:app --reload`

3. To run streamlit server, navigate to frontend directory and run:
`streamlit run app.py`

