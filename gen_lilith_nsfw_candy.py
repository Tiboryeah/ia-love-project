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
    # Mantenemos la descripcion del cuerpo, pero IP-Adapter hará el trabajo del rostro
    "base_identity": "stunningly beautiful 18 year old goth girl, extremely pale porcelain skin, dark aesthetic makeup, heavy black eyeliner, black lipstick, (large perky breasts, natural cleavage:1.1), short waist, wide hips, thick thicc thighs, hourglass aesthetic, professional instagram photo",
    "negative": "mature, old, wrinkles, heavy cakey makeup, sagging, deformed, ugly, monster, horror, blurry, low quality, worst quality, bad anatomy, bad hands, mutated hands, missing fingers, extra digit, mutated fingers, fused fingers, poorly drawn hands, asymmetrical breasts, uneven breasts, lumpy legs, mutated legs, deformed legs, ugly face, deformed face, poorly drawn face, bad face, deformed mask, cross-eyed, text, error, cropped, jpeg artifacts, watermark, cartoon, illustration, drawing, mutant, disfigured"
}

nsfw_prompts = [
    ("nsfw_pose_doggy", "photo of {identity} from behind, doggy style pose, completely naked, showing full ass, bright lighting, realistic skin, 8k"),
    ("nsfw_pose_missionary", "photo of {identity} lying on back, spread legs, missionary pose, looking up at camera, completely naked, realistic skin, explicit"),
    ("nsfw_pose_cowgirl", "photo of {identity} straddling, cowgirl pose, sitting on top, completely naked, visible huge breasts and naked body, looking at camera"),
    ("nsfw_pose_bent_over", "photo of {identity} bent over, looking back over shoulder, completely naked, showing back and ass, explicit, anatomically correct"),
    ("nsfw_detail_breasts", "close up of beautiful breasts, {identity}, completely naked torso, detailed nipples, realistic skin texture, soft lighting"),
    ("nsfw_detail_pussy", "extreme close up of perfect pussy, spread legs, {identity}, completely naked, explicit genitalia detail, anatomically correct, highly detailed, raw unedited photo"),
    ("nsfw_detail_ass", "close up of perfect round ass, {identity}, completely naked, from behind, realistic skin, high resolution"),
    ("nsfw_detail_thighs", "close up of thick thighs and hips, {identity}, completely naked, standing pose, smooth skin, 8k resolution"),
    ("nsfw_giving_bj", "close up of {identity} face looking up, mouth open, suggestive facial expression, ahegao, glowing skin, intimate lighting"),
    ("nsfw_afterglow", "portrait of {identity}, messy hair, sweaty skin, lying in bed completely naked, flushed face, intimate afterglow, highly detailed")
]

output_dir = f"lora_training/{character['id']}/nsfw_candy"
os.makedirs(output_dir, exist_ok=True)

print("\n=============================================")
print("Iniciando generación NSFW Candy-Perfect (IP-Adapter FaceID)")
print("=============================================\n")

for idx, (name, prompt_template) in enumerate(nsfw_prompts):
    full_prompt = prompt_template.format(identity=character["base_identity"]) + ", masterpiece, high quality, RAW photo, extremely detailed, best quality"
    print(f"Generando {idx+1}/{len(nsfw_prompts)}: {name}...")
    
    payload = {
        "prompt": full_prompt,
        "negative_prompt": character["negative"],
        "steps": 35,
        "cfg_scale": 7.0,
        "width": 512,
        "height": 768,
        "enable_hr": True,
        "hr_scale": 1.5,
        "hr_upscaler": "R-ESRGAN 4x+",
        "denoising_strength": 0.5,
        "sampler_name": "DPM++ 2M",
        "seed": 2000 + idx, 
        "send_images": True,
        "alwayson_scripts": {
            "IP Adapters": {
                "args": [
                    1, False, # units, unload
                    "ip-adapter-plus-face_sd15", "None", "None", "None", # models
                    0.8, 0.5, 0.5, 0.5, # weights
                    [ref_b64], [], [], [], # images
                    True, False, False, False, # crop
                    0.0, 0.0, 0.0, 0.0, # start steps
                    1.0, 1.0, 1.0, 1.0, # end steps
                    [], [], [], [], # masks
                    False, "" # layers options
                ]
            },
            "ADetailer": {
                "args": [
                    {
                        "ad_model": "face_yolov8n.pt",
                        "ad_prompt": "stunningly beautiful goth face, perfectly symmetrical, flawless pale skin, detailed eyes, intense gaze",
                        "ad_denoising_strength": 0.35, # Ligeramente mas bajo para no distorsionar demasiado el FaceID
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
                print(f"  ✅ Guardada: {filename}")
            else:
                print(f"  ❌ Error: No trajo imagen en JSON.")
        else:
            print(f"  ❌ Error HTTP {response.status_code}: {response.text}")
    except Exception as e:
        print(f"  ❌ Error fatal en {name}: {e}")

print(f"\n¡Dataset Candy AI completado!\nRevisa la carpeta: {output_dir}")
