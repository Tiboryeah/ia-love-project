import os
import requests
import base64

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

character = {
    "id": "sweet-coco",
    "base_identity": "stunning beautiful blonde woman, perfect face, symmetrical features",
    "negative": "deformed, ugly, monster, horror, blurry, low quality, clothes, censored, text, watermark"
}

# Angulos y partes del cuerpo especificas para NSFW y anatomia perfecta
nsfw_prompts = [
    # Posiciones corporales complejas
    ("nsfw_pose_doggy", "photo of {identity} from behind, doggy style pose, completely naked, showing full ass, bright lighting, realistic skin, 8k"),
    ("nsfw_pose_missionary", "photo of {identity} lying on back, spread legs, missionary pose, looking up at camera, completely naked, realistic skin, explicit"),
    ("nsfw_pose_cowgirl", "photo of {identity} straddling, cowgirl pose, sitting on top, completely naked, visible breasts and completely naked body, looking at camera"),
    ("nsfw_pose_bent_over", "photo of {identity} bent over, looking back over shoulder, completely naked, showing back and ass, explicit, anatomically correct"),
    
    # Acercamientos anatomicos a partes clave
    ("nsfw_detail_breasts", "extreme close up of beautiful breasts, {identity}, completely naked torso, detailed nipples, realistic skin texture, soft lighting"),
    ("nsfw_detail_pussy", "extreme close up of perfect pussy, spread legs, {identity}, completely naked, explicit genitalia detail, anatomically correct, highly detailed, raw unedited photo"),
    ("nsfw_detail_ass", "close up of perfect round ass, {identity}, completely naked, from behind, realistic skin, high resolution"),
    ("nsfw_detail_thighs", "close up of thick thighs and hips, {identity}, completely naked, standing pose, smooth skin, 8k resolution"),
    
    # Pies y manos (Critico para que la IA no los deforme)
    ("nsfw_detail_feet", "close up of bare feet and toes, detailed soles, {identity} completely naked sitting on bed, highly detailed, perfect anatomy"),
    ("nsfw_detail_hands", "close up of beautiful hands with manicured fingers resting on naked body, {identity}, perfect hands anatomy, 5 fingers, realistic skin"),

    # Expresiones intimas
    ("nsfw_giving_bj", "close up of {identity} face looking up, mouth open, suggestive facial expression, ahegao, glowing skin, intimate lighting"),
    ("nsfw_afterglow", "portrait of {identity}, messy hair, sweaty skin, lying in bed completely naked, flushed face, intimate afterglow, highly detailed")
]

output_dir = f"lora_training/{character['id']}/images"
os.makedirs(output_dir, exist_ok=True)

print(f"Generating 12 NSFW specific training images for {character['id']}...")

for idx, (name, prompt_template) in enumerate(nsfw_prompts):
    full_prompt = prompt_template.format(identity=character["base_identity"])
    print(f"Generating {idx+1}/12: {name}...")
    
    payload = {
        "prompt": full_prompt + ", masterpiece, high quality, RAW photo",
        "negative_prompt": character["negative"],
        "steps": 25,
        "cfg_scale": 7.0,
        "width": 512,
        "height": 512,
        "sampler_name": "Euler a",
        "seed": 200 + idx,  # Semilla distinta a la fase 1
        "send_images": True,
    }
    
    try:
        response = requests.post(url, json=payload, timeout=600)
        if response.ok:
            data = response.json()
            img_data = base64.b64decode(data["images"][0])
            with open(f"{output_dir}/coco_{name}_{idx}.png", "wb") as f:
                f.write(img_data)
        else:
            print(f"Failed {name}: {response.text}")
    except Exception as e:
        print(f"Error generating {name}: {e}")

print("NSFW Dataset generation complete!")
