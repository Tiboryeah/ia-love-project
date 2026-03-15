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

print("¡Conectado! Generando pruebas de poses para Darkmatter...\n")

# Definir las poses a probar
poses = [
    {
        "name": "standing_full_body",
        "prompt": "masterpiece, best quality, ultra detailed, photo of darkmatter standing, full body shot, looking at viewer, nude, heavy alternative makeup, dark lipstick, neck tattoos, extensive full body tattoos, short dark hair, perfect eyes, professional lighting, 8k resolution, perfect anatomy",
    },
    {
        "name": "lying_on_bed",
        "prompt": "masterpiece, best quality, ultra detailed, photo of darkmatter lying on a bed, lounging, seductive look, nude, stomach tattoos visible, thigh tattoos visible, short dark hair, soft room lighting, 8k resolution, perfect anatomy",
    },
    {
        "name": "profile_back_view",
        "prompt": "masterpiece, best quality, ultra detailed, photo of darkmatter from the side, profile view, back tattoos visible, looking over shoulder, nude, short dark hair, moody lighting, 8k resolution, perfect anatomy",
    },
    {
        "name": "sitting_on_chair",
        "prompt": "masterpiece, best quality, ultra detailed, photo of darkmatter sitting on a modern chair, legs crossed, elegant pose, nude, arm tattoos visible, short dark hair, professional studio lighting, 8k resolution, perfect anatomy",
    }
]

# Configuración base
base_payload = {
    "negative_prompt": "clothing, clothes, lingerie, underwear, latex, bodysuit, bra, panties, lowres, bad anatomy, bad hands, deformed hands, mutated hands, missing fingers, extra digit, mutated fingers, fused fingers, poorly drawn hands, asymmetrical breasts, uneven breasts, lumpy legs, mutated legs, deformed legs, ugly face, deformed face, poorly drawn face, bad face, deformed mask, cross-eyed, text, error, cropped, worst quality, low quality, normal quality, jpeg artifacts, watermark, blurry, deformed, cartoon, illustration, drawing, mutant, disfigured, extra limbs, extra feet, deformed feet",
    "steps": 30,
    "cfg_scale": 7.0,
    "width": 512,
    "height": 768,
    "sampler_name": "Euler a",
    "seed": -1, # Cambiar a un número fijo si quieres repetir un resultado
    "restore_faces": True,
    "send_images": True
}

for pose in poses:
    payload = base_payload.copy()
    payload["prompt"] = pose["prompt"] + ", <lora:darkmatter:0.85>"
    
    print(f"Generando pose: {pose['name']}...")
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload, timeout=600)
        if response.ok:
            data = response.json()
            if "images" in data and len(data["images"]) > 0:
                img_data = base64.b64decode(data["images"][0])
                filename = f"TEST_DARKMATTER_{pose['name']}.png"
                output_path = os.path.join(os.getcwd(), filename)
                with open(output_path, "wb") as f:
                    f.write(img_data)
                
                elapsed = time.time() - start_time
                print(f"✅ Guardado en: {filename} (Tiempo: {elapsed:.1f}s)")
            else:
                print(f"❌ No se recibió imagen para {pose['name']}")
        else:
            print(f"❌ Error API ({response.status_code}) en {pose['name']}")
    except Exception as e:
        print(f"❌ Error al generar {pose['name']}: {e}")

print("\n¡Pruebas completadas! Revisa los archivos TEST_DARKMATTER_*.png")
