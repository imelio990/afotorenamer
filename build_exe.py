#!/usr/bin/env python
"""
Script para crear el ejecutable de AfoToRelocate
"""
import os
import sys
import subprocess

def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    
    # Directorio del proyecto
    project_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(project_dir, 'src')
    main_script = os.path.join(src_dir, 'main.py')
    
    # Comando PyInstaller
    pyinstaller_cmd = [
        'pyinstaller',
        '--onefile',              # Un solo archivo ejecutable
        '--windowed',             # Sin ventana de consola
        '--name=AfoToRelocate',   # Nombre del ejecutable
        '--icon=icon.ico',        # Icono (si existe)
        '--add-data', f'{src_dir};src',  # Incluir directorio src
        '--hidden-import=PIL._tkinter_finder',  # Importaciones ocultas para PIL
        '--hidden-import=tkinter',
        '--hidden-import=tkinter.ttk',
        '--hidden-import=tkinter.filedialog',
        '--hidden-import=tkinter.messagebox',
        '--distpath=dist',        # Directorio de salida
        '--workpath=build',       # Directorio de trabajo
        '--specpath=.',           # Donde guardar el .spec
        main_script
    ]
    
    print("Construyendo ejecutable...")
    print(f"Comando: {' '.join(pyinstaller_cmd)}")
    
    try:
        # Ejecutar PyInstaller
        result = subprocess.run(pyinstaller_cmd, cwd=project_dir, check=True, 
                              capture_output=True, text=True)
        print("✓ Ejecutable creado exitosamente!")
        print(f"Ubicación: {os.path.join(project_dir, 'dist', 'AfoToRelocate.exe')}")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error al crear el ejecutable:")
        print(f"Código de salida: {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False
    
    return True

if __name__ == "__main__":
    success = build_executable()
    if success:
        print("\n🎉 ¡Ejecutable listo para usar!")
        print("Puedes encontrarlo en la carpeta 'dist/AfoToRelocate.exe'")
    else:
        print("\n❌ Falló la creación del ejecutable")
        sys.exit(1)
