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
SCALER_PATH = BASE_DIR / 'data' / 'scaler.joblib'

# Feature columns in order
FEATURE_COLUMNS = [
    'Age', 'Gender', 'Heart rate', 
    'Systolic blood pressure', 'Diastolic blood pressure',
    'Blood sugar', 'CK-MB', 'Troponin'
]


def load_and_prepare_data():
    df = pd.read_csv(DATA_PATH)
    
    # Features (X) and target (y)
    X = df[FEATURE_COLUMNS]
    y = (df['Result'] == 'positive').astype(int) # 1 for positive, 0 for negative
    
    return X, y


def train_model(test_size=0.2, random_state=42):
    
    X, y = load_and_prepare_data()

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
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
    
    print(f"\nAccuracy: {accuracy:.4f}")
    
    # Save model AND scaler
    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print(f"Scaler saved to {SCALER_PATH}")
    

def load_model_and_scaler():
    if not MODEL_PATH.exists() or not SCALER_PATH.exists():
        raise FileNotFoundError(
            "Model or scaler not found. "
            "Please run train_model() first."
        )
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler


def predict_risk(data):
    """
    Predicts heart disease risk percentage for a single patient.
    
    Args:
        data (dict): Dictionary containing patient data with keys matching FEATURE_COLUMNS
        
    Returns:
        float: Risk percentage (0-100)
    """
    model, scaler = load_model_and_scaler()
    
    # Ensure data is in correct order
    input_data = []
    for col in FEATURE_COLUMNS:
        if col not in data:
            raise ValueError(f"Missing required field: {col}")
        input_data.append(data[col])
    
    # Reshape for single sample
    input_array = np.array(input_data).reshape(1, -1)
    
    # Scale
    scaled_input = scaler.transform(input_array)
    
    # Predict probability of positive class (index 1)
    probability = model.predict_proba(scaled_input)[0][1]
    
    return probability * 100

if __name__ == '__main__':
    train_model()
