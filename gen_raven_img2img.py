import os
import requests
import base64
from io import BytesIO
from PIL import Image

url = "http://127.0.0.1:7860/sdapi/v1/img2img"

character = {
    "id": "raven-egirl",
    "base_identity": "stunningly beautiful 20 year old e-girl goth woman, very pale skin, black hair with bangs, heavy e-girl makeup, thick dark winged eyeliner, black choker, intensely ripped black tights, slim fit body, perfect cute face, symmetrical features, social media influencer, instagram model",
    "negative": "deformed, ugly, monster, horror, blurry, lowres, low quality, worst quality, bad anatomy, bad proportions, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, text, watermark"
}

input_dir = "lora_training/darkmatter"
output_dir = f"lora_training/{character['id']}/img2img_images"
os.makedirs(output_dir, exist_ok=True)

print(f"Buscando imágenes base en {input_dir}...")
image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
print(f"Se encontraron {len(image_files)} imágenes. Iniciando generación img2img...")

def encode_image(image_path):
    # Abrimos la imagen, aseguramos que esté en RGB
    img = Image.open(image_path).convert("RGB")
    # Opcional: redimensionar aquí si la imagen es gigante para no colapsar la VRAM
    img.thumbnail((768, 768)) 
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

for idx, filename in enumerate(image_files):
    file_path = os.path.join(input_dir, filename)
    encoded_image = encode_image(file_path)
    print(f"Procesando {idx+1}/{len(image_files)}: {filename}...")
    
    payload = {
        "init_images": [encoded_image],
        # El prompt reforzará los rasgos e-girl para 'traducir' a la chica de la foto a nuestro personaje
        "prompt": character["base_identity"] + ", masterpiece, best quality, highly detailed, ultra-realistic, 8k resolution, raw photo, film grain",
        "negative_prompt": character["negative"],
        "steps": 40,
        "cfg_scale": 7.0,
        # Denoising strength: 
        # 0.0 = idéntica a la original
        # 1.0 = imagen completamente nueva que ignora la forma
        # 0.45 - 0.55 es perfecto para mantener la pose/fondo pero cambiar la cara/ropa
        "denoising_strength": 0.50, 
        "sampler_name": "DPM++ 2M Karras",
        "seed": -1, # Semilla aleatoria para variedad
        "send_images": True,
        # Mantener proporciones de la imagen fuente (o forzar 512x768, dependiendo)
        # SD.Next ajustará internamente si enviamos estas vars
        "width": 512,
        "height": 768, 
    }
    
    try:
        response = requests.post(url, json=payload, timeout=600)
        if response.ok:
            data = response.json()
            img_data = base64.b64decode(data["images"][0])
            out_path = os.path.join(output_dir, f"raven_img2img_{idx}.png")
            with open(out_path, "wb") as f:
                f.write(img_data)
        else:
            print(f"Failed {filename}: {response.text}")
    except Exception as e:
        print(f"Error generating {filename}: {e}")

print("¡Generación Img2Img completada!")
