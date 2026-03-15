import { NextResponse } from 'next/server';

// ============================================================
// CHARACTER VISUAL IDENTITY PROFILES
// Each character has: fixed seed, detailed face/body description
// The fixed seed + detailed physical description = consistent identity
// ============================================================
const CHARACTER_PROFILES: Record<string, {
    seed: number;
    identity: string;
    negativeExtras: string;
    hasLora?: boolean;
    loraName?: string;
}> = {
    "sweet-coco": {
        seed: -1, // Changed to random seed for varied natural results
        hasLora: true,
        loraName: "sweet_coco_v1",
        identity: "blonde woman, flawless skin, mesmerizing eyes, elegant features, perfect smile",
        negativeExtras: "ugly, deformed, monster, freckles, bumps, acne, rough skin, old, masculine, horror, scary, distorted,"
    },
    "fitness-vicky": {
        seed: 343434,
        identity: "stunningly beautiful fitness model, (face of Gal Gadot:0.4), flawless tanned skin, bright green eyes, athletic but feminine features, perfectly symmetrical face, gorgeous smile",
        negativeExtras: "masculine, rough skin, acne, bumps, freckles, distorted face, ugly, old,"
    },
    "goth-darkangel": {
        seed: 565656,
        identity: "stunningly beautiful goth woman, (face of Jenna Ortega:0.4), flawless porcelain skin, raven dark hair, captivating dark eyes, elegant sharp features, beautiful aesthetic makeup",
        negativeExtras: "monster, horror, scary, creepy, vampire, ghost, ugly, deformed, freckles, messy makeup,"
    },
    "morgana-dark": {
        seed: 99999,
        identity: "stunningly beautiful 35 year old woman, (face of Monica Bellucci:0.4), sophisticated elegant woman, flawless skin, dark brunette hair, sharp elegant facial features, deep captivating eyes",
        negativeExtras: "blonde, casual, messy, old, wrinkles,"
    },
    "hana-chan": {
        seed: 12345,
        identity: "stunningly beautiful young asian woman, flawless beautifully smooth skin, cute aesthetic, pink hair, big captivating eyes, youthful features",
        negativeExtras: "blonde, western features, mature, old,"
    },
};

// Style descriptors per situation
const STYLE_PRESETS: Record<string, string> = {
    selfie: "candid selfie photo, casual lighting, smartphone camera quality, home interior background",
    cinematic: "cinematic lighting, professional 8k sharp photo, shallow depth of field, bokeh background",
    nsfw: "extremely explicit, uncensored, (completely naked:1.3), intimate photography, highly detailed body parts, natural skin textures, raw skin pores, intimate lighting, seductive pose, masterpiece",
    full_body: "full body shot, standing, wide angle, showing legs and head, room background",
    mixed: "natural lighting, everyday candid photo",
};

const BASE_QUALITY = "stunningly beautiful woman, perfect facial symmetry, mesmerizing eyes, professional photography, soft cinematic lighting, vivid colors, depth of field, 8k uhd, masterpiece, clean aesthetic";
const BASE_NEGATIVE = "deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, paint, anime, text, watermark, signature, bad anatomy, mutation, deformed face, disfigured, messy makeup, horror, scary, creepy, old, wrinkles";

export async function POST(req: Request) {
    try {
        const { prompt, characterName, style = "mixed" } = await req.json();

        // Get character profile for identity consistency
        const charProfile = CHARACTER_PROFILES[characterName];
        const styleDesc = STYLE_PRESETS[style] || STYLE_PRESETS.mixed;
        const seed = charProfile?.seed ?? -1; // -1 = random if no profile

        // Build a prompt that describes BOTH who she is AND what she's doing
        let finalPrompt: string;
        let finalNegative: string;

        if (charProfile) {
            // Check if this character has a LoRA model trained
            // Lowered weight to 0.60 to completely eliminate pixelation/deep-frying from the training
            const loraPrefix = (charProfile as any).hasLora ? `<lora:${(charProfile as any).loraName}:0.60>, ` : "";

            // Identity must be at the very front for maximum consistency
            const actionContext = prompt || "looking at camera, warm smile";
            const shotType = style === "full_body" ? "full body photography" : "portrait photography";

            // Format: [LoRA], [Shot Type], [Action], [Character Identity], [Style], [Quality]
            finalPrompt = `${loraPrefix}${shotType}, ${actionContext}, ${charProfile.identity}, ${styleDesc}, ${BASE_QUALITY}`;
            finalNegative = `${BASE_NEGATIVE}, ${charProfile.negativeExtras}`;
        } else {
            // Fallback for unknown characters
            finalPrompt = `beautiful woman, ${styleDesc}, ${prompt || ""}, ${BASE_QUALITY}`;
            finalNegative = BASE_NEGATIVE;
        }

        const payload = {
            prompt: finalPrompt,
            negative_prompt: finalNegative,
            steps: 18,          // Lowered to 18 to prevent 3-minute CPU timeout on NextJS
            cfg_scale: 5.0,     // Lowered from 7.0 to 5.0 to prevent deep-fried/pixelated artifacting
            width: 512,
            height: 512,
            sampler_name: "Euler a",
            seed: seed,
            send_images: true,
            save_images: true,
        };

        console.log(`[Image API] char=${characterName} style=${style} seed=${seed}`);
        console.log(`[Image API] prompt: ${finalPrompt.slice(0, 120)}...`);

        const response = await fetch('http://127.0.0.1:7860/sdapi/v1/txt2img', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
            signal: AbortSignal.timeout(180000), // 3 min timeout for CPU
        });

        if (response.ok) {
            const data = await response.json();
            if (data.images && data.images.length > 0) {
                console.log(`[Image API] Success!`);
                return NextResponse.json({
                    image: `data:image/png;base64,${data.images[0]}`
                });
            }
        }

        const errText = await response.text().catch(() => 'unknown');
        console.error(`[Image API] Failed: ${response.status} ${errText}`);
        return NextResponse.json({ error: 'No image generated' }, { status: 500 });

    } catch (error) {
        console.error('[Image API] Error:', error);
        return NextResponse.json({ error: 'Internal Error' }, { status: 500 });
    }
}
