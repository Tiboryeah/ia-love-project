import os
import requests
import base64

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

character = {
    "id": "raven-egirl",
    "base_identity": "stunningly beautiful 20 year old e-girl goth woman, very pale skin, black hair with bangs and twin braids, heavy e-girl makeup, thick dark winged eyeliner, black choker, black and white striped crop top, intensely ripped black tights, slim fit body, perfect cute face, symmetrical features, social media influencer, instagram model",
    "negative": "deformed, ugly, monster, horror, blurry, lowres, low quality, worst quality, bad anatomy, bad proportions, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, ugly, bad proportions, gross proportions, text, watermark"
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
    ("serious", "portrait of {identity}, serious dramatic e-girl expression, piercing gaze"),
    ("seductive", "portrait of {identity}, seductive look, bedroom eyes, slightly parted lips"),
    
    # Medio cuerpo / Ropa diferente (sobrescribimos la ropa para variar, pero mantenemos su estilo)
    ("casual", "medium shot of {identity}, wearing casual oversized black band t-shirt, standing in an aesthetic led-lit bedroom"),
    ("gym", "medium shot of {identity}, wearing tight black sports bra and yoga pants, gym mirror background, mirror selfie"),
    ("elegant", "medium shot of {identity}, wearing elegant black velvet gothic dress, luxury background"),
    ("lingerie", "medium shot of {identity}, wearing delicate black lace lingerie and choker, bedroom background"),
    ("bikini", "medium shot of {identity}, wearing tiny black bikini with chains, beach background, sunset"),
    
    # Cuerpo entero
    ("full_body_jeans", "full body photo of {identity}, standing, wearing black distressed jeans and cropped top, street background"),
    ("full_body_dress", "full body photo of {identity}, walking, wearing black gothic dress with boots, outdoor street"),
    ("full_body_back", "full body photo from behind of {identity}, looking over shoulder at camera")
]

output_dir = f"lora_training/{character['id']}/images"
os.makedirs(output_dir, exist_ok=True)

print(f"Generating 15 high-quality training images for {character['id']}...")

for idx, (name, prompt_template) in enumerate(prompts):
    full_prompt = prompt_template.format(identity=character["base_identity"])
    print(f"Generating {idx+1}/15: {name}...")
    
    payload = {
        "prompt": full_prompt + ", masterpiece, best quality, highly detailed, ultra-realistic, 8k resolution, raw photo, film grain",
        "negative_prompt": character["negative"],
        "steps": 35,
        "cfg_scale": 7.0,
        "width": 512,
        "height": 512, # Imagenes verticales para redes sociales
        "sampler_name": "Euler a", # Mejor compatibilidad con AMD
        "seed": 500 + idx, 
        "send_images": True
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
