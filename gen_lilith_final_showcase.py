import requests
import base64
import os
import time

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
output_dir = r"e:\IALove\showcase_lilith"
os.makedirs(output_dir, exist_ok=True)

# Common params
base_payload = {
    "steps": 25,
    "cfg_scale": 6.0,
    "width": 512,
    "height": 512,
    "sampler_name": "Euler a",
    "send_images": True,
    "save_images": True
}

# ------------------------------------------------------------
# SFW POSES (5)
# ------------------------------------------------------------
sfw_prompts = [
    "candid selfie photo, <lora:lilith_goth_v1_5060ti:0.8>, lilith-goth, stunningly beautiful 18 year old youthful gothic girl, babyface, black lipstick, pale skin, casual bedroom background",
    "cinematic lighting, <lora:lilith_goth_v1_5060ti:0.8>, lilith-goth, (full body photography:1.1), stunning goth girl, standing in a library, wearing short black dress, combat boots, masterpiece",
    "close up portrait, <lora:lilith_goth_v1_5060ti:0.8>, lilith-goth, mesmerizing look, youthful soft features, very pale porcelain skin, dark aesthetic makeup, home lighting",
    "outdoor photography, <lora:lilith_goth_v1_5060ti:0.8>, lilith-goth, stunning goth girl walking in a park, soft natural sunlight, (extremely large massive breasts:1.1), youthful babyface",
    "candid shot, <lora:lilith_goth_v1_5060ti:0.8>, lilith-goth, goth girl sitting at a cafe table, checking smartphone, highly detailed skin textures, masterpiece"
]

# ------------------------------------------------------------
# NSFW POSES (5)
# ------------------------------------------------------------
nsfw_prompts = [
    "<lora:lilith_goth_v1_5060ti:0.8>, lilith-goth, extremely explicit, (completely naked:1.3), sedentary pose on bed, showing (extremely large massive symmetrical breasts:1.2) and vulva, pussy, raw skin textures, intimate lighting",
    "<lora:lilith_goth_v1_5060ti:0.8>, lilith-goth, (doggy style pose:1.4), (completely naked:1.3), looking back at camera over shoulder, from behind, showing large ass and detailed ano, pussy, intimate intimate photography",
    "<lora:lilith_goth_v1_5060ti:0.8>, lilith-goth, (missionary pose:1.4), (completely naked:1.3), lying on back, legs spread wide, showing detailed vulva and pussy, seductive face expression, masterpiece",
    "<lora:lilith_goth_v1_5060ti:0.8>, lilith-goth, (close up on vulva and pussy:1.4), spreading legs, raw skin details, pink skin, intimate photography, masterpiece",
    "<lora:lilith_goth_v1_5060ti:0.8>, lilith-goth, (standing nude:1.1), facing camera, (completely naked:1.3), showing full figure, (large massive heavy breasts:1.2), seductive goth look, masterpiece"
]

def generate(idx, prompt, is_nsfw=False):
    payload = base_payload.copy()
    payload["prompt"] = prompt
    payload["negative_prompt"] = "ugly, deformed, old, wrinkles, cgi, render, 3d, (extra fingers:1.2), (malformed fingers:1.2)"
    
    # ADetailer Configuration
    # Face for everyone
    ad_args = [{
        "ad_model": "face_yolov8n.pt",
        "ad_prompt": "stunningly beautiful cute youthful face, detailed eyes, perfect makeup",
        "ad_denoising_strength": 0.4
    }]
    
    # Genitals for NSFW only
    if is_nsfw:
        ad_args.append({
            "ad_model": "Pussy on Pussy.safetensors",
            "ad_prompt": "extremely detailed pussy, vulva, wet skin textures, raw skin detail, pink pussy, masterpieces",
            "ad_denoising_strength": 0.5
        })
    
    payload["alwayson_scripts"] = {"ADetailer": {"args": ad_args}}
    
    prefix = "nsfw" if is_nsfw else "sfw"
    filename = f"{prefix}_{idx}.png"
    
    print(f"[*] Generando {filename}...")
    try:
        response = requests.post(url, json=payload, timeout=120)
        if response.status_code == 200:
            data = response.json()
            img_data = base64.b64decode(data['images'][0])
            with open(os.path.join(output_dir, filename), "wb") as f:
                f.write(img_data)
            print(f"[+] {filename} Guardada.")
        else:
            print(f"[-] Error en {filename}: {response.status_code}")
    except Exception as e:
        print(f"[-] Error fatal: {e}")

# Main Execution Loop
print("=== SESION DE MUESTRA PARA LILITH-GOTH ===")
for i, p in enumerate(sfw_prompts):
    generate(i+1, p, is_nsfw=False)

for i, p in enumerate(nsfw_prompts):
    generate(i+1, p, is_nsfw=True)

print(f"\n¡SESION COMPLETADA! Revisa tus 10 fotos en: {output_dir}")
