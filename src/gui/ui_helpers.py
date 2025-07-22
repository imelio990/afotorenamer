import tkinter as tk

def show_exif_popup(root, fname, exif_info):
    popup = tk.Toplevel(root)
    popup.title(f"EXIF de {fname}")
    text = tk.Text(popup, wrap=tk.WORD, width=80, height=30)
    text.pack(fill=tk.BOTH, expand=True)
    text.insert(tk.END, "\n".join(exif_info))
    text.config(state=tk.DISABLED)
    btn = tk.Button(popup, text="Cerrar", command=popup.destroy)
    btn.pack(pady=5)

def listbox_home(tree):
    items = tree.get_children()
    if items:
        tree.selection_set(items[0])
        tree.focus(items[0])
        tree.see(items[0])
    return "break"

def listbox_end(tree):
    items = tree.get_children()
    if items:
        tree.selection_set(items[-1])
        tree.focus(items[-1])
        tree.see(items[-1])
    return "break"

def listbox_page_down(tree, page=10):
    items = tree.get_children()
    if not items:
        return "break"
    sel = tree.selection()
    if sel:
        idx = items.index(sel[0])
    else:
        idx = 0
    new_idx = min(idx + page, len(items) - 1)
    tree.selection_set(items[new_idx])
    tree.focus(items[new_idx])
    tree.see(items[new_idx])
    # Limpiar selección múltiple
    for iid in items:
        if iid != items[new_idx]:
            tree.selection_remove(iid)
    return "break"

def listbox_page_up(tree, page=10):
    items = tree.get_children()
    if not items:
        return "break"
    sel = tree.selection()
    if sel:
        idx = items.index(sel[0])
    else:
        idx = 0
    new_idx = max(idx - page, 0)
    tree.selection_set(items[new_idx])
    tree.focus(items[new_idx])
    tree.see(items[new_idx])
    # Limpiar selección múltiple
    for iid in items:
        if iid != items[new_idx]:
            tree.selection_remove(iid)
    return "break"
