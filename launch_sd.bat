@echo off
echo ============================================
echo  IALove - SD.Next (NVIDIA GPU Mode)
echo ============================================
echo.
echo Usando NVIDIA RTX 5060 Ti 16GB para maxima velocidad!
echo Tiempo estimado: ~2-5 segundos por imagen (SD 1.5)
echo.
cd /d "%~dp0sdnext"
.\venv\Scripts\python.exe launch.py --api --theme dark --port 7860
pause
