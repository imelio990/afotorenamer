
# afotorelocate: Organizador y Renombrador de Fotos y Videos

Este proyecto es una aplicación gráfica para organizar, visualizar y renombrar archivos de imagen y video en tu equipo. Utiliza la biblioteca `tkinter` para la interfaz y permite automatizar el proceso de clasificación y renombrado de archivos multimedia según sus fechas y metadatos.

Visualiza la estructura de carpetas en tu equipo mediante un panel tipo árbol (Treeview).
Para imágenes, extrae fechas de captura, digitalización y otros datos EXIF relevantes. Para videos, usa fechas de archivo.

Renombra archivos para evitar duplicados y mejorar la organización: renombra los archivos colocando la fecha al inicio del nombre, eliminando cualquier fecha previa y opcionalmente añadiendo el modelo de cámara.
Agrupa automáticamente archivos en carpetas mensuales: mueve los archivos a subdirectorios de mes (formato `yyyy_mm`) dentro del directorio elegido, agrupando automáticamente por fecha.

El botón "Scan" busca recursivamente todos los archivos válidos en los subdirectorios y los muestra en la lista para su procesamiento.




## Project Structure

```
python-treeview-imageviewer
├── src
│   ├── main.py          # Entry point of the application
│   ├── gui
│   │   ├── treeview.py  # Contains DirectoryTreeView class for directory navigation
│   │   └── listbox.py   # Contains ImageListBox class for displaying image files
│   └── utils
│       └── file_utils.py # Utility functions for file operations
├── requirements.txt      # Lists the dependencies required for the project
└── README.md             # Documentation for the project
```

## Setup Instructions

1. Clone the repository or download the project files.
2. Navigate to the project directory.
3. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application by executing the following command:
   ```
   python src/main.py
   ```
2. The main window will open, displaying a Treeview on the left side for directory navigation and a Listbox on the right side for viewing image files.
3. Click on a directory in the Treeview to load and display the image files in the Listbox.

## Dependencies

- `tkinter`: For creating the GUI.
- Additional libraries may be included in `requirements.txt` for image handling.

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or features you would like to add.