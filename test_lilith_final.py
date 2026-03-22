import requests
import base64
import os

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

payload = {
    "prompt": "<lora:lilith_goth_v1_5060ti:0.8>, portrait photography, lilith-goth, stunningly beautiful 18 year old youthful gothic girl, babyface, black lipstick, pale skin, looking at camera, cinematic lighting, masterpiece",
    "negative_prompt": "ugly, deformed, old, wrinkles, cgi, render, 3d, (extra fingers:1.2)",
    "steps": 20,
    "cfg_scale": 5.0,
    "width": 512,
    "height": 512,
    "sampler_name": "Euler a",
    "send_images": True,
    "save_images": True,
    "alwayson_scripts": {
        "ADetailer": {
            "args": [
                {
                    "ad_model": "face_yolov8n.pt",
                    "ad_prompt": "stunningly beautiful cute face, perfect eyes",
                    "ad_denoising_strength": 0.35
                }
            ]
        }
    }
}

print("Generando imagen de test de Lilith con su nuevo LoRA...")
response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    img_data = base64.b64decode(data['images'][0])
    output_path = r"e:\IALove\test_lilith_lora_result.png"
    with open(output_path, "wb") as f:
        f.write(img_data)
    print(f"¡Éxito! Imagen guardada en: {output_path}")
else:
    print(f"Error: {response.status_code} - {response.text}")
