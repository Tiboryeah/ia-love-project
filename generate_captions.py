import os

img_dir = "lora_training/sweet-coco/images"
trigger = "sweet_coco"

# Base descriptions for different parts of the dataset generated
captions = {
    "bikini": "wearing tiny red bikini, beach background, sunny day",
    "casual": "wearing casual white t-shirt, standing in a sunny room",
    "full_body_dress": "full body photo, walking, wearing summer dress, outdoor street",
    "full_body_jeans": "full body photo, standing, wearing ripped jeans and crop top",
    "lingerie": "wearing delicate lace lingerie, bedroom background",
    "seductive": "seductive look, bedroom eyes, slightly parted lips",
    "serious": "serious dramatic expression, piercing gaze",
    "laughing": "laughing happily, wide smile with teeth, bright eyes",
    "high_angle": "high angle selfie, looking up at camera",
    "low_angle": "low angle portrait, looking down slightly",
    "front_close": "close up portrait photo, looking directly at camera, soft smile",
    "side_profile": "side profile portrait, looking away, neutral expression",
    "full_body_back": "full body photo from behind, looking over shoulder",
    
    # NSFW
    "nsfw_pose_doggy": "from behind, doggy style pose, completely naked, showing full ass",
    "nsfw_pose_missionary": "lying on back, spread legs, missionary pose, looking up at camera, completely naked",
    "nsfw_pose_cowgirl": "straddling, cowgirl pose, sitting on top, completely naked, visible breasts",
    "nsfw_pose_bent_over": "bent over, looking back over shoulder, completely naked",
    "nsfw_detail_breasts": "extreme close up of breasts, completely naked torso",
    "nsfw_detail_pussy": "extreme close up of pussy, spread legs, completely naked, explicit genitalia",
    "nsfw_detail_ass": "close up of ass, completely naked, from behind",
    "nsfw_detail_thighs": "close up of thighs and hips, completely naked, standing pose",
    "nsfw_detail_feet": "close up of bare feet and toes, detailed soles, completely naked", # We deleted this one but just in case
    "nsfw_detail_hands": "close up of hands with manicured fingers resting on naked body",
    "nsfw_giving_bj": "close up of face looking up, mouth open, suggestive facial expression, ahegao",
    "nsfw_afterglow": "messy hair, sweaty skin, lying in bed completely naked, flushed face"
}

base_tags = "woman, blonde hair, blue eyes, beautiful, highly detailed"

if os.path.exists(img_dir):
    for filename in os.listdir(img_dir):
        if filename.endswith(".png"):
            txt_filename = filename.replace(".png", ".txt")
            
            # Find matching caption
            matched_cap = ""
            for key, val in captions.items():
                if key in filename:
                    matched_cap = val
                    break
            
            # Combine trigger + base tags + specific caption
            full_caption = f"{trigger}, {base_tags}, {matched_cap}"
            
            with open(os.path.join(img_dir, txt_filename), "w") as f:
                f.write(full_caption)
    print("Caption files generated successfully.")
else:
    print("Directory not found.")
