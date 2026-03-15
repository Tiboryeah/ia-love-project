import requests
import base64

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

payload = {
    "prompt": "portrait of a stunningly beautiful blonde woman, perfect face, symmetrical features, cinematic lighting, high quality, masterpiece",
    "negative_prompt": "deformed, ugly, monster, horror, blurry, low quality",
    "steps": 20,
    "cfg_scale": 7.0,
    "width": 512,
    "height": 512,
    "sampler_name": "Euler a",
    "seed": 1,
}

print("Generating Pure Beauty test...")
response = requests.post(url, json=payload, timeout=300)
if response.ok:
    data = response.json()
    img_data = base64.b64decode(data["images"][0])
    with open("pure_beauty.png", "wb") as f:
        f.write(img_data)
    print("Saved pure_beauty.png")
else:
    print(f"Failed: {response.text}")
