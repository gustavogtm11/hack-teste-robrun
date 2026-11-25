@echo off
setlocal
cd /d "%~dp0"
echo [1/4] Verificando Python...
py -3 --version
if errorlevel 1 (
    echo Python 3 nao encontrado. Instale Python 3.10 ou superior.
    pause
    exit /b 1
)
echo [2/4] Criando ambiente e instalando dependencias...
if not exist .venv py -3 -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Falha ao instalar dependencias.
    pause
    exit /b 1
)
echo [3/4] Gerando Inventory Security Lab...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name RobRunInventoryLab app.py
if errorlevel 1 goto failed
echo [4/4] Gerando Overlay Lab...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name RobRunOverlayLab overlay_lab.py
if errorlevel 1 goto failed
echo.
echo Executaveis criados:
echo dist\RobRunInventoryLab.exe
echo dist\RobRunOverlayLab.exe
pause
exit /b 0
:failed
echo Falha na compilacao. Consulte as mensagens acima.
pause
exit /b 1
