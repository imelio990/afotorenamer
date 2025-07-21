from tkinter import Frame, BOTH
from tkinter.ttk import Treeview
import os
import datetime

class ImageListBox(Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        columns = (
            "name", "size", "created", "modified",
            "DateTimeOriginal", "DateTimeDigitized", "DateTime",
            "subdirectorio", "nuevo nombre", "modelo"
        )
        self.tree = Treeview(self, columns=columns, show="headings")
        self.tree.heading("name", text="Nombre", command=lambda: self.sort_by_column("name", False))
        self.tree.heading("size", text="Tamaño (bytes)", command=lambda: self.sort_by_column("size", False))
        self.tree.heading("created", text="Creado", command=lambda: self.sort_by_column("created", False))
        self.tree.heading("modified", text="Modificado", command=lambda: self.sort_by_column("modified", False))
        self.tree.heading("DateTimeOriginal", text="DateTimeOriginal", command=lambda: self.sort_by_column("DateTimeOriginal", False))
        self.tree.heading("DateTimeDigitized", text="DateTimeDigitized", command=lambda: self.sort_by_column("DateTimeDigitized", False))
        self.tree.heading("DateTime", text="DateTime", command=lambda: self.sort_by_column("DateTime", False))
        self.tree.heading("subdirectorio", text="Subdirectorio", command=lambda: self.sort_by_column("subdirectorio", False))
        self.tree.heading("nuevo nombre", text="Nuevo nombre", command=lambda: self.sort_by_column("nuevo nombre", False))
        self.tree.heading("modelo", text="Modelo", command=lambda: self.sort_by_column("modelo", False))
        self.tree.column("name", width=180)
        self.tree.column("size", width=100, anchor="e")
        self.tree.column("created", width=140)
        self.tree.column("modified", width=140)
        self.tree.column("DateTimeOriginal", width=140)
        self.tree.column("DateTimeDigitized", width=140)
        self.tree.column("DateTime", width=140)
        self.tree.column("subdirectorio", width=120)
        self.tree.column("nuevo nombre", width=180)
        self.tree.column("modelo", width=140)
        self.tree.pack(fill=BOTH, expand=True)
        self._sort_column = None
        self._sort_reverse = False

    def sort_by_column(self, col, reverse):
        items = list(self.tree.get_children(''))
        col_index = self.tree['columns'].index(col)
        def sort_key(iid):
            value = self.tree.set(iid, col)
            # Intenta convertir a número si es posible
            try:
                return float(value.replace(',', '').replace(' bytes', ''))
            except Exception:
                return value.lower() if isinstance(value, str) else value
        items.sort(key=sort_key, reverse=reverse)
        for idx, iid in enumerate(items):
            self.tree.move(iid, '', idx)
        # Alterna el orden para el próximo click
        self._sort_column = col
        self._sort_reverse = not reverse
        # Cambia el comando del heading para alternar
        self.tree.heading(col, command=lambda: self.sort_by_column(col, not reverse))

    def update_listbox(self, directory):
        self.tree.delete(*self.tree.get_children())
        if not os.path.isdir(directory):
            return
        image_exts = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')
        from utils.file_utils import get_image_file_info
        for fname in os.listdir(directory):
            if fname.lower().endswith(image_exts):
                fpath = os.path.join(directory, fname)
                try:
                    info = get_image_file_info(directory, fname)
                    size = info.size if info else os.path.getsize(fpath)
                    ctime = datetime.datetime.fromtimestamp(os.path.getctime(fpath)).strftime('%Y-%m-%d %H:%M:%S')
                    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fpath)).strftime('%Y-%m-%d %H:%M:%S')
                    # Inserta fila con columnas fijas, EXIF y nuevas vacías
                    values = [
                        fname,
                        size,
                        ctime,
                        mtime,
                        info.exif_datetime_original if info else '',
                        info.exif_datetime_digitized if info else '',
                        info.exif_datetime if info else '',
                        info.subdir if info else '',
                        info.nuevo_nombre if info else '',
                        info.camera_model if info and info.camera_model else ''
                    ]
                    self.tree.insert('', 'end', values=values)
                except Exception:
                    pass
        # Asegura que todas las columnas sean ordenables
        for col in self.tree['columns']:
            self.tree.heading(col, command=lambda c=col: self.sort_by_column(c, False))