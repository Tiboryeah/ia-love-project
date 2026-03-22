import requests
import base64
import os

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
ref_path = r"e:\IALove\references\lilith_face.png"
output_dir = r"e:\IALove\rescue_lilith"
os.makedirs(output_dir, exist_ok=True)

print("Cargando referencia de rostro...")
with open(ref_path, "rb") as f:
    ref_b64 = base64.b64encode(f.read()).decode("utf-8")

def generate_pro(idx, pose_prompt, filename):
    print(f"[*] Generando {filename} con Motor Experto...")
    
    # Payload optimizado: IP-Adapter (Identidad) + LoRA 0.6 (Estilo) + ADetailer (Anatomia)
    payload = {
        "prompt": f"<lora:lilith_goth_v1_5060ti:0.6>, {pose_prompt}, lilith-goth, stunning 18yo goth girl, (extremely large massive breasts:1.2), pale skin, masterpiece",
        "negative_prompt": "ugly, deformed, bad hands, mutated fingers, extra fingers, (old face:1.3), wrinkles, cgi, render, 3d, (malformed genitals:1.2)",
        "steps": 25,
        "cfg_scale": 7.0,
        "width": 512,
        "height": 512,
        "sampler_name": "Euler a",
        "alwayson_scripts": {
            "IP Adapters": {
                "args": [
                    1, False, # num_adapters, unload_adapter
                    "ip-adapter-plus-face_sd15", "None", "None", "None", # adapters (4)
                    0.7, 0.5, 0.5, 0.5, # scales (4)
                    [ref_b64], [], [], [], # files (4 lists)
                    False, False, False, False, # crops (4)
                    0.0, 0.0, 0.0, 0.0, # starts (4)
                    1.0, 1.0, 1.0, 1.0, # ends (4)
                    [], [], [], [], # masks (4)
                    False, "" # layers_active, layers
                ]
            },
            "ADetailer": {
                "args": [
                    {
                        "ad_model": "face_yolov8n.pt",
                        "ad_prompt": "stunningly beautiful youthful face, detailed eyes, masterpiece",
                        "ad_denoising_strength": 0.35
                    },
                    {
                        "ad_model": "Pussy on Pussy.safetensors",
                        "ad_prompt": "extremely detailed pussy, (detailed clitoris:1.1), (wet pink skin:1.1), perfect anatomy",
                        "ad_denoising_strength": 0.5
                    }
                ]
            }
        }
    }

    try:
        res = requests.post(url, json=payload, timeout=120)
        if res.status_code == 200:
            with open(os.path.join(output_dir, filename), "wb") as f:
                f.write(base64.b64decode(res.json()['images'][0]))
            print(f"[+] {filename} exitosa.")
        else:
            print(f"[-] Error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"[-] Error fatal: {e}")

# Poses clave solicitadas
poses = [
    ("portrait photography, looking at camera, bedroom", "sfw_portrait.png"),
    ("full body photography, standing, black dress", "sfw_full.png"),
    ("missionary pose, on bed, legs spread, completely naked", "nsfw_missionary.png"),
    ("doggy style pose, from behind, looking back, completely naked", "nsfw_doggy.png"),
    ("close up on pussy and ass, intimate lighting", "nsfw_detail.png")
]

for pose, name in poses:
    generate_pro(0, pose, name)
