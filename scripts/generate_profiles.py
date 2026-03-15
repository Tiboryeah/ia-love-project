import requests
import json
import base64
import os
import time

AURA_DATABASE = [
    {
        "id": "fitness-vicky",
        "name": "Victoria 'Vicky' Fit",
        "desc": "hyperrealistic portrait of a stunning fitness girl, toned athletic body, sweat glistening on skin, messy blonde ponytail, wearing tight black gym gear, sports bra and leggings, intense gaze, gym background with cinematic lighting, depth of field, 8k resolution, shot on Sony A7R IV, highly detailed skin pores, realistic eyes, masterpiece"
    },
    {
        "id": "goth-darkangel",
        "name": "Darkangel666",
        "desc": "ultra realistic portrait of a mysterious goth girl, pale complexion, dramatic dark makeup, deep kohl eyeliner, black lipstick, long straight black hair with subtle purple highlights, wearing a gothic choker and black velvet outfit, moody atmospheric lighting, soft shadows, 8k, photorealistic, cinematic shot, highly detailed facial features"
    },
    {
        "id": "sweet-coco",
        "name": "Coco",
        "desc": "hyperrealistic photo of a beautiful blonde girl with platinum bob hair, huge expressive blue eyes, seductive innocent smile, wearing soft pink silk lingerie, choker, morning sunlight coming through window, warm cinematic glow, 8k, master photography, detailed skin texture, raw photo"
    },
    {
        "id": "morgana-dark",
        "name": "Morgana",
        "desc": "extraordinarily realistic portrait of a sophisticated mature woman, elegant brunette hair, piercing professional gaze, wearing a luxury designer power suit, high-end corporate office background, global lighting, photorealistic, 8k, sharp focus, masterpiece of professional photography"
    },
    {
        "id": "hana-chan",
        "name": "Hana-chan",
        "desc": "ultra realistic asian girl, cute features, anime-inspired makeup, dyed colorful hair, wearing an oversized hoodie and headset, gaming room with purple neon lights, bokeh background, hyper-detailed skin, 8k, real-life anime girl aesthetic"
    }
]

def generate_image(aura, retries=3):
    print(f"Generating for {aura['name']}...")
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    
    payload = {
        "prompt": f"raw photo, {aura['desc']}, high resolution, photorealistic, 8k",
        "negative_prompt": "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck",
        "steps": 6,
        "cfg_scale": 1.5,
        "width": 512,
        "height": 768,
        "sampler_name": "Euler a"
    }

    for attempt in range(retries):
        try:
            response = requests.post(url, json=payload, timeout=120)
            print(f"API Code: {response.status_code}")
            print(f"Preview: {response.text[:500]}")
            response.raise_for_status()
            data = response.json()
            
            if "images" in data and len(data["images"]) > 0:
                image_data = base64.b64decode(data["images"][0])
                file_path = f"public/profiles/{aura['id']}.png"
                with open(file_path, "wb") as f:
                    f.write(image_data)
                print(f"Successfully saved: {file_path}")
                return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {aura['id']}: {e}")
            time.sleep(5)
    
    return False

if __name__ == "__main__":
    if not os.path.exists("public/profiles"):
        os.makedirs("public/profiles")
    
    # Ensure SD API is responsive
    print("Waiting for SD API at http://127.0.0.1:7860...")
    while True:
        try:
            requests.get("http://127.0.0.1:7860/sdapi/v1/sd-models", timeout=5)
            print("API is UP!")
            break
        except:
            time.sleep(5)
            
    for aura in AURA_DATABASE:
        generate_image(aura)
    print("All profile generations finished.")
