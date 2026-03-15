import os
import glob

dir_path = r"c:\Users\USER\.gemini\antigravity\scratch\IALove\lora_training\darkmatter"
trigger = "darkmatter"
base_tags = "young woman, highly detailed, photorealistic"

extensions = ["*.jpg", "*.jpeg", "*.png"]
files = []
for ext in extensions:
    files.extend(glob.glob(os.path.join(dir_path, ext)))

for file_path in files:
    filename = os.path.basename(file_path)
    name_no_ext = os.path.splitext(filename)[0]
    
    # Clean name (convert snake_case to readable tags)
    desc = name_no_ext.replace('_', ' ')
    
    txt_path = os.path.splitext(file_path)[0] + ".txt"
    full_caption = f"{trigger}, {base_tags}, {desc}"
    
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(full_caption)
        
print("Captions generated for Darkmatter successfully!")
