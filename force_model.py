import requests
import time

url = "http://127.0.0.1:7860/sdapi/v1/options"
payload = {"sd_model_checkpoint": "Realistic_Vision_V6.0 [fe7578cb5e]"}

for i in range(10):
    try:
        print(f"Attempt {i+1}: Setting model...")
        response = requests.post(url, json=payload, timeout=60)
        print(f"Response: {response.text}")
        if response.status_code == 200:
            print("Successfully requested model change.")
            break
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(10)
