import os
import time
import requests
import base64

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
models_url = "http://127.0.0.1:7860/sdapi/v1/sd-models"

# Directorio de salida
output_dir = r"c:\Users\USER\.gemini\antigravity\scratch\IALove\darkmatter_dataset_v2\10_darkmatter_sfw"
os.makedirs(output_dir, exist_ok=True)

# Outfits para el dataset SFW
sfw_outfits = [
    "black oversized hoodie with alternative graphics, street style",
    "black lace corset top with leather pants, punk style",
    "distressed band t-shirt, skinny jeans, silver chains",
    "black latex bodysuit, high fashion alternative",
    "techwear jacket with buckles and straps, futuristic goth",
    "black velvet dress, elegant gothic look",
    "fishnet top over a black tank top, edgy alternative",
    "leather biker jacket, white t-shirt, dark aesthetic",
    "cropped black sweater, plaid skirt, alt girl style",
    "sheer black lace top, tactical vest, mixed style",
    "black denim jacket with patches, combat boots visible",
    "gothic lolita inspired black dress with ruffles",
    "oversized flannel shirt, black bra visible underneath, casual alt",
    "pvc mini skirt, mesh top, nightclub alternative style",
    "hooded black cloak, mysterious gothic priestess vibe"
]

def wait_for_api():
    print("Esperando a que la API esté lista...")
    while True:
        try:
            r = requests.get(models_url, timeout=5)
            if r.status_code == 200:
                return True
        except:
            pass
        time.sleep(10)

if __name__ == "__main__":
    wait_for_api()
    print("¡API lista! Generando dataset SFW para Darkmatter v2.0...\n")

    for i, outfit in enumerate(sfw_outfits):
        prompt = f"masterpiece, best quality, photorealistic, photo of darkmatter, wearing {outfit}, highly detailed face, piercings, tattoos visible on neck and arms, short dark hair, symmetric features, professional lighting, 8k resolution, <lora:darkmatter:0.8>"
        
        payload = {
            "prompt": prompt,
            "negative_prompt": "nude, naked, nsfw, nipples, pussy, bad anatomy, deformed hands, extra fingers, blurry, low quality, watermark",
            "steps": 30,
            "cfg_scale": 7.0,
            "width": 512,
            "height": 768,
            "sampler_name": "Euler a",
            "seed": -1,
            "restore_faces": True
        }

        print(f"Generando imagen {i+1}/15: {outfit[:30]}...")
        try:
            response = requests.post(url, json=payload, timeout=600)
            if response.ok:
                data = response.json()
                img_data = base64.b64decode(data["images"][0])
                filename = f"darkmatter_sfw_{i+1:02d}.png"
                with open(os.path.join(output_dir, filename), "wb") as f:
                    f.write(img_data)
                print(f"✅ Guardado: {filename}")
            else:
                print(f"❌ Error en imagen {i+1}")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("\n¡Dataset SFW completado en darkmatter_dataset_v2/10_darkmatter_sfw!")
