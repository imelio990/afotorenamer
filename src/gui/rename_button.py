import os
import tkinter as tk
import datetime
from PIL import Image, ExifTags

class RenameButton(tk.Button):
    def __init__(self, master, listbox_widget, get_directory_func, log_func, **kwargs):
        super().__init__(master, text="Rename", command=self.show_image_stats, **kwargs)
        self.listbox_widget = listbox_widget
        self.get_directory = get_directory_func
        self.log_func = log_func

    def show_image_stats(self):
        directory = self.get_directory()
        if not directory:
            self.log_func("No hay directorio seleccionado.")
            return
        # Para Treeview, obtener los nombres de archivo de la primera columna:
        files = [self.listbox_widget.tree.item(iid)['values'][0] for iid in self.listbox_widget.tree.get_children()]
        if not files:
            self.log_func("No hay imágenes en el directorio.")
            return
        for fname in files:
            fpath = os.path.join(directory, fname)
            try:
                size = os.path.getsize(fpath)
                ctime = datetime.datetime.fromtimestamp(os.path.getctime(fpath)).strftime('%Y-%m-%d %H:%M:%S')
                mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fpath)).strftime('%Y-%m-%d %H:%M:%S')
                msg = f"{fname} | {size} bytes | Creado: {ctime} | Modificado: {mtime}"
                self.log_func(msg)
                # Mostrar EXIF si es imagen compatible
                exif_info = self.get_exif_info(fpath)
                if exif_info:
                    for k, v in exif_info.items():
                        self.log_func(f"    {k}: {v}")
                else:
                    self.log_func("    Sin información EXIF.")
            except Exception as e:
                self.log_func(f"Error con {fname}: {e}")

    def get_exif_info(self, fpath):
        try:
            image = Image.open(fpath)
            exif_data = image._getexif()
            if not exif_data:
                return None
            exif = {}
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                exif[tag_name] = value
            return exif
        except Exception:
            return None