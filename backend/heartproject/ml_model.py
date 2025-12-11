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
    report = classification_report(y_test, y_pred, target_names=['Negative', 'Positive'])
    
    print(f"\nAccuracy: {accuracy:.4f}")
    

def load_model():
    
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. "
            "Please run train_model() first."
        )
    return joblib.load(MODEL_PATH)



if __name__ == '__main__':
    train_model()
