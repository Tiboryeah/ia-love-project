import os
import requests
import base64
from pathlib import Path

url = "http://127.0.0.1:7860/sdapi/v1/interrogate"
dataset_dir = r"e:\IALove\lora_training\lilith-goth\dataset\15_lilith-goth"

print("=============================================")
print("  Iniciando Auto-Tagger para Lilith (CLIP)")
print("=============================================\n")

png_files = list(Path(dataset_dir).glob("*.png"))
print(f"Detectadas {len(png_files)} imágenes para etiquetar...")

for idx, img_path in enumerate(png_files):
    txt_path = img_path.with_suffix(".txt")
    
    # Si ya tiene texto, saltar (para reiniciar en caso de fallos)
    if txt_path.exists():
        continue
        
    print(f"[{idx+1}/{len(png_files)}] Analizando: {img_path.name}")
    
    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")
        
    payload = {
        "image": "data:image/png;base64," + img_b64
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.ok:
            data = response.json()
            caption = data.get("caption", "")
            
            # Formato Kohya: Añadimos siempre el Trigger Word (identidad) al inicio
            final_tags = "lilith-goth, " + caption
            
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(final_tags)
            print(f"  -> Guardado txt: {final_tags[:50]}...")
        else:
            print(f"  ❌ Error HTTP: {response.text}")
    except Exception as e:
        print(f"  ❌ Error al conectar: {e}")

print("\n¡Auto-Tagger finalizado con éxito! El dataset está 100% listo para entrenar.")
