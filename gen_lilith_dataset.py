import os
import requests
import base64
import time

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

character = {
    "id": "lilith-goth",
    "base_identity": "stunningly beautiful 18 year old goth girl, extremely pale porcelain skin, exquisite facial symmetry, dark aesthetic makeup, heavy black eyeliner, black lipstick, (large perky breasts, natural cleavage:1.1), short waist, wide hips, thick thicc thighs, hourglass aesthetic, professional instagram photo",
    "negative": "mature, old, wrinkles, heavy cakey makeup, (aged face:1.2), sagging, deformed, ugly, monster, horror, blurry, low quality, worst quality, bad anatomy, bad hands, mutated hands, missing fingers, extra digit, mutated fingers, fused fingers, poorly drawn hands, asymmetrical breasts, uneven breasts, lumpy legs, mutated legs, deformed legs, ugly face, deformed face, poorly drawn face, bad face, deformed mask, cross-eyed, text, error, cropped, jpeg artifacts, watermark, cartoon, illustration, drawing, mutant, disfigured"
}

# 15 diferentes ángulos, expresiones y prendas para el LoRA
prompts = [
    ("front_close", "close up portrait photo of {identity}, looking directly at camera, soft smile, cinematic lighting"),
    ("side_profile", "side profile portrait of {identity}, looking away, neutral expression, soft lighting"),
    ("high_angle", "high angle selfie of {identity}, looking up at camera, cute expression, bedroom background"),
    ("low_angle", "low angle portrait of {identity}, looking down slightly, powerful expression, luxury hotel lobby"),
    ("laughing", "portrait of {identity}, laughing happily, wide smile with teeth, bright eyes, sunny park background"),
    ("serious", "portrait of {identity}, serious dramatic expression, piercing gaze, dark urban street"),
    ("seductive", "portrait of {identity}, seductive look, bedroom eyes, slightly parted lips, intimate lighting"),
    ("casual", "medium shot of {identity}, wearing casual black crop top and shorts, standing in a sunny room"),
    ("gym", "medium shot of {identity}, wearing tight black sports bra and yoga pants, gym mirror selfie"),
    ("elegant", "medium shot of {identity}, wearing elegant black evening lace dress, luxury gala background"),
    ("lingerie", "medium shot of {identity}, wearing delicate black lace lingerie, bedroom background, soft lighting"),
    ("bikini", "medium shot of {identity}, wearing tiny black bikini, pool side background, sunny day"),
    ("full_body_standing", "full body photo of {identity}, standing, wearing leather mini skirt and boots, street background"),
    ("full_body_walking", "full body photo of {identity}, walking, wearing black summer dress, outdoor promenade"),
    ("full_body_back", "full body photo from behind of {identity}, looking over shoulder at camera, showing large ass and hourglass figure")
]

output_dir = f"lora_training/{character['id']}/images"
os.makedirs(output_dir, exist_ok=True)

# 1. Esperar a que el servidor este listo
print("Esperando a que SD.Next este listo (esto puede tardar 1-2 mins)...")
while True:
    try:
        resp = requests.get("http://127.0.0.1:7860/sdapi/v1/options", timeout=5)
        if resp.ok:
            break
    except:
        pass
    time.sleep(5)

print("\n¡Servidor detectado! Iniciando TEST SET de 15 imagenes...")
print("Usando Hires. Fix (768x1152 final) para calidad Instagramer.")

for idx, (name, prompt_template) in enumerate(prompts):
    full_prompt = prompt_template.format(identity=character["base_identity"]) + ", masterpiece, best quality, ultra detailed, RAW photo"
    print(f"Generando {idx+1}/15: {name}...")
    
    payload = {
        "prompt": full_prompt,
        "negative_prompt": character["negative"],
        "steps": 35,
        "cfg_scale": 7.5,
        "width": 512,
        "height": 768,
        "enable_hr": True,
        "hr_scale": 1.5, # Total 768x1152
        "hr_upscaler": "R-ESRGAN 4x+",
        "denoising_strength": 0.5,
        "sampler_name": "DPM++ 2M",
        "seed": 1000 + idx, 
        "send_images": True,
        "alwayson_scripts": {
            "ADetailer": {
                "args": [
                    {
                        "ad_model": "face_yolov8n.pt",
                        "ad_prompt": "stunningly beautiful goth face, perfectly symmetrical, flawless pale skin, detailed eyes, intense gaze, (gorgeous:1.2)",
                        "ad_denoising_strength": 0.4,
                        "ad_clip_skip": 2,
                        "ad_confidence": 0.3
                    }
                ]
            }
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=900)
        if response.ok:
            data = response.json()
            if "images" in data and len(data["images"]) > 0:
                img_data = base64.b64decode(data["images"][0])
                filename = f"{character['id']}_{name}_{idx}.png"
                with open(f"{output_dir}/{filename}", "wb") as f:
                    f.write(img_data)
                print(f"  --> Guardada: {filename}")
            else:
                print(f"  [!] Error: No trajo imagen en JSON.")
        else:
            print(f"  [!] Error HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"  [!] Error fatal en {name}: {e}")

print("\n¡Set de prueba completado!")
print(f"Revisa la carpeta: {output_dir}")
