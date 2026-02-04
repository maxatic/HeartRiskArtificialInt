import requests
import json

BASE_URL = 'http://127.0.0.1:8000'
EMAIL = 'debug_doctor_shell' # Existing user from previous step
PASSWORD = 'testpass'

def get_token():
    url = f"{BASE_URL}/api/login/"
    data = {'username': EMAIL, 'password': PASSWORD}
    resp = requests.post(url, json=data)
    if resp.status_code == 200:
        return resp.json()['access']
    raise Exception(f"Login failed: {resp.text}")

def test_partial_prediction(token):
    print("\n--- Testing Partial Prediction (6 fields) ---")
    url = f"{BASE_URL}/api/predict-risk/"
    headers = {'Authorization': f'Bearer {token}'}
    # Missing CK-MB and Troponin
    data = {
        "age": 50,
        "gender": "male",
        "heart_rate": 70,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "blood_sugar": 100
        # ck_mb, troponin omitted
    }
    
    resp = requests.post(url, json=data, headers=headers)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        result = resp.json()
        print(f"Is Partial: {result.get('is_partial_assessment')}")
        if result.get('is_partial_assessment') is True:
            print("SUCCESS: Identified as partial assessment")
        else:
            print("FAILURE: Not identified as partial")
    else:
        print(f"Error: {resp.text}")

def test_full_prediction(token):
    print("\n--- Testing Full Prediction (8 fields) ---")
    url = f"{BASE_URL}/api/predict-risk/"
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        "age": 50,
        "gender": "male",
        "heart_rate": 70,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "blood_sugar": 100,
        "ck_mb": 2.5,
        "troponin": 0.02
    }
    
    resp = requests.post(url, json=data, headers=headers)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        result = resp.json()
        print(f"Is Partial: {result.get('is_partial_assessment')}")
        if not result.get('is_partial_assessment'):
             print("SUCCESS: Identified as full assessment")
        else:
             print("FAILURE: Identified as partial incorrectly")
    else:
        print(f"Error: {resp.text}")

if __name__ == "__main__":
    try:
        token = get_token()
        test_partial_prediction(token)
        test_full_prediction(token)
    except Exception as e:
        print(f"Test Failed: {e}")
