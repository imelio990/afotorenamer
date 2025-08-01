import os
import tkinter as tk
from gui.treeview import DirectoryTreeView
from gui.listbox import ImageListBox
from gui.rename_button import RenameButton
from gui.ui_helpers import show_exif_popup, listbox_home, listbox_end, listbox_page_down, listbox_page_up
from utils.file_utils import get_image_file_info, mover_archivo
from utils.image_types import ImageFileInfo
from utils.logger import log_to_listbox
from utils.config import get_last_directory, save_last_directory
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

        # Frame para la lista de ficheros y su scrollbar
        self.list_frame = tk.Frame(self.right_frame)
        self.list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Listbox de imágenes (Treeview) y scrollbar
        self.listbox = ImageListBox(self.list_frame)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.list_scroll = tk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.listbox.tree.yview)
        self.listbox.tree.config(yscrollcommand=self.list_scroll.set)
        self.list_scroll.pack(side=tk.RIGHT, fill=tk.Y)

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

        # Bind para teclas especiales en la lista de ficheros
        self.listbox.tree.bind("<Home>", self.on_listbox_home)
        self.listbox.tree.bind("<End>", self.on_listbox_end)
        self.listbox.tree.bind("<Next>", self.on_listbox_page_down)
        self.listbox.tree.bind("<Prior>", self.on_listbox_page_up)
        self.listbox.tree.bind("<Home>", lambda e: listbox_home(self.listbox.tree))
        self.listbox.tree.bind("<End>", lambda e: listbox_end(self.listbox.tree))
        self.listbox.tree.bind("<Next>", lambda e: listbox_page_down(self.listbox.tree))
        self.listbox.tree.bind("<Prior>", lambda e: listbox_page_up(self.listbox.tree))

        # Cargar el último directorio guardado
        self.load_last_directory()

    def on_listbox_home(self, event):
        items = self.listbox.tree.get_children()
        if items:
            self.listbox.tree.selection_set(items[0])
            self.listbox.tree.see(items[0])
        return "break"

    def on_listbox_end(self, event):
        items = self.listbox.tree.get_children()
        if items:
            self.listbox.tree.selection_set(items[-1])
            self.listbox.tree.see(items[-1])
        return "break"

    def on_listbox_page_down(self, event):
        items = self.listbox.tree.get_children()
        if not items:
            return "break"
        sel = self.listbox.tree.selection()
        if sel:
            idx = items.index(sel[0])
        else:
            idx = 0
        page = 10  # Número de elementos por página (ajustable)
        new_idx = min(idx + page, len(items) - 1)
        self.listbox.tree.selection_set(items[new_idx])
        self.listbox.tree.see(items[new_idx])
        return "break"

    def on_listbox_page_up(self, event):
        items = self.listbox.tree.get_children()
        if not items:
            return "break"
        sel = self.listbox.tree.selection()
        if sel:
            idx = items.index(sel[0])
        else:
            idx = 0
        page = 10  # Número de elementos por página (ajustable)
        new_idx = max(idx - page, 0)
        self.listbox.tree.selection_set(items[new_idx])
        self.listbox.tree.see(items[new_idx])
        return "break"

    def on_directory_select(self, event):
        selected_item = self.treeview.tree.selection()
        if selected_item:
            directory = self.treeview.tree.set(selected_item[0], 'fullpath')
            self.current_directory = directory
            self.listbox.update_listbox(directory)
            self.log_message(f"Directorio seleccionado: {directory}")
            # Guardar el directorio seleccionado en la configuración
            save_last_directory(directory)

    def log_message(self, message: str):
        log_to_listbox(self.log_listbox, message)

    def scan_exif_dates(self):
        import datetime
        directory = self.current_directory
        if not directory:
            self.log_message("No hay directorio seleccionado.")
            return
        self.listbox.tree.delete(*self.listbox.tree.get_children())
        image_exts = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')
        video_exts = ('.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm')
        for root, _, files in os.walk(directory):
            for fname in files:
                ext = os.path.splitext(fname)[1].lower()
                fpath = os.path.join(root, fname)
                # Calcular ruta relativa desde el directorio base
                rel_path = os.path.relpath(fpath, directory)
                try:
                    if ext in image_exts:
                        info = get_image_file_info(root, fname)
                        size = info.size if info else os.path.getsize(fpath)
                        ctime = datetime.datetime.fromtimestamp(os.path.getctime(fpath)).strftime('%Y-%m-%d %H:%M:%S')
                        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fpath)).strftime('%Y-%m-%d %H:%M:%S')
                        values = [
                            rel_path,  # Usar ruta relativa en lugar de solo el nombre
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
                    elif ext in video_exts:
                        size = os.path.getsize(fpath)
                        ctime = datetime.datetime.fromtimestamp(os.path.getctime(fpath)).strftime('%Y-%m-%d %H:%M:%S')
                        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fpath)).strftime('%Y-%m-%d %H:%M:%S')
                        # Para videos, no hay EXIF ni modelo
                        values = [
                            rel_path,  # Usar ruta relativa en lugar de solo el nombre
                            size,
                            ctime,
                            mtime,
                            '', '', '', '', '', ''
                        ]
                    else:
                        continue
                    self.listbox.tree.insert('', 'end', values=values)
                except Exception:
                    pass
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
        self.root.config(cursor="watch")
        self.root.update()
        try:
            self.log_message(f"Iniciando renombrado en directorio: {directory}")
            self.log_message(f"Archivos a procesar: {len(selected)}")
            
            for iid in selected:
                values = list(self.listbox.tree.item(iid)['values'])
                rel_path = values[0]  # Ahora es la ruta relativa completa
                fname = os.path.basename(rel_path)  # Extraer solo el nombre del archivo
                full_path = os.path.join(directory, rel_path)  # Construir ruta completa
                
                self.log_message(f"Procesando: {rel_path}")
                
                if not os.path.exists(full_path):
                    self.log_message(f"✗ No se encontró el archivo: {full_path}")
                    self.listbox.tree.selection_remove(iid)
                    continue
                
                # Verificar si es imagen o video para procesarlo adecuadamente
                ext = os.path.splitext(fname)[1].lower()
                image_exts = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp')
                video_exts = ('.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm')
                
                if ext in image_exts:
                    info = get_image_file_info(os.path.dirname(full_path), fname)
                    if info:
                        # Forzar el destino a subdirectorio de mes dentro del directorio elegido
                        import re
                        subdir = str(info.subdir)
                        match = re.match(r"(\d{4})[-_/]?(\d{2})", subdir)
                        if match:
                            subdir = f"{match.group(1)}_{match.group(2)}"
                        # Actualizar info.subdir para que mover_archivo lo use
                        info.subdir = subdir
                        success = mover_archivo(info, directory, self.log_message)
                        if success:
                            self.log_message(f"✓ Archivo procesado correctamente")
                    else:
                        self.log_message(f"✗ No se pudo obtener información EXIF de {fname}")
                elif ext in video_exts:
                    # Para videos, usar fechas de archivo
                    import datetime
                    ctime = os.path.getctime(full_path)
                    mtime = os.path.getmtime(full_path)
                    min_date = datetime.datetime.fromtimestamp(min(ctime, mtime))
                    subdir = min_date.strftime("%Y_%m")
                    nuevo_nombre = f"{min_date.strftime('%Y%m%d_%H%M%S')}_{fname}"
                    
                    # Crear un objeto ImageFileInfo para videos
                    from utils.image_types import ImageFileInfo
                    info = ImageFileInfo(
                        fname=fname,
                        size=os.path.getsize(full_path),
                        ctime=ctime,
                        mtime=mtime,
                        subdir=subdir,
                        nuevo_nombre=nuevo_nombre,
                        min_date=min_date
                    )
                    success = mover_archivo(info, directory, self.log_message)
                    if success:
                        self.log_message(f"✓ Video procesado correctamente")
                else:
                    self.log_message(f"✗ Tipo de archivo no soportado: {fname}")
                
                self.listbox.tree.selection_remove(iid)
        finally:
            self.root.config(cursor="")
            self.root.update()
        self.log_message("=== Renombrado finalizado ===")

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
        rel_path = values[0]  # Ahora es la ruta relativa completa
        fname = os.path.basename(rel_path)
        fpath = os.path.join(directory, rel_path)  # Usar ruta relativa para construir path completo
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
            show_exif_popup(self.root, fname, exif_info)
        except Exception as e:
            self.log_message(f"Error leyendo EXIF de {fname}: {e}")

    def load_last_directory(self):
        """Carga y selecciona el último directorio guardado"""
        last_dir = get_last_directory()
        if last_dir and os.path.exists(last_dir):
            try:
                # Usar after para dar tiempo a que la interfaz se inicialice completamente
                self.root.after(500, lambda: self.restore_directory(last_dir))
            except Exception as e:
                self.log_message(f"Error al restaurar directorio: {e}")
        else:
            self.log_message("No hay directorio previo guardado o no existe")

    def restore_directory(self, directory):
        """Restaura el directorio expandiendo el treeview y seleccionándolo"""
        try:
            # Expandir el treeview hasta el directorio guardado y seleccionarlo
            self.treeview.select_and_expand_path(directory)
            # Dar un poco más de tiempo para que se complete la expansión
            self.root.after(200, lambda: self.finalize_directory_restore(directory))
        except Exception as e:
            self.log_message(f"Error al expandir directorio: {e}")

    def finalize_directory_restore(self, directory):
        """Finaliza la restauración del directorio actualizando el listbox"""
        try:
            self.current_directory = directory
            self.listbox.update_listbox(directory)
            self.log_message(f"Directorio restaurado: {directory}")
        except Exception as e:
            self.log_message(f"Error al finalizar restauración: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()