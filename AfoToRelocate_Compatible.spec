# -*- mode: python ; coding: utf-8 -*-

import sys
import os

# Configuración para máxima compatibilidad
block_cipher = None

# Obtener el directorio del proyecto
project_dir = os.path.dirname(os.path.abspath(SPEC))
src_dir = os.path.join(project_dir, 'src')

# Configurar análisis con imports explícitos
a = Analysis(
    [os.path.join(src_dir, 'main.py')],
    pathex=[project_dir],
    binaries=[],
    datas=[
        (src_dir, 'src'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'PIL',
        'PIL.Image',
        'PIL.ExifTags',
        'PIL._tkinter_finder',
        'datetime',
        'os',
        'shutil',
        're',
        'json',
        'typing',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Configurar PYZ
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Configurar EXE con compatibilidad mejorada
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AfoToRelocate_Compatible',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Desactivar UPX para mejor compatibilidad
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin ventana de consola
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Configuraciones adicionales para compatibilidad
    manifest=None,
    version=None,
    uac_admin=False,
    uac_uiaccess=False,
)
