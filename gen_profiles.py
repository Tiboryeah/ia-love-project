import requests
import base64
import os

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

CHARACTERS = [
    {
        "id": "sweet-coco",
        "seed": 1,
        "prompt": "portrait of a stunningly beautiful blonde woman, perfect face, symmetrical features, blonde hair bob, cinematic lighting, high quality, masterpiece"
    },
    {
        "id": "fitness-vicky",
        "seed": 2,
        "prompt": "portrait of a stunningly beautiful athletic woman, perfect face, symmetrical features, honey blonde ponytail, fitness model, cinematic lighting, high quality, masterpiece"
    },
    {
        "id": "goth-darkangel",
        "seed": 3,
        "prompt": "portrait of a stunningly beautiful goth woman, perfect face, symmetrical features, long black hair, pale skin, gothic jewelry, cinematic lighting, high quality, masterpiece"
    },
    {
        "id": "morgana-dark",
        "seed": 4,
        "prompt": "portrait of a stunningly beautiful 35 year old woman, perfect face, symmetrical features, elegant dark hair, sophisticated look, cinematic lighting, high quality, masterpiece"
    },
    {
        "id": "hana-chan",
        "seed": 5,
        "prompt": "portrait of a stunningly beautiful young asian woman, perfect face, symmetrical features, pink hair, cute aesthetic, cinematic lighting, high quality, masterpiece"
    }
]

NEGATIVE = "deformed, ugly, monster, horror, blurry, low quality"

output_dir = "public/profiles"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for char in CHARACTERS:
    print(f"Generating Goddess profile for {char['id']}...")
    
    payload = {
        "prompt": char["prompt"],
        "negative_prompt": NEGATIVE,
        "steps": 20,
        "cfg_scale": 7.0,
        "width": 512,
        "height": 512,
        "sampler_name": "Euler a",
        "seed": char["seed"],
        "send_images": True,
    }
    
    try:
        response = requests.post(url, json=payload, timeout=600)
        if response.ok:
            data = response.json()
            img_data = base64.b64decode(data["images"][0])
            with open(f"{output_dir}/{char['id']}.png", "wb") as f:
                f.write(img_data)
            print(f"Saved goddess {char['id']}.png")
        else:
            print(f"Failed {char['id']}: {response.text}")
    except Exception as e:
        print(f"Error generating {char['id']}: {e}")

print("Done generating Goddess profiles.")
