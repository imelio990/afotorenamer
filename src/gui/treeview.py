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

        # Construye la lista de rutas parciales para cada nivel
        parts = path.strip("\\").split("\\")
        if not parts:
            return

        # Ejemplo: C:\Users\egayosoa\Desktop -> ['C:', 'Users', 'egayosoa', 'Desktop']
        current_path = parts[0] + "\\"
        path_levels = [current_path]
        for part in parts[1:]:
            current_path = os.path.join(current_path, part)
            path_levels.append(current_path)

        def expand_level(level=0, parent=''):
            if level >= len(path_levels):
                return
            target_path = path_levels[level]
            for child in self.tree.get_children(parent):
                if self.tree.set(child, 'fullpath') == target_path:
                    self.tree.item(child, open=True)
                    self.on_open(None)  # Cargar subdirectorios
                    if level == len(path_levels) - 1:
                        self.tree.selection_set(child)
                        self.tree.see(child)
                    else:
                        # Espera a que los hijos se carguen antes de expandir el siguiente nivel
                        self.after(150, lambda l=level+1, p=child: expand_level(l, p))
                    break

        expand_level()

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)