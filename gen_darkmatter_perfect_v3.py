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

print("¡Conectado! Refinando la perfección de Darkmatter (v3)...\n")

# 2. Configuración con Hires Fix y Prompts Técnicos Extremos
# - Reducimos fuerza del LoRA para mejorar anatomía (manos)
# - Forzamos pezones pequeños y rosados
# - Usamos un Negative Prompt más pesado para las manos
payload = {
    "prompt": "masterpiece, best quality, ultra detailed, photorealistic, photo of darkmatter, symmetry, beautiful symmetric face, bridge piercing, nasallang piercing, septum ring, medusa piercing, vertical labret, nostrils studs, perfect eyes, dark goth lipstick, heavy alternative makeup, short dark hair, (tiny small pink round nipples:1.4), (perfect small breasts:1.2), perfect symmetric anatomy, (highly detailed 5 fingers per hand:1.3), full body standing, nude, extensive sharp full body tattoos, full sleeves tattoos, neck tattoos, professional studio lighting, depth of field, 8k resolution, <lora:darkmatter:0.7>",
    "negative_prompt": "bad anatomy, (extra fingers:1.6), (mutated hands:1.6), (fused fingers:1.6), deformed hands, missing fingers, extra legs, (giant nipples:1.5), (large nipples:1.4), (brown nipples:1.3), asymmetrical breasts, blurry face, lowres, bad hands, text, error, cropped, worst quality, low quality, normal quality, jpeg artifacts, watermark, blurry, deformed body, extra limbs, (nipple piercings:1.4)", # Agregué nipple piercings a negativo porque a veces los confunde con pezones grandes
    "steps": 40,
    "cfg_scale": 7.0,
    "width": 512,
    "height": 768,
    "sampler_name": "Euler a",
    "seed": -1,
    "enable_hr": True, 
    "hr_scale": 1.5,
    "hr_upscaler": "R-ESRGAN 4x+",
    "denoising_strength": 0.35, # Bajamos el denoising para que el Hires Fix no invente cosas raras
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
            output_path = os.path.join(os.getcwd(), "DARKMATTER_PERFECTA_V3.png")
            with open(output_path, "wb") as f:
                f.write(img_data)
            
            elapsed = time.time() - start_time
            print(f"\n¡INTENTO 3 COMPLETADO! 🏆 Imagen guardada como: DARKMATTER_PERFECTA_V3.png")
            print(f"Tiempo total: {elapsed/60:.1f} minutos.")
        else:
            print("Error: No se recibió ninguna imagen.")
    else:
        print(f"Error de API: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Error catastrófico: {e}")
