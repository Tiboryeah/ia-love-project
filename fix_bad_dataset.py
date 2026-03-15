import os
import requests
import base64
import time

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

character = {
    "id": "sweet-coco",
    "base_identity": "stunning beautiful blonde woman, perfect face, symmetrical features",
    "negative": "deformed, ugly, monster, horror, blurry, low quality, mirror, reflection, water reflection"
}

output_dir = f"lora_training/{character['id']}/images"

# Esperar a que inicie el servidor
for _ in range(30):
    try:
        requests.get("http://127.0.0.1:7860/sdapi/v1/sd-models", timeout=2)
        break
    except:
        time.sleep(5)

fixes = [
    {
        "filename": "coco_gym_8.png",
        "prompt": "medium shot of {identity}, wearing tight sports bra and shorts, plain gym wall background, selfie, soft lighting",
        "negative": character["negative"] + ", mirror, glass, double, clone, text",
        "seed": 9123
    },
    {
        "filename": "coco_elegant_9.png",
        "prompt": "medium shot of {identity}, wearing elegant black evening dress, standing in a plain elegant room, soft cinematic lighting",
        "negative": character["negative"] + ", mirror, glass, reflective surface, clone",
        "seed": 9124
    },
    {
        "filename": "coco_nsfw_detail_feet_8.png",
        "prompt": "close up of bare feet, 5 toes, detailed soles, {identity} completely naked sitting on bed, highly detailed, perfect anatomy",
        "negative": character["negative"] + ", extra toes, missing toes, deformed foot, six toes, deformed joints, long toes",
        "seed": 9126
    }
]

print("Regenerating 3 flawed images...")

for item in fixes:
    full_prompt = item["prompt"].format(identity=character["base_identity"])
    print(f"Fixing {item['filename']}...")
    
    payload = {
        "prompt": full_prompt + ", masterpiece, high quality",
        "negative_prompt": item["negative"],
        "steps": 25,
        "cfg_scale": 7.0,
        "width": 512,
        "height": 512,
        "sampler_name": "Euler a",
        "seed": item["seed"],
        "send_images": True,
    }
    
    try:
        response = requests.post(url, json=payload, timeout=600)
        if response.ok:
            data = response.json()
            img_data = base64.b64decode(data["images"][0])
            with open(os.path.join(output_dir, item['filename']), "wb") as f:
                f.write(img_data)
            print(f"-> Overwritten {item['filename']}")
        else:
            print(f"Failed {item['filename']}: {response.text}")
    except Exception as e:
        print(f"Error {item['filename']}: {e}")

print("Fix complete!")
