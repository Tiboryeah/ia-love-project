@echo off
echo =========================================================
echo    IA Love - Creador de Diosas (Entrenamiento LoRA)
echo =========================================================
echo.
echo Este script iniciara el entrenamiento profundo de la red neuronal
echo para grabar permanentemente el rostro y cuerpo de tu personaje.
echo.
echo ADVERTENCIA PARA HARDWARE AMD:
echo Entrenar un modelo de IA requiere muchisima memoria de video (VRAM).
echo Si el proceso falla por "Out of Memory", deberas reducir la
echo resolucion de las imagenes o subir este dataset a Google Colab/RunPod.
echo.
echo ---------------------------------------------------------
echo Configuracion de Entrenamiento:
echo Personaje: sweet-coco
echo Carpeta de Imagenes: .\lora_training\sweet-coco\images
echo Repeticiones por imagen: 100
echo Epocas (Epochs): 10
echo Pasos totales aprox: 15,000
echo Modelo Base: Realistic Vision V6.0
echo ---------------------------------------------------------
pause

:: Notas:
:: 1. Necesitas instalar Kohya_ss o usar un script de diffusers para que esto funcione nativamente.
:: 2. Tu PC usa AMD, el entrenamiento en DirectML (Windows) es posible pero inestable.
:: 3. A continuacion se muestra el comando profesional estandar (sd-scripts) asumiendo
::    que tienes el entorno de entrenamiento configurado. Si no lo tienes,
::    este archivo te servira de puente para llevar la carpeta "lora_training" a la nube.

set MODEL_PATH=".\sdnext\models\Stable-diffusion\Realistic_Vision_V6.0.safetensors"
set TRAIN_DIR=".\lora_training\sweet-coco\images"
set OUT_DIR=".\sdnext\models\Lora"
set LORA_NAME="sweet_coco_v1"

echo Iniciando proceso (Simulacion o enlace a Kohya)...
:: Si tuvieras sd-scripts aqui, el comando seria algo asi:
:: accelerate launch --num_cpu_threads_per_core=2 "train_network.py" ^
::   --pretrained_model_name_or_path=%MODEL_PATH% ^
::   --train_data_dir=%TRAIN_DIR% ^
::   --resolution="512,512" ^
::   --output_dir=%OUT_DIR% ^
::   --output_name=%LORA_NAME% ^
::   --network_module="networks.lora" ^
::   --max_train_epochs=10 ^
::   --learning_rate="1e-4" ^
::   --network_dim=32 ^
::   --network_alpha=16 ^
::   --mixed_precision="fp16" ^
::   --save_every_n_epochs=2

echo.
echo [!] Para entrenar seriamente en AMD, recomendamos usar la interfaz web de SD.Next
echo ve a la pestana "Entrenamiento" y selecciona la carpeta de imagenes que generamos.
echo O sube la carpeta 'lora_training' a un servicio en la nube especializado como Civitai.
echo.
pause
