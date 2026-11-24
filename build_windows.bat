@echo off
setlocal
cd /d "%~dp0"

echo [1/3] Verificando Python...
py -3 --version
if errorlevel 1 (
    echo Python 3 nao encontrado. Instale Python 3.10 ou superior.
    pause
    exit /b 1
)

echo [2/3] Criando ambiente e instalando dependencias...
if not exist .venv py -3 -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Falha ao instalar dependencias.
    pause
    exit /b 1
)

echo [3/3] Gerando executavel...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name RobRunInventoryLab app.py
if errorlevel 1 (
    echo Falha na compilacao.
    pause
    exit /b 1
)

echo.
echo Executavel criado em: dist\RobRunInventoryLab.exe
pause
