import os
import requests
import base64
import time

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
reference_img_path = r"e:\IALove\references\lilith_face.png"

print("Cargando la Foto Maestra de Lilith...")
with open(reference_img_path, "rb") as f:
    ref_b64 = base64.b64encode(f.read()).decode("utf-8")

character = {
    "id": "lilith-goth",
    "base_identity": "stunningly beautiful 18 year old goth girl, extremely pale porcelain skin, dark aesthetic makeup, heavy black eyeliner, black lipstick, (large perky breasts, natural cleavage:1.1), short waist, wide hips, thick thicc thighs, hourglass aesthetic, professional instagram photo",
    "negative": "mature, old, wrinkles, heavy cakey makeup, sagging, deformed, ugly, monster, horror, blurry, low quality, worst quality, bad anatomy, bad hands, mutated hands, missing fingers, extra digit, fused fingers, asymmetrical breasts, uneven breasts, lumpy legs, deformed legs, ugly face, deformed face, poorly drawn face, bad face, cross-eyed, text, error, cropped, jpeg artifacts, mutant, disfigured, fused anatomy, completely censored"
}

# Volviendo a las plantillas que ya habían demostrado funcionar sin deformar la anatomia
nsfw_prompts = [
    ("reparacion_missionary", "photo of {identity} lying on back, spread legs, missionary pose, looking up at camera, completely naked, realistic skin, explicit, anatomically correct", 512, 768),
    ("reparacion_detail_ass", "close up of perfect round ass, {identity}, completely naked, from behind, realistic skin, high resolution, soft lighting", 512, 768),
]

output_dir = f"lora_training/{character['id']}/nsfw_candy/reparaciones"
os.makedirs(output_dir, exist_ok=True)

print("\n=============================================")
print("Generando Fuerza Bruta (Plantillas Limpias y Estables)")
print("=============================================\n")

for name, prompt_template, w, h in nsfw_prompts:
    full_prompt = prompt_template.format(identity=character["base_identity"]) + ", masterpiece, high quality, RAW photo, best quality"
    
    print(f"\n[+] Iniciando 5 variaciones para: {name}...")
    
    for i in range(5):
        print(f"  -> Generando seed variante {i+1}/5...")
        
        payload = {
            "prompt": full_prompt,
            "negative_prompt": "deformed, ugly, monster, horror, blurry, low quality, clothes, text, watermark, bad anatomy, missing fingers, extra digit, mutant",
            "steps": 35,
            "cfg_scale": 7.0, # Volviendo a 7.0 (estable)
            "width": w,
            "height": h,
            "enable_hr": True,
            "hr_scale": 1.5,
            "hr_upscaler": "R-ESRGAN 4x+",
            "denoising_strength": 0.5,
            "sampler_name": "DPM++ 2M",
            "seed": 7700 + i, 
            "send_images": True,
            "alwayson_scripts": {
                "IP Adapters": {
                    "args": [
                        1, False,
                        "ip-adapter-plus-face_sd15", "None", "None", "None",
                        0.8, 0.5, 0.5, 0.5,
                        [ref_b64], [], [], [],
                        True, False, False, False,
                        0.0, 0.0, 0.0, 0.0,
                        1.0, 1.0, 1.0, 1.0,
                        [], [], [], [],
                        False, ""
                    ]
                },
                "ADetailer": {
                    "args": [
                        {
                            "ad_model": "face_yolov8n.pt",
                            "ad_prompt": "stunningly beautiful goth face, perfectly symmetrical",
                            "ad_denoising_strength": 0.35,
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
                    filename = f"var_{i+1}_{name}.png"
                    with open(f"{output_dir}/{filename}", "wb") as f:
                        f.write(img_data)
                    print(f"     ✅ Guardada: {filename}")
                else:
                    print(f"     ❌ Error: No trajo imagen en JSON.")
            else:
                print(f"     ❌ Error HTTP {response.status_code}: {response.text}")
        except Exception as e:
            print(f"     ❌ Error fatal en {name} (var {i+1}): {e}")

print(f"\n¡Variaciones (Reparaciones) completadas!\nRevisa tus 10 opciones nuevas en la carpeta:\n  {output_dir}")
