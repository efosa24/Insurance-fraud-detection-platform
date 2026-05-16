
# Insurance Fraud Detection Platform

A production-ready end-to-end machine learning platform for detecting fraudulent insurance claims using supervised machine learning, FastAPI, Streamlit, Docker, and MLOps best practices.

This project demonstrates how to build, train, deploy, and test a real-world fraud detection system that can be integrated into enterprise insurance analytics workflows.

--------------------------------------------------------------------------------

# Project Overview

Insurance fraud costs the industry billions of dollars annually. This project leverages machine learning to automatically identify potentially fraudulent claims based on historical insurance claim data.

The platform includes:

- Machine learning fraud prediction engine
- Automated preprocessing pipeline
- REST API for real-time scoring
- Interactive web interface
- Dockerized deployment
- GitHub-ready project structure
- Production logging and configuration
- Unit testing
- Scalable architecture

--------------------------------------------------------------------------------

# Technology Stack

## Machine Learning
- Python
- Scikit-learn
- XGBoost
- SMOTE

## Backend
- FastAPI
- Uvicorn

## Frontend
- Streamlit

## Deployment
- Docker
- Docker Compose
- MLflow

--------------------------------------------------------------------------------

# Repository Structure

insurance-fraud-detection-platform/
│
├── app/
│   ├── api/
│   ├── frontend/
│   ├── model/
│   ├── utils/
│   └── artifacts/
│
├── data/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore

--------------------------------------------------------------------------------

# Installation Guide

1. Clone Repository

git clone https://github.com/YOUR_USERNAME/insurance-fraud-detection-platform.git

cd insurance-fraud-detection-platform

--------------------------------------------------------------------------------

2. Create Virtual Environment

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

--------------------------------------------------------------------------------

3. Install Dependencies

pip install -r requirements.txt

--------------------------------------------------------------------------------

4. Train the Model

python app/model/train.py

--------------------------------------------------------------------------------

# Running FastAPI

uvicorn app.api.main:app --reload

API URL:
http://localhost:8000

Swagger Docs:
http://localhost:8000/docs

--------------------------------------------------------------------------------

# Running Streamlit

streamlit run app/frontend/streamlit_app.py

Frontend URL:
http://localhost:8501

--------------------------------------------------------------------------------

# Example API Payload

{
  "Month": "Jan",
  "WeekOfMonth": 1,
  "DayOfWeek": "Monday",
  "Make": "Honda",
  "AccidentArea": "Urban",
  "Age": 35,
  "Fault": "Policy Holder",
  "PolicyType": "Sedan - Collision",
  "VehicleCategory": "Sedan",
  "VehiclePrice": "20000 to 29000",
  "Deductible": 400,
  "DriverRating": 3,
  "Year": 1994,
  "BasePolicy": "Collision"
}

--------------------------------------------------------------------------------

# Example API Response

{
  "fraud_prediction": 1,
  "fraud_probability": 0.8732
}

--------------------------------------------------------------------------------

# Running with Docker

docker-compose up --build

--------------------------------------------------------------------------------

# Unit Testing

pytest

--------------------------------------------------------------------------------

# Recommended Future Improvements

- SHAP Explainability
- JWT Authentication
- PostgreSQL Integration
- CI/CD with GitHub Actions
- Drift Monitoring
- Kafka Streaming

--------------------------------------------------------------------------------

# Author

Festus Eriamiatoe, Ph.D.

Data Scientist | Machine Learning Engineer | AI & Analytics Professional

--------------------------------------------------------------------------------

# License

MIT License
