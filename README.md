# CardioGuard: Heart Disease Risk Predictor

CardioGuard is a comprehensive web application designed to predict the risk of heart disease in patients using Machine Learning techniques. Built on the Django framework, it provides a robust backend, secure API authentication, and explainable AI insights to assist healthcare professionals and individuals in assessing heart health.

## Features

- **Heart Risk Prediction**: Employs a Random Forest classifier trained on a medical dataset to predict heart disease risk.
- **Explainable AI (XAI)**: Utilizes SHAP (SHapley Additive exPlanations) to provide insights into how each health metric (e.g., Blood Pressure, Age, Heart Rate) contributes to the final risk score.
- **Adaptive Models**: Supports both a full 8-feature model and a reduced 6-feature model (excluding CK-MB and Troponin) for flexible data entry.
- **Role-Based Dashboards**: Provides specialized dashboards for doctors to manage patients and view history, as well as personal dashboards for individual patients.
- **Secure Authentication**: Implements JSON Web Token (JWT) authentication for secure API access and data privacy.
- **RESTful API**: Exposes a clean and well-documented API for seamless integration with varied frontends.

## Tech Stack

- **Backend Framework**: Django 4.2+, Django REST Framework (DRF)
- **Machine Learning**: Scikit-Learn, Pandas, NumPy, SHAP, Joblib
- **Database**: SQLite (Default)
- **Authentication**: SimpleJWT

## Prerequisites

To run this project locally, ensure you have the following installed:
- Python 3.8 or higher
- `pip` (Python package installer)

## Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd HeartRiskArtificialInt
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   Navigate to the backend directory and install the required packages:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Run Database Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Train the Machine Learning Models**
   The application requires the trained models `heart_model.joblib` and `scaler.joblib` to function. Train the models by running:
   ```bash
   python heartproject/ml_model.py
   ```
   *Note: Ensure the dataset `Medicaldataset.csv` is correctly placed inside the `backend/data/` directory before running the script.*

6. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```
   The application will be accessible at: `http://127.0.0.1:8000/`

## Usage

- **Web Interface**: Navigate to `http://127.0.0.1:8000/predict/` to use the interactive prediction form.
- **Doctor Dashboard**: Accessible via `/doctor-dashboard/` to manage multiple patient profiles and view their assessment history.

##  API Endpoints (Overview)

The project exposes several API endpoints for frontend integrations:

- `POST /api/login/` - Obtain JWT Access and Refresh tokens.
- `POST /api/token/refresh/` - Refresh expired access tokens.
- `POST /api/predict-risk/` - Submit health metrics and get a risk prediction + SHAP values.
- `GET /api/history/` - Retrieve the medical assessment history for the authenticated user.
- `GET /api/me/` - Get the current user's profile details.
- `GET /api/patients/` - (Doctors Only) Get a list of associated patients.

## Project Structure

```text
HeartRiskArtificialInt/
│
├── backend/
│   ├── data/                   # ML datasets and saved model artifacts (*.joblib)
│   ├── heartproject/           # Core Django settings, routing, and ML logic
│   ├── predictor/              # Data models (MedicalRecord, Patient)
│   ├── static/                 # Static assets (CSS, JS, Images)
│   ├── templates/              # HTML templates for the frontend views
│   ├── manage.py               # Django management script
│   └── requirements.txt        # Python dependencies
│
└── README.md                   # Project documentation
```
