# IA Love - Virtual Girlfriend (Stable Diffusion Integration)

Este es el código fuente del proyecto **IA Love**, una plataforma de novias virtuales impulsada por Inteligencia Artificial, que incluye la generación de imágenes en tiempo real mediante *Stable Diffusion* (SD.Next) y la opción de entrenar *LoRAs* personalizados.

## 🚀 Requisitos Previos (Para tu amigo)

Para que el proyecto funcione en otra computadora, especialmente la generación de imágenes, necesitas lo siguiente:

1.  **Node.js:** Versión 18 o superior (para correr la página web en Next.js).
2.  **Python 3.10 o 3.11:** Requerido para instalar y ejecutar SD.Next.
3.  **Git:** Para descargar repositorios.
4.  *(Opcional pero muy recomendado)* Una tarjeta de video dedicada (Nvidia RTX o AMD moderna). Aunque el proyecto está configurado actualmente para correr en procesador (CPU), es extremadamente lento (10-15 min por foto) en comparación a usar una tarjeta de video (10-20 segundos).

---

## 🛠️ Instalación Paso a Paso

### Paso 1: Descargar el Servidor de Imágenes (SD.Next)
El repositorio no incluye la instalación completa de SD.Next (porque pesa varios GBs). Debes instalarlo dentro de la carpeta del proyecto.

1. Abre una terminal (PowerShell o CMD) en la carpeta raíz de este proyecto (`IALove`).
2. Clona el repositorio de SD.Next oficial:
   ```bash
   git clone https://github.com/vladmandic/automatic sdnext
   ```
3. Entra en la carpeta `sdnext` y ejecuta el instalador. Sigue las instrucciones en pantalla para descargar los componentes básicos.
   ```bash
   cd sdnext
   webui.bat
   ```

### Paso 2: Descargar el Modelo Base
El cerebro que dibuja las imágenes no viene incluido. Debes descargar **Realistic Vision V6.0**.
1. Descarga el modelo `Realistic_Vision_V6.0.safetensors` desde Civitai o HuggingFace.
2. Coloca ese archivo dentro de la carpeta: `\sdnext\models\Stable-diffusion\`

### Paso 3: Colocar los LoRAs (Tus personajes)
Para que personajes como *Darkmatter* o *Morgana* funcionen, necesitan sus "filtros de identidad" (los archivos `.safetensors`).
1. Toma los archivos de tus modelos entrenados (ej. `darkmatter.safetensors`).
2. Ponlos dentro de la carpeta: `\sdnext\models\Lora\`

### Paso 4: Instalar las dependencias de la Página Web
Abre una terminal nueva en la raíz del proyecto (`IALove`) e instala las librerías de Node:
```bash
npm install
```

---

## 🎮 Cómo Arrancar el Proyecto

Para usar la aplicación, necesitas arrancar ambos servidores a la vez.

### 1. Iniciar el Motor de IA (SD.Next)
Puedes usar el script que dejamos preparado (`launch_sd.bat`) o ejecutar manualmente el comando. Note que *actualmente está configurado para forzar CPU*.

Ejecuta desde la raíz del proyecto:
```bash
.\launch_sd.bat
```
*(Si tu amigo tiene una tarjeta de video Nvidia, él debería editar este archivo y quitar `--use-cpu all` y `--use-openvino`, y en su lugar poner `--use-cuda`).*

Espera a que la consola diga algo como: `Startup time...` y `Local URL: http://127.0.0.1:7860`.

### 2. Iniciar la Interfaz Web
En otra terminal, corre la página web de Next.js:
```bash
npm run dev
```

Abre tu navegador en `http://localhost:3000`. ¡Listo! Al chatear y pedir fotos, la web se comunicará en secreto con SD.Next para generar las imágenes.

---

## 📁 Estructura del Proyecto (Scripts Importantes)

Para pruebas directas de generación (sin usar la web), tienes estos scripts listos:

*   **`gen_darkmatter.py` / `gen_morgana.py`:** Pruebas SFW de cada personaje.
*   **`gen_nsfw_morgana.py` / `gen_nsfw_raven.py`:** Pruebas directas de anatomía NSFW usando configuraciones avanzadas.
*   **`generate_dataset.py` & `generate_nsfw_dataset.py`:** Estos son los scripts mágicos que usamos para "crear desde cero" el dataset de *Sweet Coco* generando 30 imágenes base de forma automatizada.
*   **`train_models.bat`:** Una plantilla que explica cómo invocar el entrenamiento LoRA una vez tienes las imágenes listas.
