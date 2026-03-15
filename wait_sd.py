import time
import requests

url = "http://127.0.0.1:7860/sdapi/v1/sd-models"
print("Waiting for SD.Next...")
for i in range(60):
    try:
        res = requests.get(url, timeout=2)
        if res.status_code == 200:
            print("Server is UP!")
            exit(0)
    except:
        pass
    time.sleep(5)
print("Timeout waiting for server")
exit(1)
