import requests
import json

try:
    print("Checking models...")
    response = requests.get("http://127.0.0.1:7860/sdapi/v1/sd-models", timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Models: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
