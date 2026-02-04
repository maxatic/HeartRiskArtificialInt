import requests
import json

BASE_URL = 'http://127.0.0.1:8000'
EMAIL = 'debug_doctor_shell'
PASSWORD = 'testpass'

def get_token():
    url = f"{BASE_URL}/api/login/"
    data = {'username': EMAIL, 'password': PASSWORD}
    resp = requests.post(url, json=data)
    if resp.status_code == 200:
        return resp.json()['access']
    raise Exception(f"Login failed: {resp.text}")

def check_history(token):
    # Get a result ID first?
    # We can use the predict api to create one
    url = f"{BASE_URL}/api/predict-risk/"
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        "age": 50, "gender": "male", "heart_rate": 70, 
        "systolic_bp": 120, "diastolic_bp": 80, "blood_sugar": 100,
        "ck_mb": 2.5, "troponin": 0.02
    }
    resp = requests.post(url, json=data, headers=headers)
    record_id = resp.json().get('record_id')
    print(f"Created record {record_id}")
    
    # Get detail
    url = f"{BASE_URL}/api/result/{record_id}/"
    resp = requests.get(url, headers=headers)
    history = resp.json().get('history', [])
    
    if len(history) > 0:
        item = history[0]
        if 'id' in item:
            print(f"SUCCESS: History item has ID: {item.get('id')}")
        else:
            print(f"FAILURE: History item missing ID. Keys: {item.keys()}")
    else:
        print("WARNING: No history found")

if __name__ == "__main__":
    try:
        token = get_token()
        check_history(token)
    except Exception as e:
        print(e)
