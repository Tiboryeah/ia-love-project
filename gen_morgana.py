import os
import requests
import base64

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

character = {
    "id": "morgana-goth",
    "base_identity": "stunningly beautiful 20 year old gothic woman, extremely pale skin, huge breasts, cleavage, long black hair, heavy dark eyeliner, black lips, instagram model, perfect face, symmetrical features",
    "negative": "deformed, ugly, monster, horror, blurry, low quality, mirror, reflection, water reflection"
}

# 15 diferentes ángulos, expresiones y prendas para el LoRA
prompts = [
    # Ángulos de rostro
    ("front_close", "close up portrait photo of {identity}, looking directly at camera, soft smile"),
    ("side_profile", "side profile portrait of {identity}, looking away, neutral expression"),
    ("high_angle", "high angle selfie of {identity}, looking up at camera, cute expression"),
    ("low_angle", "low angle portrait of {identity}, looking down slightly, powerful expression"),
    
    # Expresiones
    ("laughing", "portrait of {identity}, laughing happily, wide smile with teeth, bright eyes"),
    ("serious", "portrait of {identity}, serious dramatic expression, piercing gaze"),
    ("seductive", "portrait of {identity}, seductive look, bedroom eyes, slightly parted lips"),
    
    # Medio cuerpo / Ropa diferente
    ("casual", "medium shot of {identity}, wearing casual gothic t-shirt, standing in a sunny room"),
    ("gym", "medium shot of {identity}, wearing tight black sports bra and shorts, gym wall background, selfie"),
    ("elegant", "medium shot of {identity}, wearing elegant black evening dress, luxury background"),
    ("lingerie", "medium shot of {identity}, wearing delicate black lace lingerie, bedroom background"),
    ("bikini", "medium shot of {identity}, wearing tiny black bikini, beach background, sunny day"),
    
    # Cuerpo entero
    ("full_body_jeans", "full body photo of {identity}, standing, wearing black ripped jeans and crop top"),
    ("full_body_dress", "full body photo of {identity}, walking, wearing black gothic dress, outdoor street"),
    ("full_body_back", "full body photo from behind of {identity}, looking over shoulder at camera")
]

output_dir = f"lora_training/{character['id']}/images"
os.makedirs(output_dir, exist_ok=True)

print(f"Generating 15 training images for {character['id']}...")

for idx, (name, prompt_template) in enumerate(prompts):
    full_prompt = prompt_template.format(identity=character["base_identity"])
    print(f"Generating {idx+1}/15: {name}...")
    
    payload = {
        "prompt": full_prompt + ", masterpiece, high quality, extremely detailed",
        "negative_prompt": character["negative"],
        "steps": 30,
        "cfg_scale": 7.5,
        "width": 768,
        "height": 768,
        "sampler_name": "DPM++ 2M Karras",
        "seed": 300 + idx, 
        "send_images": True,
    }
    
    try:
        response = requests.post(url, json=payload, timeout=600)
        if response.ok:
            data = response.json()
            img_data = base64.b64decode(data["images"][0])
            with open(f"{output_dir}/{character['id']}_{name}_{idx}.png", "wb") as f:
                f.write(img_data)
        else:
            print(f"Failed {name}: {response.text}")
    except Exception as e:
        print(f"Error generating {name}: {e}")

print("Dataset generation complete!")
