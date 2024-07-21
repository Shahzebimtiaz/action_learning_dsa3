# Clinical bert webapp

## Overview

This project is a web application that integrates Optical Character Recognition (OCR) and Named Entity Recognition (NER) functionalities. It includes a FastAPI backend for handling API requests and a Streamlit frontend for user interaction.

## Folder Structure

The project directory is organized as follows:

mvp/<br>
│<br>
├── backend/ # Backend directory containing FastAPI application<br>
│ ├── app/<br>
│ │ ├── api/<br>
│ │ │ ├── v1/<br>
│ │ │ │ ├── endpoints/<br>
│ │ │ │ │ ├── ocr.py # OCR endpoint for handling image uploads and text extraction<br>
│ │ │ │ │ └── ner.py # NER endpoint for handling clinical text and bert model<br>
│ │ │ │ │ └── auth.py # the endpoint for handling authentication and <br>
│ │ │ │ │ └── translate.py # the endpoint for handling text translation<br>
│ │ │ │ │ └── admin.py # the endpoint for handling user creation, deletion, logging...<br>
│ │ │ └── api.py # API router setup, add all endpoint py files to this file<br>
│ │ │ │ │ └── auth.py # the endpoint for handling authentication and<br>
│ │ │ │ │ └── translate.py # the endpoint for handling text translation<br>
│ │ │ └── api.py # API router setup<br>
│ │ ├── core/<br>
│ │ │ └── security.py # Security utilities such as password hashing<br>
│ │ ├── models/<br>
│ │ │ └── user.py # Database models<br>
│ │ │ └── schemas.py # Database connection and <br>
│ │ │ └── database.py # Database connection and setup<br>
│ │ ├── schemas/<br>
│ │ │ └── user.py # Pydantic schemas for request and response validation<br>
│ │ ├── main.py # FastAPI application entry point, here you should include all the endpoints paths<br>
│ │<br>
│ └── requirements.txt # Python dependencies for the backend<br>
│
├── frontend/ # Frontend directory containing Streamlit application<br>
│ ├── pages/<br>
│ │ ├── home.py # Home page with functionality for uploading images and testing endpoints<br>
│ │ ├── entity_detail.py # Page for displaying entity details (if applicable)<br>
│ │ ├── user_profile.py # Page for user profile management (if applicable)<br>
│ │ ├── admin.py # Page for admin functionalities (if applicable)<br>
│ │ └── alerts.py # Page for displaying alerts (if applicable)<br>
│ ├── app.py # Entry point for the Streamlit application, should include all pages here<br>
│ 
├── .gitignore # Git ignore file to exclude files from version control<br>
├── README.md # This README file<br>
└── docker-compose.yml # Docker Compose configuration (if applicable)<br>
└── requirements.txt # Python dependencies for the backend, run pip install<br>


1. Install dependencies:
Navigate to mvp directory and run:
`pip install -r requirements.txt`

2. Setup postgresql database:

To set up the PostgreSQL database for the project, follow these steps:

* Installation:

   - Go to [PostgreSQL Download Page](https://www.postgresql.org/download/) and download the appropriate installer for your operating system.
   - Follow the on-screen installation instructions.
   - During installation, you will be prompted to create a new admin password.
   - Leave the connection port as 5432.

* Create a New PostgreSQL Server:

   - Open pgAdmin 4.
   - Enter the admin password you input during installation.
   - Create a new server named `action_learning_dsa3`.
   - In the Connection tab, enter the Host name/address as `localhost` and keep the port as `5432`.
   - Default username: `postgres`
   - Password: admin password specified during installation.
   - Save the settings.

* Create a New Database:

   - Right-click on Databases under the `clinicalbert_app` and choose Create -> Database.
   - Name the database: `clinicalbert_app`.
   - Save the settings.

* Create Tables:

Execute the sql script in folder `backend/models/create_tables.sql` using pgAdmin query tool.


2. To run fastapi server, navigate to backend directory and run:
`uvicorn app.main:app --reload`

3. To run streamlit server, navigate to frontend directory and run:
`streamlit run app.py`

