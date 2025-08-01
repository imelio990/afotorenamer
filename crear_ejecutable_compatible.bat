@echo off
echo ================================================
echo    Creando ejecutable compatible de AfoToRelocate
echo ================================================
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

echo Limpiando archivos anteriores...
if exist "dist\AfoToRelocate.exe" del "dist\AfoToRelocate.exe"
if exist "build" rmdir /s /q "build"
if exist "AfoToRelocate.spec" del "AfoToRelocate.spec"

echo.
echo Creando ejecutable con maxima compatibilidad...

REM Crear el ejecutable con PyInstaller usando parametros mas compatibles
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name=AfoToRelocate ^
    --add-data "src;src" ^
    --hidden-import=PIL._tkinter_finder ^
    --hidden-import=tkinter ^
    --hidden-import=tkinter.ttk ^
    --hidden-import=tkinter.filedialog ^
    --hidden-import=tkinter.messagebox ^
    --hidden-import=PIL.Image ^
    --hidden-import=PIL.ExifTags ^
    --hidden-import=datetime ^
    --hidden-import=os ^
    --hidden-import=shutil ^
    --hidden-import=re ^
    --hidden-import=json ^
    --distpath=dist ^
    --workpath=build ^
    --specpath=. ^
    --noupx ^
    --console ^
    src/main.py

echo.
if exist "dist\AfoToRelocate.exe" (
    echo ✓ Ejecutable compatible creado exitosamente!
    echo Ubicacion: %cd%\dist\AfoToRelocate.exe
    echo.
    echo Tamaño del archivo:
    for %%A in (dist\AfoToRelocate.exe) do echo   %%~zA bytes
    echo.
    echo NOTA: Esta version incluye ventana de consola para mejor compatibilidad
    echo Si necesitas version sin consola, usa: crear_ejecutable_sin_consola.bat
) else (
    echo ✗ Error: No se pudo crear el ejecutable compatible
)

echo.
echo Presiona cualquier tecla para continuar...
pause >nul
