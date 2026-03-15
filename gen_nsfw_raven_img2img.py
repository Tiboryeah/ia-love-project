import os
import requests
import base64
from io import BytesIO
from PIL import Image

url = "http://127.0.0.1:7860/sdapi/v1/img2img"

character = {
    "id": "raven-egirl",
    "base_identity": "stunningly beautiful 20 year old e-girl goth woman, completely naked, extremely pale skin, bare breasts, nipples, thick thighs, full round ass, explicit nude body, perfect anatomy, symmetrical features, heavy e-girl makeup, black choker, black hair with bangs, piercing gaze",
    "negative": "clothes, bra, panties, underwear, lingerie, covered, deformed, ugly, monster, horror, blurry, lowres, low quality, worst quality, bad anatomy, bad proportions, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, text, watermark"
}

input_dir = "lora_training/darkmatter"
output_dir = f"lora_training/{character['id']}/img2img_nsfw_images"
os.makedirs(output_dir, exist_ok=True)

print(f"Iniciando generación Img2Img + NSFW desde el directorio base {input_dir}...")
image_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
print(f"Se transformarán {len(image_files)} fotos originales en contenido RAW de alta resolución.")

def encode_image(image_path):
    img = Image.open(image_path).convert("RGB")
    # Redimensionamos exactamente a 512x768 para alinear tensores en GPU
    img = img.resize((512, 768), Image.Resampling.LANCZOS) 
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

for idx, filename in enumerate(image_files):
    file_path = os.path.join(input_dir, filename)
    encoded_image = encode_image(file_path)
    print(f"Procesando NSFW {idx+1}/{len(image_files)}: {filename}...")
    
    payload = {
        "init_images": [encoded_image],
        "prompt": character["base_identity"] + ", masterpiece, best quality, highly detailed, ultra-realistic, 8k resolution, raw photo, film grain",
        "negative_prompt": character["negative"],
        "steps": 40,
        "cfg_scale": 7.0,
        
        # Como queremos quitar la ropa que tiene actualmente la foto, subiremos la fuerza de ruido.
        # Un Denoising entre 0.60 y 0.70 permite 'destruir' la ropa original pero mantener la pose intacta.
        "denoising_strength": 0.65, 
        
        "sampler_name": "DDIM",
        "seed": -1, # Random
        "send_images": True,
        "width": 512,
        "height": 768, 
    }
    
    try:
        response = requests.post(url, json=payload, timeout=600)
        if response.ok:
            data = response.json()
            if "images" in data and len(data["images"]) > 0:
                img_data = base64.b64decode(data["images"][0])
                out_path = os.path.join(output_dir, f"raven_nsfw_img2img_{idx}.png")
                with open(out_path, "wb") as f:
                    f.write(img_data)
            else:
                print(f"Error, no images valids, full response: {data}")
        else:
            print(f"Failed {filename}: {response.text}")
    except Exception as e:
        # Mostramos advertencias de conectividad por si el API sigue cerrado
        if "HTTPConnectionPool" in str(e):
            print(f"Error Crítico: Tu servidor de SD.Next no está respondiendo. Ejecuta primero webui.bat.")
            break
        else:
            print(f"Error generando {filename}: {e}")

print("¡Proceso a completado! Revisa la carpeta img2img_nsfw_images")
