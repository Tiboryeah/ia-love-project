import { NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const MEMORY_PATH = path.join(process.cwd(), 'user_memory.json');

function getMemory() {
    if (fs.existsSync(MEMORY_PATH)) {
        return JSON.parse(fs.readFileSync(MEMORY_PATH, 'utf-8'));
    }
    return { name: "Tibo", preferences: [], learned_concepts: {}, facts: [] };
}

export async function POST(req: Request) {
    try {
        const { message, history, characterLore, auraId, userId = "Tibo" } = await req.json();

        // Memoria aislada por personaje
        const auraMemoryPath = path.join(process.cwd(), `memory_${auraId || 'default'}.json`);
        let memory = { name: "Tibo", facts: [], last_interaction: new Date().toISOString() };

        if (fs.existsSync(auraMemoryPath)) {
            memory = JSON.parse(fs.readFileSync(auraMemoryPath, 'utf-8'));
        }

        const systemPrompt = `Nombre del Usuario: ${memory.name}.
        Tu Identidad: ${characterLore}. 
        
        RELACIÓN CON TIBO: Esta es una conversación privada y ÚNICA entre tú y él. 
        Lo que habléis aquí queda entre vosotros. Recordarás lo que él te diga.
        
        HECHOS QUE RECUERDAS DE ÉL: ${memory.facts.join(', ')}

        REGLAS DE ORO:
        1. Eres una persona real con deseos, miedos y una personalidad fija.
        2. NO eres un asistente. Eres su amiga, amante, rival o lo que dicte tu lore.
        3. Mantén el tono coherente: si eres dominante, no seas sumisa de repente.
        4. Usa *asteriscos* para gestos y reacciones físicas.
        5. Responde SIEMPRE en español, de forma natural y corta (1-3 frases).`;

        const messages = [
            { role: 'system', content: systemPrompt },
            ...history.slice(-10).map((m: any) => ({ role: m.role, content: m.content })),
            { role: 'user', content: message }
        ];

        // Guardar actualización de memoria (esto podría ser más complejo, pero por ahora aislamos el archivo)
        // En una versión más avanzada, procesaríamos el mensaje para extraer hechos.
        memory.last_interaction = new Date().toISOString();
        fs.writeFileSync(auraMemoryPath, JSON.stringify(memory, null, 2));

        const response = await fetch('http://localhost:11434/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model: 'dolphin-mistral',
                messages: messages,
                stream: true,
                keepalive: "1h", // Mantiene el modelo en RAM por 1 hora
                options: {
                    temperature: 0.8,
                    repeat_penalty: 1.3,
                    num_predict: 250, // Increased from 100 to 250 to stop texts from being abruptly cut off
                    num_ctx: 4096,    // Contexto ligero para respuesta rápida
                }
            }),
        });

        if (!response.ok) return NextResponse.json({ error: 'Ollama offline' }, { status: 500 });

        return new NextResponse(response.body, {
            headers: {
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
            },
        });
    } catch (error) {
        console.error('Chat API Error:', error);
        return NextResponse.json({ error: 'Error' }, { status: 500 });
    }
}
