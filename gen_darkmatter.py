import os
import time
import requests
import base64

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
models_url = "http://127.0.0.1:7860/sdapi/v1/sd-models"

# 1. Esperar a que la API este viva
print("Esperando a que SD.Next arranque y cargue sus modelos (esto toma ~1-2 mins)...")
while True:
    try:
        resp = requests.get(models_url, timeout=5)
        if resp.status_code == 200:
            break
    except:
        pass
    time.sleep(3)
    print("Aun cargando...")

print("\n¡SD.Next esta listo y escuchando!")

# 2. Configurar el Payload con el LoRA y Hires Fix para Maxima Calidad
payload = {
    "prompt": "masterpiece, best quality, ultra detailed, extremely detailed photo of darkmatter, completely naked, nude, explicit nsfw, spreading legs, full nude body, visible pussy, beautiful breasts, visible nipples, heavy alternative makeup, dark lipstick, multiple facial piercings, facial tattoos, neck tattoos, extensive full body tattoos, full sleeves tattoos, tattooed chest, alternative goth girl, short dark hair, perfect eyes, professional lighting, 8k resolution, perfect anatomy, symmetrical body, smooth skin, <lora:darkmatter:0.85>",
    "negative_prompt": "clothing, clothes, lingerie, underwear, latex, bodysuit, bra, panties, lowres, bad anatomy, bad hands, deformed hands, mutated hands, missing fingers, extra digit, mutated fingers, fused fingers, poorly drawn hands, asymmetrical breasts, uneven breasts, lumpy legs, mutated legs, deformed legs, ugly face, deformed face, poorly drawn face, bad face, deformed mask, cross-eyed, text, error, cropped, worst quality, low quality, normal quality, jpeg artifacts, watermark, blurry, deformed, cartoon, illustration, drawing, mutant, disfigured",
    "steps": 35,
    "cfg_scale": 7.0,
    "width": 512,
    "height": 768,
    "enable_hr": True,
    "hr_scale": 2,
    "hr_upscaler": "R-ESRGAN 4x+",
    "denoising_strength": 0.5,
    "sampler_name": "Euler a",
    "seed": -1,
    "restore_faces": False,
    "send_images": True
}

print(f"\nEncendiendo la fragua de Darkmatter...\nLoRA activado: <lora:darkmatter:0.85>")
print("Dibujando una foto de ULTRA ALTA RESOLUCION (2x Hires Fix)...")
print("Tiempo estimado con la 5060 Ti: ~8-12 segundos (antes tomaba mins)")

# 3. Pedir la generacion
try:
    response = requests.post(url, json=payload, timeout=900)
    if response.ok:
        data = response.json()
        if "images" in data and len(data["images"]) > 0:
            img_data = base64.b64decode(data["images"][0])
            output_path = os.path.join(os.getcwd(), "DARKMATTER_PERFECTA_V4.png")
            with open(output_path, "wb") as f:
                f.write(img_data)
            print(f"\n¡¡VICTORIA!! 🏆")
            print(f"Tu diosa esta lista en HD (1024x1536). Abre esta ruta:")
            print(f"👉 {output_path} 👈")
        else:
            print("Hubo conexion pero la respuesta no trajo imagen.")
            print(f"Respuesta JSON: {data}")
    else:
        print(f"El generador respondio con error: HTTP {response.status_code} - {response.text}")
except Exception as e:
    print(f"\nError catastrofico durante la generacion: {e}")
