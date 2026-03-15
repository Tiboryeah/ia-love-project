@echo off
echo ============================================
echo  IALove - SD.Next (CPU Mode)
echo ============================================
echo.
echo NOTA: DirectML con SD1.5 produce imagenes negras (bug conocido)
echo Usando GPU (DirectML) para maxima velocidad y calidad.
echo Tiempo estimado: ~25-40 segundos por imagen (20 pasos)
echo.
cd /d "%~dp0sdnext"
.\venv\Scripts\python.exe launch.py --api --use-cpu all --port 7860 --use-openvino
pause
