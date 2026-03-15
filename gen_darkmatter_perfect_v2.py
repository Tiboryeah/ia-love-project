import os
import time
import requests
import base64

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
models_url = "http://127.0.0.1:7860/sdapi/v1/sd-models"

# 1. Esperar a que la API esté viva
print("Esperando a que SD.Next arranque (esto puede tomar ~2-3 mins en CPU)...")
while True:
    try:
        resp = requests.get(models_url, timeout=5)
        if resp.status_code == 200:
            break
    except:
        pass
    time.sleep(10)
    print("Aun cargando...")

print("¡Conectado! Forjando la versión perfecta de Darkmatter...\n")

# 2. Configuración con Hires Fix y Prompts Técnicos
payload = {
    "prompt": "masterpiece, best quality, ultra detailed, photorealistic, extremely detailed photo of darkmatter, beautiful symmetric face, (bridge piercing:1.2), (nasallang piercing:1.2), (septum ring:1.1), (medusa piercing:1.1), (vertical labret:1.1), nostril studs, perfect eyes with dark eyeliner, dark goth lipstick, heavy alternative makeup, short dark hair, (small pink round nipples:1.3), perfect breasts, perfect symmetric anatomy, detailed fingers, 5 fingers per hand, standing, nude, extensive full body tattoos, full sleeves tattoos, neck tattoos, professional studio lighting, depth of field, 8k resolution, <lora:darkmatter:0.8>",
    "negative_prompt": "bad anatomy, (extra fingers:1.5), (mutated hands:1.5), (fused fingers:1.5), deformed hands, missing fingers, extra legs, extra arms, (deformed nipples:1.4), (brown nipples:1.3), asymmetrical breasts, blurry face, lowres, bad hands, text, error, cropped, worst quality, low quality, normal quality, jpeg artifacts, watermark, blurry, deformed body, extra limbs",
    "steps": 35,
    "cfg_scale": 7.5,
    "width": 512,
    "height": 768,
    "sampler_name": "Euler a",
    "seed": -1,
    "enable_hr": True, # HIRES FIX ES CLAVE PARA LAS MANOS Y PIERCINGS
    "hr_scale": 1.5,
    "hr_upscaler": "R-ESRGAN 4x+",
    "denoising_strength": 0.4,
    "restore_faces": True,
    "send_images": True
}

print("Generando imagen de alta resolución... (esto tomará ~10-12 minutos en CPU)")
start_time = time.time()

try:
    response = requests.post(url, json=payload, timeout=1200)
    if response.ok:
        data = response.json()
        if "images" in data and len(data["images"]) > 0:
            img_data = base64.b64decode(data["images"][0])
            output_path = os.path.join(os.getcwd(), "DARKMATTER_PERFECTA_V2.png")
            with open(output_path, "wb") as f:
                f.write(img_data)
            
            elapsed = time.time() - start_time
            print(f"\n¡VICTORIA! 🏆 Imagen guardada como: DARKMATTER_PERFECTA_V2.png")
            print(f"Tiempo total: {elapsed/60:.1f} minutos.")
        else:
            print("Error: No se recibió ninguna imagen.")
    else:
        print(f"Error de API: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Error catastrófico: {e}")
