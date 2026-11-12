
# AI Health Prediction System

## Project Overview

The AI Health Prediction System is a Flask-based web application designed to manage patient blood test records and generate AI-assisted health insights.

The application collects patient information and blood test values, including glucose, haemoglobin and cholesterol. It sends these values to the Gemini AI API to generate health-related remarks.

The application stores patient records in an SQLite database and provides an interface for hospital staff to manage and search patient information.

## Features

- Patient registration
- View all registered patient records
- Edit patient email addresses
- Delete patient records
- Search patients by name or email
- Input validation for email, date of birth and numerical values
- Prevention of future dates of birth
- SQLite database for persistent storage
- Gemini AI API integration
- AI-generated health remarks based on blood test values
- Tabler-based responsive user interface

## Technologies Used

### Backend
- Python
- Flask
- SQLite

### Frontend
- HTML
- CSS
- Bootstrap 5
- Tabler UI

### AI Integration
- Google Gemini API
- Python Requests
- REST API

## Project Structure

AI_Health_Prediction/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── templates/
│   ├── dashboard.html
│   ├── index.html
│   └── patients.html
│
├── static/
│
└── patients.db

Note: The .env file, virtual environment and database file should not be uploaded to the public GitHub repository.

## Installation and Setup

### 1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL

### 2. Open the project folder

cd AI_Health_Prediction

### 3. Create a virtual environment

python -m venv venv

### 4. Activate the virtual environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1

### 5. Install dependencies

pip install -r requirements.txt

### 6. Configure the Gemini API key

Create a file named .env in the project root directory.

Add your own Gemini API key:

GEMINI_API_KEY=your_api_key_here

Never share or upload your actual API key.

### 7. Run the application

python app.py

### 8. Open the application

http://127.0.0.1:5000

## Application Workflow

1. Open the Hospital Dashboard.
2. Select Add Patient to register a patient.
3. Enter patient details and blood test values.
4. The application sends valid blood test values to the Gemini API.
5. AI-generated health remarks are saved in the SQLite database.
6. Open Patient Records to view patient information and AI remarks.
7. Search for patients using their name or email.
8. Edit or delete patient records when required.

## Input Validation

The application validates:

- Required patient information.
- Email address format.
- Date of birth format.
- Date of birth cannot be in the future.
- Blood test values must be valid non-negative numbers.

## AI Integration

The application uses the Google Gemini API to generate health-related remarks based on:

- Glucose level
- Haemoglobin level
- Total cholesterol level

The generated remarks provide informational interpretations of the entered values.

AI-generated remarks are not medical diagnoses or a replacement for professional medical evaluation.

## Database

SQLite is used to store patient information, blood test values and AI-generated remarks.

Patient records remain stored between application restarts.

## Important Notes

- A valid Gemini API key is required for AI analysis.
- Internet access is required for the external AI API and CDN-hosted UI assets.
- Use synthetic or authorized test data only.
- Do not upload API keys, private patient records or database files to a public repository.

## Author

Saviksha Shetty

MCA Graduate
