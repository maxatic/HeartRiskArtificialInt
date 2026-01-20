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
import shap

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'data' / 'Medicaldataset.csv'
MODEL_PATH = BASE_DIR / 'data' / 'heart_model.joblib'
SCALER_PATH = BASE_DIR / 'data' / 'scaler.joblib'

MODEL_PATH_REDUCED = BASE_DIR / 'data' / 'heart_model_reduced.joblib'
SCALER_PATH_REDUCED = BASE_DIR / 'data' / 'scaler_reduced.joblib'

# Feature columns in order
FEATURE_COLUMNS = [
    'Age', 'Gender', 'Heart rate', 
    'Systolic blood pressure', 'Diastolic blood pressure',
    'Blood sugar', 'CK-MB', 'Troponin'
]

# Reduced features (excluding 'CK-MB' and 'Troponin' which are at indices 6 and 7 in zero-indexed list)
FEATURE_COLUMNS_REDUCED = [
    'Age', 'Gender', 'Heart rate', 
    'Systolic blood pressure', 'Diastolic blood pressure',
    'Blood sugar'
]


def load_and_prepare_data(feature_columns):
    df = pd.read_csv(DATA_PATH)
    
    # Features (X) and target (y)
    X = df[feature_columns]
    y = (df['Result'] == 'positive').astype(int) # 1 for positive, 0 for negative
    
    return X, y


def train_model(feature_columns=FEATURE_COLUMNS, model_path=MODEL_PATH, scaler_path=SCALER_PATH, test_size=0.2, random_state=42):
    
    print(f"Training model with {len(feature_columns)} features: {feature_columns}")
    X, y = load_and_prepare_data(feature_columns)

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
    
    print(f"Accuracy (Random Forest): {accuracy:.4f}")
    
    # Save model AND scaler
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    print(f"Model saved to {model_path}")
    print(f"Scaler saved to {scaler_path}\n")





def load_model_and_scaler(model_path=MODEL_PATH, scaler_path=SCALER_PATH):
    if not model_path.exists() or not scaler_path.exists():
        raise FileNotFoundError(
            f"Model or scaler not found at {model_path} / {scaler_path}. "
            "Please run train_model() first."
        )
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return model, scaler


def predict_risk(data, use_reduced_model=False):
    """
    Predicts heart disease risk percentage for a single patient.
    
    Args:
        data (dict): Dictionary containing patient data with keys matching FEATURE_COLUMNS
        use_reduced_model (bool): If True, use the reduced model (6 features)
        
    Returns:
        float: Risk percentage (0-100)
    """
    if use_reduced_model:
        current_features = FEATURE_COLUMNS_REDUCED
        current_model_path = MODEL_PATH_REDUCED
        current_scaler_path = SCALER_PATH_REDUCED
    else:
        current_features = FEATURE_COLUMNS
        current_model_path = MODEL_PATH
        current_scaler_path = SCALER_PATH

    model, scaler = load_model_and_scaler(current_model_path, current_scaler_path)
    
    # Ensure data is in correct order
    input_data = []
    for col in current_features:
        if col not in data:
            raise ValueError(f"Missing required field: {col}")
        input_data.append(data[col])
    
    # Reshape for single sample
    input_array = np.array(input_data).reshape(1, -1)
    
    # Scale
    scaled_input = scaler.transform(input_array)
    
    # Predict probability of positive class (index 1)
    probability = model.predict_proba(scaled_input)[0][1]
    
    # Calculate SHAP values
    # We use TreeExplainer for Random Forest
    # Note: shap_values for classification often return a list [values_for_class_0, values_for_class_1]
    # We want class 1 (postive risk)
    # NOTE: SHAP TreeExplainer works well for Trees. 
    # If we switch to SVM globally, we'd need KernelExplainer. 
    # For now, we assume the saved model is still Random Forest.
    explainer = shap.TreeExplainer(model)
    shap_vals = explainer.shap_values(scaled_input)
    
    # Handle different SHAP output formats (sometimes array, sometimes list of arrays)
    if isinstance(shap_vals, list):
        shap_vals_class_1 = shap_vals[1][0]
    else:
        # If binary classification output is single array (less common for RF in shap but possible)
        if len(shap_vals.shape) == 3:
             shap_vals_class_1 = shap_vals[0, :, 1]
        else:
             shap_vals_class_1 = shap_vals[0]

    # Create a dictionary of Feature Name -> SHAP Value
    # This explains how much each feature contributed to the risk score calculation
    shap_dict = {}
    for i, col in enumerate(current_features):
        shap_dict[col] = float(shap_vals_class_1[i])

    return probability * 100, shap_dict

if __name__ == '__main__':
    # Standard training (saves models)
    print("Training Full Model (8 features)...")
    train_model(FEATURE_COLUMNS, MODEL_PATH, SCALER_PATH)
    
    print("Training Reduced Model (6 features - No CK-MB/Troponin)...")
    train_model(FEATURE_COLUMNS_REDUCED, MODEL_PATH_REDUCED, SCALER_PATH_REDUCED)


