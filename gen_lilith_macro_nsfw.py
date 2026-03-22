import os
import requests
import base64

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

character = {
    "id": "lilith-goth",
    # Mantenemos las caracteristicas corporales (piel palida, estilo) para que la IA asocie textura/tono.
    "base_identity": "18 year old goth girl, extremely pale porcelain skin",
    "negative": "face, head, eyes, mouth, deformed, ugly, horror, blurry, low quality, worst quality, clothes, text, watermark, bad anatomy, mutant, disfigured, smooth crack, censored, fused anatomy"
}

# 3 acercamientos fotograficos extremos, sin pedir cara ni extremidades completas
macro_prompts = [
    ("macro_pussy_1", "solo, extreme macro close up photography of (perfect anatomical pink pussy:1.4), visible wet labia, completely naked body part, {identity}, highly detailed reproductive organ, realistic skin pores, cinematic lighting", 512, 512),
    ("macro_anus_2", "solo, extreme macro close up photography of (highly detailed gaping pink anus:1.5), spreading pale ass cheeks apart, completely visible wrinkled sphincter, {identity}, realistic skin texture, sharp focus", 512, 512),
    ("macro_feet_3", "solo, macro close up photography of beautiful bare slender feet, perfect 5 toes, dark pedicured toenails, {identity}, soft pale skin, detailed wrinkles on soles, resting on dark silk sheets", 512, 512)
]

output_dir = f"lora_training/{character['id']}/nsfw_candy/macro_details"
os.makedirs(output_dir, exist_ok=True)

print("\n=============================================")
print("Generando Dataset de Macro Anatomía (Tono Piel + Genitales puros)")
print("  - NOTA: IP-Adapter APAGADO para evitar rostros fantasma.")
print("=============================================\n")

for name, prompt_template, w, h in macro_prompts:
    full_prompt = prompt_template.format(identity=character["base_identity"]) + ", masterpiece, high quality, RAW photo, extremely detailed, best quality"
    
    print(f"\n[+] Iniciando Variante Macro de: {name}...")
    
    for i in range(2): # 2 Seeds por pose para que elijas la mas realista
        print(f"  -> Generando seed {i+1}/2...")
        
        payload = {
            "prompt": full_prompt,
            "negative_prompt": character["negative"],
            "steps": 40,
            "cfg_scale": 7.5,
            "width": w,
            "height": h,
            "enable_hr": True,
            "hr_scale": 1.5,
            "hr_upscaler": "R-ESRGAN 4x+",
            "denoising_strength": 0.5,
            "sampler_name": "DPM++ 2M",
            "seed": 5500 + i, 
            "send_images": True,
            "alwayson_scripts": {
                # Controladores APAGADOS para que pinte solo anatomía
                "ADetailer": {
                    "args": [
                        {
                            "ad_model": "Pussy on Pussy.safetensors",
                            "ad_prompt": "(highly detailed anatomical female genitalia, perfect pink labia, hyperrealistic nsfw:1.4)",
                            "ad_denoising_strength": 0.45,
                            "ad_clip_skip": 2,
                            "ad_confidence": 0.35
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
                    filename = f"{name}_seed_{i+1}.png"
                    with open(f"{output_dir}/{filename}", "wb") as f:
                        f.write(img_data)
                    print(f"     ✅ Guardada: {filename}")
                else:
                    print(f"     ❌ Error: No trajo imagen.")
            else:
                print(f"     ❌ Error HTTP {response.status_code}: {response.text}")
        except Exception as e:
            print(f"     ❌ Error fatal en {name} (var {i+1}): {e}")

print(f"\n¡Dataset Macro completado!\nRevisa tus 6 fotos base en:\n  {output_dir}")
