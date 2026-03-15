import shutil
import os

source_dir = r"c:\Users\USER\.gemini\antigravity\scratch\IALove\lora_training\darkmatter"
output_filename = r"c:\Users\USER\.gemini\antigravity\scratch\IALove\darkmatter_dataset_v1"

print(f"Zipping {source_dir}...")
shutil.make_archive(output_filename, 'zip', source_dir)
print(f"Successfully created {output_filename}.zip!")
