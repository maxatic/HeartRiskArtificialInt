"""
Machine Learning model for heart disease risk prediction.
Uses the Kaggle Medical Dataset to train a Random Forest classifier.
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from pathlib import Path
import joblib

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'data' / 'Medicaldataset.csv'
MODEL_PATH = BASE_DIR / 'data' / 'heart_model.joblib'

# Feature columns in order
FEATURE_COLUMNS = [
    'Age', 'Gender', 'Heart rate', 
    'Systolic blood pressure', 'Diastolic blood pressure',
    'Blood sugar', 'CK-MB', 'Troponin'
]


def load_and_prepare_data():
    """
    Load the medical dataset and prepare it for training.
    
    Returns:
        tuple: (X features DataFrame, y target Series)
    """
    df = pd.read_csv(DATA_PATH)
    
    # Features (X) and target (y)
    X = df[FEATURE_COLUMNS]
    y = (df['Result'] == 'positive').astype(int)
    
    return X, y


def train_model(test_size=0.2, random_state=42):
    """
    Train the heart risk prediction model and save it.
    
    Args:
        test_size: Fraction of data to use for testing
        random_state: Random seed for reproducibility
    
    Returns:
        dict: Training results including accuracy and classification report
    """
    print("Loading data...")
    X, y = load_and_prepare_data()
    
    print(f"Dataset shape: {X.shape}")
    print(f"Positive cases: {y.sum()} ({y.mean()*100:.1f}%)")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=random_state,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['Negative', 'Positive'])
    
    print(f"\nAccuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(report)
    
    # Feature importance
    importance = dict(zip(FEATURE_COLUMNS, model.feature_importances_))
    print("\nFeature Importance:")
    for feat, imp in sorted(importance.items(), key=lambda x: x[1], reverse=True):
        print(f"  {feat}: {imp:.4f}")
    
    # Save model and scaler
    print(f"\nSaving model to {MODEL_PATH}...")
    joblib.dump({
        'model': model,
        'scaler': scaler,
        'feature_columns': FEATURE_COLUMNS,
        'accuracy': accuracy
    }, MODEL_PATH)
    
    print("Model saved successfully!")
    
    return {
        'accuracy': accuracy,
        'report': report,
        'feature_importance': importance
    }


def load_model():
    """
    Load the trained model from disk.
    
    Returns:
        dict: Contains 'model', 'scaler', 'feature_columns', 'accuracy'
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Please run train_model() first."
        )
    return joblib.load(MODEL_PATH)


def predict_risk(patient_data: dict) -> dict:
    """
    Predict heart disease risk for a patient.
    
    Args:
        patient_data: Dictionary with patient information:
            - age: Patient age (years)
            - gender: 0 = Female, 1 = Male
            - heart_rate: Heart rate (bpm)
            - systolic_bp: Systolic blood pressure (mmHg)
            - diastolic_bp: Diastolic blood pressure (mmHg)
            - blood_sugar: Blood sugar level (mg/dL)
            - ck_mb: CK-MB enzyme level
            - troponin: Troponin level
    
    Returns:
        dict: Prediction result with 'risk' and 'probability'
    """
    # Load saved model
    saved = load_model()
    model = saved['model']
    scaler = saved['scaler']
    
    # Prepare input features in correct order
    features = np.array([[
        patient_data['age'],
        patient_data['gender'],
        patient_data['heart_rate'],
        patient_data['systolic_bp'],
        patient_data['diastolic_bp'],
        patient_data['blood_sugar'],
        patient_data['ck_mb'],
        patient_data['troponin']
    ]])
    
    # Scale and predict
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    probabilities = model.predict_proba(features_scaled)[0]
    
    risk_probability = probabilities[1]  # Probability of positive (at risk)
    
    # Determine risk level
    if risk_probability < 0.3:
        risk_level = 'low'
    elif risk_probability < 0.6:
        risk_level = 'moderate'
    else:
        risk_level = 'high'
    
    return {
        'risk': 'positive' if prediction == 1 else 'negative',
        'risk_level': risk_level,
        'probability': round(risk_probability * 100, 2),
        'recommendation': _get_recommendation(risk_level)
    }


def _get_recommendation(risk_level: str) -> str:
    """Get health recommendation based on risk level."""
    recommendations = {
        'low': "Your heart health indicators look good. Continue maintaining a healthy lifestyle with regular exercise and a balanced diet.",
        'moderate': "Some indicators suggest moderate risk. Consider scheduling a check-up with your healthcare provider and monitoring your blood pressure regularly.",
        'high': "Your indicators suggest elevated heart disease risk. Please consult a cardiologist promptly for a comprehensive evaluation."
    }
    return recommendations.get(risk_level, "Please consult a healthcare professional.")


if __name__ == '__main__':
    # Train the model when run directly
    train_model()
