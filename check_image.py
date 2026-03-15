import requests
import json
import base64
import numpy as np
from PIL import Image
import io

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
payload = {"prompt": "dog", "steps": 5, "width": 512, "height": 512}
r = requests.post(url, json=payload, timeout=120)
data = r.json()

if data.get("images"):
    img_bytes = base64.b64decode(data["images"][0])
    img = Image.open(io.BytesIO(img_bytes))
    arr = np.array(img)
    print(f"Image stats - Min:{arr.min()} Max:{arr.max()} Mean:{arr.mean():.1f}")
    print(f"Non-zero pixels: {(arr > 5).sum()}")
    
    info_str = data.get("info", "{}")
    info = json.loads(info_str) if isinstance(info_str, str) else info_str
    print(f"Seed: {info.get('seed', '?')}")
