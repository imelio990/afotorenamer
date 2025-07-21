import os
import tkinter as tk
from gui.treeview import DirectoryTreeView
from gui.listbox import ImageListBox
from gui.rename_button import RenameButton
from utils.file_utils import get_image_file_info, mover_archivo
from utils.image_types import ImageFileInfo
from utils.logger import log_to_listbox
from typing import List, Optional

class MainApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Directory and Image Viewer")

        # Usa PanedWindow para permitir redimensionar los paneles principales
        self.main_paned = tk.PanedWindow(self.root, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self.main_paned.pack(fill=tk.BOTH, expand=True)

        # Panel superior: Treeview y panel derecho
        self.top_paned = tk.PanedWindow(self.main_paned, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        self.main_paned.add(self.top_paned, stretch='always')

        # Treeview de directorios
        self.treeview = DirectoryTreeView(self.top_paned, log_func=self.log_message)
        self.top_paned.add(self.treeview, minsize=150, stretch='always')

        # Frame para Listbox de imágenes y botón
        self.right_frame = tk.Frame(self.top_paned)
        self.top_paned.add(self.right_frame, minsize=200, stretch='always')

        # Panel de comandos encima del listbox de imágenes
        self.command_frame = tk.Frame(self.right_frame)
        self.command_frame.pack(side=tk.TOP, fill=tk.X)

        # Listbox de imágenes debajo del panel de comandos
        self.listbox = ImageListBox(self.right_frame)
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Botón Scan (a la izquierda de Rename) en el panel de comandos
        self.scan_button = tk.Button(
            self.command_frame,
            text="Scan",
            command=self.scan_exif_dates
        )
        self.scan_button.pack(side=tk.LEFT, padx=4, pady=2)

        # Elimina el botón Rename
        # self.rename_button = RenameButton(
        #     self.command_frame,
        #     self.listbox,
        #     lambda: self.current_directory,
        #     self.log_message
        # )
        # self.rename_button.pack(side=tk.LEFT, padx=4, pady=2)

        # Botón Renombrar (a la derecha de Scan) en el panel de comandos
        self.move_button = tk.Button(
            self.command_frame,
            text="Renombrar",
            command=self.renombrar_archivos
        )
        self.move_button.pack(side=tk.LEFT, padx=4, pady=2)

        # Elimina el botón para restaurar la última ruta seleccionada
        # self.restore_button = tk.Button(
        #     self.command_frame,
        #     text="Restaurar última ruta",
        #     command=self.defer_restore_last_path
        # )
        # self.restore_button.pack(side=tk.LEFT, padx=4, pady=2)

        # Log redimensionable en la parte inferior con scrollbar
        self.log_frame = tk.Frame(self.main_paned)
        self.log_listbox = tk.Listbox(self.log_frame)
        self.log_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_scroll = tk.Scrollbar(self.log_frame, orient=tk.VERTICAL, command=self.log_listbox.yview)
        self.log_listbox.config(yscrollcommand=self.log_scroll.set)
        self.log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_paned.add(self.log_frame, minsize=40, stretch='always')

        # El bind debe ser sobre el widget tree, no sobre self.treeview
        self.treeview.tree.bind("<<TreeviewSelect>>", self.on_directory_select)

        # Guarda el último directorio mostrado en el listbox
        self.current_directory = None

        # Bind para acción automática al hacer doble click en un archivo de la lista de imágenes
        self.listbox.tree.bind("<Double-1>", self.on_image_double_click)

    def on_directory_select(self, event):
        selected_item = self.treeview.tree.selection()
        if selected_item:
            directory = self.treeview.tree.set(selected_item[0], 'fullpath')
            self.current_directory = directory
            self.listbox.update_listbox(directory)
            self.log_message(f"Directorio seleccionado: {directory}")

    def log_message(self, message: str):
        log_to_listbox(self.log_listbox, message)

    def scan_exif_dates(self):
        directory = self.current_directory
        if not directory:
            self.log_message("No hay directorio seleccionado.")
            return
        items = self.listbox.tree.get_children()
        for iid in items:
            values = list(self.listbox.tree.item(iid)['values'])
            fname = values[0]
            info = get_image_file_info(directory, fname)
            if info:
                values[4] = info.exif_datetime_original or ''
                values[5] = info.exif_datetime_digitized or ''
                values[6] = info.exif_datetime or ''
                values[7] = info.subdir or ''
                values[8] = info.nuevo_nombre or ''
                self.listbox.tree.item(iid, values=values)
            else:
                self.log_message(f"Error EXIF en {fname}")
        self.log_message("Scan EXIF completado.")

    def renombrar_archivos(self):
        directory = self.current_directory
        if not directory:
            self.log_message("No hay directorio seleccionado.")
            return
        selected = self.listbox.tree.selection()
        if not selected:
            self.log_message("No hay archivos seleccionados.")
            return
        for iid in selected:
            values = list(self.listbox.tree.item(iid)['values'])
            fname = values[0]
            info = get_image_file_info(directory, fname)
            if info:
                mover_archivo(info, directory, self.log_message)
            else:
                self.log_message(f"Faltan datos para {fname}, omitiendo.")
        self.log_message("Renombrado finalizado.")

    def on_image_double_click(self, event):
        # Muestra toda la info EXIF disponible del archivo sobre el que se hace doble click
        item = self.listbox.tree.identify_row(event.y)
        if not item:
            return
        directory = self.current_directory
        if not directory:
            self.log_message("No hay directorio seleccionado.")
            return
        values = list(self.listbox.tree.item(item)['values'])
        fname = values[0]
        fpath = os.path.join(directory, fname)
        try:
            from PIL import Image, ExifTags
            image = Image.open(fpath)
            exif_data = image._getexif()
            if not exif_data:
                self.log_message(f"No EXIF en {fname}")
                return
            exif_info = []
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                exif_info.append(f"{tag_name}: {value}")
            # Muestra la info EXIF en un popup
            self.show_exif_popup(fname, exif_info)
        except Exception as e:
            self.log_message(f"Error leyendo EXIF de {fname}: {e}")

    def show_exif_popup(self, fname, exif_info):
        # Muestra la info EXIF en una ventana emergente
        popup = tk.Toplevel(self.root)
        popup.title(f"EXIF de {fname}")
        text = tk.Text(popup, wrap=tk.WORD, width=80, height=30)
        text.pack(fill=tk.BOTH, expand=True)
        text.insert(tk.END, "\n".join(exif_info))
        text.config(state=tk.DISABLED)
        btn = tk.Button(popup, text="Cerrar", command=popup.destroy)
        btn.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()