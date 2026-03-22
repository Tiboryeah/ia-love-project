import os
import requests
import base64

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
reference_img_path = r"e:\IALove\references\lilith_face.png"

print("Cargando la Foto Maestra de Lilith...")
with open(reference_img_path, "rb") as f:
    ref_b64 = base64.b64encode(f.read()).decode("utf-8")

character = {
    "id": "lilith-goth",
    "base_identity": "stunningly beautiful 18 year old goth girl, extremely pale porcelain skin, dark aesthetic makeup, heavy black eyeliner, black lipstick, (large perky breasts, natural cleavage:1.1), short waist, wide hips, thick thicc thighs, hourglass aesthetic, professional instagram photo",
    "negative": "mutant hands, extra fingers, malformed feet, deformed fingers, extra limbs, ugly, horror, blurry, bad anatomy, worst quality, missing fingers, fused fingers, asymmetrical breasts, ugly face, cross-eyed, text, watermark, completely censored"
}

# TÉCNICA ANTI-DEFORMIDADES: Usar encuadres como "upper body", "cowboy shot" o anclar manos ("arms crossed", "hands behind back")
sfw_prompts = [
    "upper body shot, {identity}, wearing black casual crop top, hands behind back, standing in city street, realistic lighting",
    "cowboy shot, {identity}, wearing elegant black gothic dress, arms folded across chest, luxury room background",
    "portrait photo, {identity}, wearing leather jacket, leaning against brick wall, hands in pockets, edgy vibe",
    "upper body shot, {identity}, wearing tight black sweater, hands resting on hips out of frame, cafe background",
    "medium close up, {identity}, wearing delicate black lace blouse, looking over shoulder, soft indoor lighting",
    "cowboy shot, {identity}, wearing punk rock t-shirt and choker, holding crossed arms, gig venue background",
    "portrait photo, {identity}, wearing black summer dress, smiling softly, sunny park background, hands behind head",
    "upper body shot, {identity}, wearing dark gym wear, sports bra, hands behind back, gym mirror selfie style",
    "medium shot, {identity}, wearing velvet corset, elegant sitting posture, hands resting on lap out of frame",
    "cowboy shot, {identity}, wearing oversized black hoodie, hiding hands in sleeves, street photography"
]

nsfw_prompts = [
    "cowboy shot, {identity}, completely naked, standing naturally, arms behind head, soft bedroom lighting, explicit",
    "upper body shot, {identity}, completely naked, looking seductively at camera, hands behind back, showing beautiful breasts",
    "medium shot, {identity}, doing doggy style pose, from behind, showing perfect ass, face turning to camera, dark background",
    "cowboy shot, {identity}, completely naked, sitting on bed edge, hands resting flat on bed out of frame, explicit full body",
    "upper body shot, {identity}, completely naked, leaning forward slightly, arms folded under breasts, intimate lighting",
    "medium close up, {identity}, totally naked, laying on stomach on silk sheets, hands hidden under pillow, looking at camera",
    "cowboy shot, {identity}, completely naked, standing in shower, wet hair, hands touching neck, explicit realistic skin",
    "upper body shot, {identity}, wearing only open black leather jacket, exposing completely naked breasts, hands in pockets",
    "medium shot, {identity}, completely naked, sitting on chair, legs crossed, hands behind back, artistic shadow lighting",
    "upper body shot, {identity}, completely naked, holding arms upwards stretching, revealing torso and breasts perfectly"
]

output_dir = f"lora_training/{character['id']}/mass_dataset"
os.makedirs(output_dir, exist_ok=True)

print(f"\nGenerando 60 Fotos (30 SFW + 30 NSFW) con Tácticas Anti-Manos/Pies...")

def generar_lote(categoria, lista_prompts, semilla_base):
    for i, prompt_template in enumerate(lista_prompts):
        full_prompt = prompt_template.format(identity=character["base_identity"]) + ", masterpiece, high quality, RAW photo, best quality"
        
        print(f"\n[+] Procesando {categoria} Template {i+1}/10...")
        
        for j in range(3): # 3 Seeds por cada template = 30 fotos
            print(f"  -> Generando variante {j+1}/3...")
            
            payload = {
                "prompt": full_prompt,
                "negative_prompt": character["negative"],
                "steps": 35,
                "cfg_scale": 7.0,
                "width": 512,
                "height": 768,
                "enable_hr": True,
                "hr_scale": 1.5,
                "hr_upscaler": "R-ESRGAN 4x+",
                "denoising_strength": 0.5,
                "sampler_name": "DPM++ 2M",
                "seed": semilla_base + i*10 + j, 
                "send_images": True,
                "alwayson_scripts": {
                    "IP Adapters": {
                        "args": [
                            1, False,
                            "ip-adapter-plus-face_sd15", "None", "None", "None",
                            0.8, 0.5, 0.5, 0.5,
                            [ref_b64], [], [], [],
                            True, False, False, False,
                            0.0, 0.0, 0.0, 0.0,
                            1.0, 1.0, 1.0, 1.0,
                            [], [], [], [],
                            False, ""
                        ]
                    },
                    "ADetailer": {
                        "args": [
                            {
                                "ad_model": "face_yolov8n.pt",
                                "ad_prompt": "stunningly beautiful goth face, perfectly symmetrical",
                                "ad_denoising_strength": 0.35,
                                "ad_clip_skip": 2,
                                "ad_confidence": 0.3
                            }
                        ]
                    }
                }
            }
            
            try:
                response = requests.post(url, json=payload, timeout=900)
                if response.ok:
                    data = response.json()
                    img_data = base64.b64decode(data["images"][0])
                    filename = f"lilith_{categoria}_t{i+1}_v{j+1}.png"
                    with open(f"{output_dir}/{filename}", "wb") as f:
                        f.write(img_data)
                    print(f"     ✅ Guardada: {filename}")
            except Exception as e:
                print(f"     ❌ Error en {categoria} (t{i+1}-v{j+1}): {e}")

generar_lote("SFW", sfw_prompts, 10000)
generar_lote("NSFW", nsfw_prompts, 20000)

print(f"\n¡Generación Masiva Completada!\nCarperta: {output_dir}")
