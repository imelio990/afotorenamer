@echo off
echo ================================================
echo    Creando ejecutable de AfoToRelocate
echo ================================================
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

REM Crear el ejecutable con PyInstaller
python -m PyInstaller --onefile --windowed --name=AfoToRelocate --add-data "src;src" --hidden-import=PIL._tkinter_finder --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.filedialog --hidden-import=tkinter.messagebox --distpath=dist --workpath=build --specpath=. src/main.py

echo.
if exist "dist\AfoToRelocate.exe" (
    echo ✓ Ejecutable creado exitosamente!
    echo Ubicacion: %cd%\dist\AfoToRelocate.exe
    echo.
    echo Tamaño del archivo:
    for %%A in (dist\AfoToRelocate.exe) do echo   %%~zA bytes
    echo.
) else (
    echo ✗ Error: No se pudo crear el ejecutable
)

echo.
echo Presiona cualquier tecla para continuar...
pause >nul
