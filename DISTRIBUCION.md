# Información de Distribución - AfoToRelocate

## 📦 Versión Ejecutable

### Archivo generado
- **Nombre**: `AfoToRelocate.exe`
- **Ubicación**: `dist/AfoToRelocate.exe`
- **Tamaño**: ~18 MB
- **Tipo**: Ejecutable portable de Windows
- **Dependencias**: Ninguna (todo incluido)

### Características del ejecutable
- ✅ **Portable**: No requiere instalación
- ✅ **Independiente**: No necesita Python instalado
- ✅ **Sin ventana de consola**: Interfaz limpia
- ✅ **Todas las dependencias incluidas**: PIL, tkinter, etc.

## 🚀 Formas de distribuir el proyecto

### 1. Ejecutable (Recomendado para usuarios finales)
```bash
# El archivo está listo en:
dist/AfoToRelocate.exe

# Para distribuir:
# - Copia AfoToRelocate.exe donde quieras
# - Ejecuta directamente con doble clic
# - No requiere instalación adicional
```

### 2. Como paquete Python instalable
```bash
# Instalar desde código fuente
pip install -e .

# O crear distribución
python setup.py sdist bdist_wheel
pip install dist/afotorelocate-1.0.0-py3-none-any.whl
```

### 3. Desde código fuente
```bash
# Clonar repositorio
git clone <tu-repo-url>
cd afotorelocate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python src/main.py
```

## 🔧 Regenerar el ejecutable

### Automático (Windows)
```bash
crear_ejecutable.bat
```

### Manual
```bash
python -m PyInstaller --onefile --windowed --name=AfoToRelocate --add-data "src;src" --hidden-import=PIL._tkinter_finder --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.filedialog --hidden-import=tkinter.messagebox --distpath=dist --workpath=build --specpath=. src/main.py
```

### Parámetros PyInstaller explicados
- `--onefile`: Un solo archivo ejecutable
- `--windowed`: Sin ventana de consola
- `--name=AfoToRelocate`: Nombre del ejecutable
- `--add-data "src;src"`: Incluir código fuente
- `--hidden-import=...`: Importaciones que Python no detecta automáticamente
- `--distpath=dist`: Carpeta de salida
- `--workpath=build`: Carpeta temporal de construcción

## 📤 Subir a GitHub

```bash
# Inicializar repositorio
git init
git add .
git commit -m "Initial commit: AfoToRelocate v1.0"

# Conectar con GitHub
git remote add origin https://github.com/tu-usuario/afotorelocate.git
git branch -M main
git push -u origin main

# Para crear un release con el ejecutable
# 1. Ve a GitHub -> Releases -> Create new release
# 2. Sube AfoToRelocate.exe como asset
# 3. Añade notas de la versión
```

## 🏷️ Versiones y releases

### Estructura recomendada de versiones
```
v1.0.0 - Versión inicial
  ├── Navegación de directorios
  ├── Escaneo recursivo
  ├── Renombrado con fechas EXIF
  ├── Organización en carpetas YYYY_MM
  └── Soporte para imágenes y videos

v1.1.0 - Mejoras de interfaz
  ├── Navegación con teclado
  ├── Scrollbars automáticos
  ├── Persistencia de configuración
  └── Mejor manejo de errores
```

## 🎯 Distribución recomendada

**Para usuarios finales**: Usar el ejecutable `AfoToRelocate.exe`
- Fácil de usar
- No requiere conocimientos técnicos
- Una sola descarga

**Para desarrolladores**: Código fuente en GitHub
- Fácil de modificar y extender
- Control de versiones
- Colaboración

**Para administradores de sistema**: Paquete instalable con pip
- Integración con entornos Python existentes
- Gestión de dependencias automática
- Fácil desinstalación
