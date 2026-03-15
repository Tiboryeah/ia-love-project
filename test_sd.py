import requests
import base64
import time
import numpy as np
from PIL import Image
import io

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

# Coco's identity + Extreme Realism Tags
coco_prompt = (
    "portrait of a beautiful young woman, platinum bob hair shoulder length, "
    "large expressive blue eyes, small nose, soft cheeks, light freckles, "
    "fair skin, rosy lips, innocent playful smile, choker necklace, 25 years old, "
    "selfie photo taken with phone, casual bedroom lighting, natural no-filter look, real life candid shot, "
    "extraordinarily hyperrealistic, professional photo session, Kodak Portra 400, "
    "sharp focus, 8k uhd, highly detailed skin pores, realistic blue eyes, natural expression, sunlight, "
    "depth of field, master photography, (extreme detail:1.3), award winning photography, "
    "realistic lighting, (film grain:0.8), (photorealistic:1.4), (real person:1.3), high skin texture detail"
)

coco_negative = (
    "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), "
    "text, watermark, logo, blur, low quality, worst quality, bad anatomy, mutation, deformed, "
    "disfigured, poorly drawn face, extra limbs, missing hands, signature, "
    "rainbow colors, colorful artifacts, glitch, chromatic aberration, oversaturated, neon colors, "
    "painted face, makeup smeared, psychedelic, fake skin, plastic skin, smooth skin, doll like, "
    "bad teeth, cross-eyed, dark hair, brunette, asian, dark eyes, long hair, red hair"
)

payload = {
    "prompt": coco_prompt,
    "negative_prompt": coco_negative,
    "steps": 20,
    "cfg_scale": 7.0,
    "width": 512,
    "height": 512,
    "sampler_name": "Euler a",
    "seed": 42069,
    "send_images": True,
}

print("Generating Coco 'Candy.ai Realism' (20 steps, RV6.0)...")
t0 = time.time()
r = requests.post(url, json=payload, timeout=240)
elapsed = time.time() - t0
data = r.json()

if data.get("images"):
    img_bytes = base64.b64decode(data["images"][0])
    img = Image.open(io.BytesIO(img_bytes))
    print(f"Done in {elapsed:.0f}s")
    img.save("test_realism.png")
    print("Saved: test_realism.png")
else:
    print("FAIL")
