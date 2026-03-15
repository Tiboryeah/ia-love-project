import { NextResponse } from 'next/server';

export async function POST(req: Request) {
    try {
        const { prompt, characterDescription } = await req.json();

        // Construimos un prompt potente y sin filtros
        // Usamos etiquetas de calidad típicas de la comunidad de SD
        const fullPrompt = `(photorealistic:1.3), (highly detailed skin:1.2), 8k, masterwork, ${characterDescription}, ${prompt}, masterpiece, cinematic lighting, (NSFW:1.2)`;
        const negativePrompt = "cartoon, drawing, anime, low quality, deformed, (extra fingers:1.2), (bad anatomy:1.2), text, watermark, filters, censored";

        // Intentamos conectar con la interfaz de Stable Diffusion (Automatic1111 / SD.Next)
        // El usuario debe tener activada la opción "--api" en su lanzador de SD
        const response = await fetch('http://127.0.0.1:7860/sdapi/v1/txt2img', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                prompt: fullPrompt,
                negative_prompt: negativePrompt,
                steps: 25,
                width: 512,
                height: 768,
                cfg_scale: 7,
                sampler_name: "Euler a",
            }),
        });

        if (!response.ok) {
            return NextResponse.json({
                error: "Stable Diffusion no está respondiendo. ¿Has activado el modo API?"
            });
        }

        const data = await response.json();

        // Devolvemos la imagen en base64
        return NextResponse.json({ image: data.images[0] });

    } catch (error) {
        console.error('Image API Error:', error);
        return NextResponse.json({ error: 'Error generando la imagen' }, { status: 500 });
    }
}
