# utils.py or top of views.py
import requests

def get_jwt_token(username, password):
    url = "http://127.0.0.1:8000/api/token/"  # Adjust if hosted elsewhere
    data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()  # returns {'access': '...', 'refresh': '...'}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}