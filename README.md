
# afotorelocate: Organizador y Renombrador de Fotos y Videos

Este proyecto es una aplicación gráfica para organizar, visualizar y renombrar archivos de imagen y video en tu equipo. Utiliza la biblioteca `tkinter` para la interfaz y permite automatizar el proceso de clasificación y renombrado de archivos multimedia según sus fechas y metadatos.

## ✨ Características principales

- **Navegación visual**: Visualiza la estructura de carpetas en tu equipo mediante un panel tipo árbol (Treeview)
- **Extracción de metadatos**: Para imágenes, extrae fechas de captura, digitalización y otros datos EXIF relevantes. Para videos, usa fechas de archivo
- **Renombrado inteligente**: Renombra archivos colocando la fecha al inicio del nombre, eliminando cualquier fecha previa y opcionalmente añadiendo el modelo de cámara
- **Organización automática**: Mueve los archivos a subdirectorios de mes (formato `yyyy_mm`) dentro del directorio elegido, agrupando automáticamente por fecha
- **Búsqueda recursiva**: El botón "Scan" busca recursivamente todos los archivos válidos en los subdirectorios y los muestra en la lista para su procesamiento
- **Soporte multimedia**: Compatible con imágenes (.jpg, .png, .tiff, .bmp, .gif, .webp) y videos (.mp4, .avi, .mov, .mkv, .wmv, .flv, .webm)
- **Interfaz intuitiva**: Navegación con teclado (Home, End, Page Up/Down), scrollbars automáticos y cursor de progreso

## 🚀 Opciones de uso

### Opción 1: Ejecutable (Recomendado)
Descarga el ejecutable `AfoToRelocate.exe` desde la carpeta `dist/` y ejecútalo directamente. No requiere instalación de Python.

### Opción 2: Desde código fuente




### Opción 2: Desde código fuente

#### Requisitos previos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

#### Instalación
1. Clona el repositorio o descarga los archivos del proyecto
2. Navega al directorio del proyecto
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

#### Ejecución
```bash
python src/main.py
```

## 🛠️ Crear tu propio ejecutable

Si quieres crear una nueva versión del ejecutable:

### Método 1: Script automatizado (Windows)
```bash
crear_ejecutable.bat
```

### Método 2: Comando manual
```bash
python -m PyInstaller --onefile --windowed --name=AfoToRelocate --add-data "src;src" --hidden-import=PIL._tkinter_finder --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=tkinter.filedialog --hidden-import=tkinter.messagebox --distpath=dist --workpath=build --specpath=. src/main.py
```

## 📁 Estructura del proyecto

```
afotorelocate/
├── src/
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── gui/
│   │   ├── treeview.py      # Navegación de directorios (DirectoryTreeView)
│   │   ├── listbox.py       # Lista de archivos multimedia (ImageListBox)  
│   │   ├── rename_button.py # Botón de renombrado
│   │   └── ui_helpers.py    # Funciones auxiliares de interfaz
│   └── utils/
│       ├── file_utils.py    # Operaciones de archivos y EXIF
│       ├── image_types.py   # Tipos de datos para metadatos
│       ├── logger.py        # Sistema de logging
│       └── config.py        # Gestión de configuración
├── dist/
│   └── AfoToRelocate.exe    # Ejecutable compilado
├── requirements.txt         # Dependencias del proyecto
├── setup.py                # Script de instalación
├── crear_ejecutable.bat    # Script para crear ejecutable
└── README.md               # Documentación del proyecto
```

## 📖 Instrucciones de uso

1. **Ejecutar la aplicación**: 
   - Ejecutable: Doble clic en `AfoToRelocate.exe`
   - Código fuente: `python src/main.py`

2. **Navegar directorios**: Usa el panel izquierdo (TreeView) para seleccionar una carpeta

3. **Escanear archivos**: Haz clic en "Scan" para buscar archivos multimedia recursivamente

4. **Seleccionar archivos**: Marca los archivos que quieres procesar en la lista del panel derecho

5. **Procesar archivos**: Haz clic en "Renombrar" para mover y renombrar los archivos seleccionados

## ⌨️ Navegación con teclado

- **Home/End**: Ir al primer/último archivo
- **Page Up/Page Down**: Navegación rápida
- **Flechas**: Navegación elemento por elemento
- **Espacio**: Seleccionar/deseleccionar archivo

## 🔧 Dependencias

- `tkinter`: For creating the GUI.
- Additional libraries may be included in `requirements.txt` for image handling.

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or features you would like to add.