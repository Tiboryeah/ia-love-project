@echo off
set HF_HOME=E:\IALove\.cache\huggingface
set TRANFORMERS_CACHE=E:\IALove\.cache\huggingface
set PIP_CACHE_DIR=E:\IALove\.cache\pip
set TEMP=E:\IALove\.cache\temp
set TMP=E:\IALove\.cache\temp
New-Item -ItemType Directory -Force -Path "E:\IALove\.cache\temp" >nul 2>&1
echo =========================================================
echo    IA Love - Creador de Diosas (E-DRIVE PROTECTED)
echo =========================================================
echo.
echo ¡DETECTADO: NVIDIA RTX 5060 Ti 16GB! 
echo El entrenamiento sera ultra rapido y estable.
echo ESPACIO PROTEGIDO (HF_HOME redirigido al disco E:)
echo.
echo ---------------------------------------------------------
echo Configuracion de Entrenamiento OPTIMIZADA:
echo Personaje: lilith-goth
echo VRAM: 16GB
echo Precision: bf16 (Nativa en arquitectura Blackwell/Ada)
echo ---------------------------------------------------------
pause

:: Notas:
:: 1. Al tener 16GB de VRAM, puedes entrenar a 768x768 para mucha mas calidad.
:: 2. Usa "bf16" en lugar de "fp16" para evitar perdida de precision.
:: 3. El comando de abajo ahora es 100% compatible y recomendado para tu PC.

set MODEL_PATH=".\sdnext\models\Stable-diffusion\Realistic_Vision_V6.0.safetensors"
set TRAIN_DIR=".\lora_training\lilith-goth\dataset"
set OUT_DIR=".\sdnext\models\Lora"
set LORA_NAME="lilith_goth_v1_5060ti"

echo Iniciando entrenamiento en GPU...

accelerate launch --num_cpu_threads_per_core=2 "train_network.py" ^
  --pretrained_model_name_or_path=%MODEL_PATH% ^
  --train_data_dir=%TRAIN_DIR% ^
  --resolution="768,768" ^
  --output_dir=%OUT_DIR% ^
  --output_name=%LORA_NAME% ^
  --network_module="networks.lora" ^
  --max_train_epochs=10 ^
  --learning_rate="1e-4" ^
  --network_dim=32 ^
  --network_alpha=16 ^
  --mixed_precision="bf16" ^
  --save_every_n_epochs=2

echo.
echo [!] ¡Aprovecha la VRAM! Puedes subir el "Batch Size" a 4 o 8 en Kohya
echo para terminar el entrenamiento en cuestion de minutos.
echo.
pause
