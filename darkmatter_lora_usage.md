# Darkmatter LoRA - Guía de Uso y Configuración

## 1. Instalación del Modelo
- **Archivo Principal:** `darkmatter.safetensors` (Este es el archivo final equivalente a la Época 10, y contiene la versión más pulida de la IA).
- **¿Dónde ponerlo?:** Descárgalo de tu Google Drive y muévelo a la carpeta `models\Lora\` dentro de la carpeta principal de tu SD.Next u otra interfaz.

## 2. Cómo Activarlo
Al escribir tu Prompt, es obligatorio usar las llaves para que la IA despierte el concepto:
- **Palabra clave (Trigger Word):** `darkmatter`
- **Llamador del LoRA:** `<lora:darkmatter:1>` (El `1` denota el 100% de fuerza. Si el efecto es demasiado rígido, se puede intentar con `<lora:darkmatter:0.8>` o `<lora:darkmatter:0.6>`).

## 3. Mejores Configuraciones (Recomendado)
- **Modelo Base (Checkpoint):** Entrenamos el LoRA utilizando *Realistic Vision V5.1*. Para resultados increíblemente fotorrealistas e idénticos al entrenamiento, usa ese mismo Checkpoint o uno altamente realista. Si buscas un estilo anime/dibujo, puedes probar con *AnyLoRA* u otro similar.
- **Sampler Sugerido:** `DDIM` o `Euler a` (Ambos son clásicos muy nobles para LoRAs nuevos).
- **Clip Skip:** `2` (Fue el valor exacto usado en el script de entrenamiento de Kohya).
- **Resolución óptima:** `512 x 512` o `512 x 768` (proporción vertical). Se recomienda usar Hires.fix para hacerlo más nítido o subirlo a resoluciones de 1024.

## 4. Prompt de Ejemplo para Mañana
**Prompt:**
`masterpiece, best quality, ultra detailed, extremely detailed photo of darkmatter, wearing her black latex bodysuit, looking at viewer, professional lighting, 8k resolution, <lora:darkmatter:1>`

**Prompt Negativo:**
`lowres, bad anatomy, bad hands, bad face, text, error, missing fingers, extra digit, cropped, worst quality, low quality, normal quality, jpeg artifacts, watermark, blurry`
