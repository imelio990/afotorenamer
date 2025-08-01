from tkinter import Frame, Scrollbar
from tkinter.ttk import Treeview
import os

CONFIG_FILE = "config.txt"

class DirectoryTreeView(Frame):
    def __init__(self, master=None, log_func=None, **kwargs):
        super().__init__(master, **kwargs)
        self.log_func = log_func
        self.tree = Treeview(self, columns=('fullpath',), displaycolumns=())
        self.tree.heading('#0', text='Directorio')
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewOpen>>", self.on_open)

        # Leer última ruta seleccionada
        self.last_path = self.load_last_path()
        self.load_directories(path="C:\\")  # Empieza desde la raíz

        # Ya no restauramos aquí la ruta, lo hace defer_restore_last_path desde MainApplication

    def load_directories(self, path="C:\\"):
        self.tree.delete(*self.tree.get_children())
        self.insert_directory('', path)

    def insert_directory(self, parent, path):
        node = self.tree.insert(parent, 'end', text=os.path.basename(path) or path, values=(path,), open=False)
        if self.has_subdirs(path):
            self.tree.insert(node, 'end')  # dummy child
        return node

    def has_subdirs(self, path):
        try:
            for item in os.listdir(path):
                if os.path.isdir(os.path.join(path, item)):
                    return True
        except Exception:
            pass
        return False

    def on_open(self, event):
        node = self.tree.focus()
        path = self.tree.set(node, 'fullpath')
        children = self.tree.get_children(node)
        if children:
            if self.tree.item(children[0], "values") == "":
                self.tree.delete(children[0])
                try:
                    for item in os.listdir(path):
                        item_path = os.path.join(path, item)
                        if os.path.isdir(item_path):
                            self.insert_directory(node, item_path)
                except Exception:
                    pass

    def save_last_path(self, path):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                f.write(path)
        except Exception:
            pass

    def load_last_path(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return f.read().strip()
        except Exception:
            pass
        return None

    def select_and_expand_path(self, path):
        # Expande y selecciona el nodo correspondiente a la ruta dada, paso a paso
        if not path or not os.path.exists(path):
            return

        # Normalizar la ruta
        path = os.path.normpath(path)
        
        # Construye la lista de rutas parciales para cada nivel
        parts = []
        current = path
        while current and current != os.path.dirname(current):
            parts.insert(0, current)
            current = os.path.dirname(current)
        
        # Agregar la raíz si no está
        if parts and not parts[0].endswith(':\\'):
            root = os.path.splitdrive(path)[0] + '\\'
            if root not in parts:
                parts.insert(0, root)

        self.expand_path_recursively(parts, 0, '')

    def expand_path_recursively(self, path_parts, index, parent):
        """Expande recursivamente cada nivel del path"""
        if index >= len(path_parts):
            return
        
        target_path = path_parts[index]
        
        # Buscar el nodo correspondiente
        found_node = None
        for child in self.tree.get_children(parent):
            child_path = self.tree.set(child, 'fullpath')
            if child_path == target_path:
                found_node = child
                break
        
        if found_node:
            # Si es el último nivel, seleccionarlo
            if index == len(path_parts) - 1:
                self.tree.selection_set(found_node)
                self.tree.see(found_node)
                self.tree.focus(found_node)
            else:
                # Expandir este nodo y continuar con el siguiente nivel
                self.tree.item(found_node, open=True)
                # Simular el evento de apertura para cargar los subdirectorios
                self.tree.focus(found_node)
                self.on_open(None)
                # Continuar con el siguiente nivel después de un pequeño delay
                self.after(100, lambda: self.expand_path_recursively(path_parts, index + 1, found_node))

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)