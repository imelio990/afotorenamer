@echo off
echo ================================================
echo    Creando ejecutables de AfoToRelocate
echo ================================================
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

echo Limpiando archivos anteriores...
if exist "dist\AfoToRelocate*.exe" del "dist\AfoToRelocate*.exe"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"

echo.
echo ================================================
echo 1/3 Creando version ESTANDAR (sin consola)
echo ================================================
python -m PyInstaller --onefile --windowed --name=AfoToRelocate --add-data "src;src" --hidden-import=PIL._tkinter_finder --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.filedialog --hidden-import=tkinter.messagebox --distpath=dist --workpath=build --specpath=. src/main.py

echo.
echo ================================================
echo 2/3 Creando version COMPATIBLE (maxima compatibilidad)
echo ================================================
python -m PyInstaller --onefile --windowed --name=AfoToRelocate_Compatible --add-data "src;src" --hidden-import=PIL._tkinter_finder --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.filedialog --hidden-import=tkinter.messagebox --noupx --distpath=dist --workpath=build_compat --specpath=. src/main.py

echo.
echo ================================================
echo 3/3 Creando version DEBUG (con consola)
echo ================================================
python -m PyInstaller --onefile --console --name=AfoToRelocate_Debug --add-data "src;src" --hidden-import=PIL._tkinter_finder --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.filedialog --hidden-import=tkinter.messagebox --noupx --distpath=dist --workpath=build_debug --specpath=. src/main.py

echo.
echo ================================================
echo           RESUMEN DE EJECUTABLES CREADOS
echo ================================================
if exist "dist\AfoToRelocate.exe" (
    echo ✓ AfoToRelocate.exe - Version estandar
    for %%A in (dist\AfoToRelocate.exe) do echo   Tamaño: %%~zA bytes
) else (
    echo ✗ AfoToRelocate.exe - ERROR
)

if exist "dist\AfoToRelocate_Compatible.exe" (
    echo ✓ AfoToRelocate_Compatible.exe - Maxima compatibilidad  
    for %%A in (dist\AfoToRelocate_Compatible.exe) do echo   Tamaño: %%~zA bytes
) else (
    echo ✗ AfoToRelocate_Compatible.exe - ERROR
)

if exist "dist\AfoToRelocate_Debug.exe" (
    echo ✓ AfoToRelocate_Debug.exe - Version debug con consola
    for %%A in (dist\AfoToRelocate_Debug.exe) do echo   Tamaño: %%~zA bytes
) else (
    echo ✗ AfoToRelocate_Debug.exe - ERROR
)

echo.
echo ================================================
echo                INSTRUCCIONES DE USO
echo ================================================
echo.
echo Si tienes problemas de compatibilidad, prueba en este orden:
echo.
echo 1. AfoToRelocate_Debug.exe
echo    - Muestra mensajes de error en consola
echo    - Mejor para diagnosticar problemas
echo.
echo 2. AfoToRelocate_Compatible.exe  
echo    - Optimizado para maxima compatibilidad
echo    - Sin compresion UPX
echo.
echo 3. AfoToRelocate.exe
echo    - Version mas limpia y compacta
echo    - Mejor si funciona en tu sistema
echo.
echo Ver TROUBLESHOOTING.md para mas detalles
echo.

echo Presiona cualquier tecla para continuar...
pause >nul
