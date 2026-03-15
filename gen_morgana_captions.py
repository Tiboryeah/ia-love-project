import os

img_dir = "lora_training/morgana-goth/images"
trigger = "morgana_goth"

captions = {
    # Angulos
    "front_close": "close up portrait photo, looking directly at camera, soft smile",
    "side_profile": "side profile portrait, looking away, neutral expression",
    "high_angle": "high angle selfie, looking up at camera",
    "low_angle": "low angle portrait, looking down slightly",
    
    # Expresiones
    "laughing": "laughing happily, wide smile with teeth, bright eyes",
    "serious": "serious dramatic expression, piercing gaze",
    "seductive": "seductive look, bedroom eyes, slightly parted lips",
    
    # Ropa y cuerpo
    "casual": "wearing casual black gothic t-shirt, standing in a sunny room",
    "gym": "wearing tight black sports bra and shorts, gym wall background",
    "elegant": "wearing elegant black evening dress, luxury background",
    "lingerie": "wearing delicate black lace lingerie, bedroom background",
    "bikini": "wearing tiny black bikini, beach background, sunny day",
    "full_body_jeans": "full body photo, standing, wearing black ripped jeans and crop top",
    "full_body_dress": "full body photo, walking, wearing black gothic dress",
    "full_body_back": "full body photo from behind, looking over shoulder",
    
    # NSFW
    "nsfw_pose_doggy": "from behind, doggy style pose, completely naked, showing full ass",
    "nsfw_pose_missionary": "lying on back, spread legs, missionary pose, looking up at camera, completely naked",
    "nsfw_pose_cowgirl": "straddling, cowgirl pose, sitting on top, completely naked, visible huge breasts",
    "nsfw_pose_bent_over": "bent over, looking back over shoulder, completely naked, explicit",
    "nsfw_detail_breasts": "extreme close up of huge breasts, completely naked torso",
    "nsfw_detail_pussy": "extreme close up of pussy, spread legs, completely naked, explicit genitalia",
    "nsfw_detail_ass": "close up of ass, completely naked, from behind",
    "nsfw_detail_thighs": "close up of thighs and hips, completely naked, standing pose",
    "nsfw_detail_feet": "close up of bare feet and toes, detailed soles, completely naked",
    "nsfw_detail_hands": "close up of hands with manicured fingers resting on naked body",
    "nsfw_giving_bj": "close up of face looking up, mouth open, suggestive facial expression, ahegao",
    "nsfw_afterglow": "messy hair, sweaty skin, lying in bed completely naked, flushed face"
}

base_tags = "20 year old gothic woman, pale skin, huge breasts, black hair, makeup, instagram model"

if os.path.exists(img_dir):
    for filename in os.listdir(img_dir):
        if filename.endswith(".png"):
            txt_filename = filename.replace(".png", ".txt")
            
            matched_cap = ""
            for key, val in captions.items():
                if key in filename:
                    matched_cap = val
                    break
            
            full_caption = f"{trigger}, {base_tags}, {matched_cap}"
            
            with open(os.path.join(img_dir, txt_filename), "w") as f:
                f.write(full_caption)
    print("Captions generated for Morgana mapping!")
else:
    print("Wait for images to finish generating.")
