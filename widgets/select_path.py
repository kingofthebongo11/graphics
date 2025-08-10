import tkinter as tk
from tkinter import filedialog


def select_path(entry_widget, path_type="folder", saved_data=None):
    """Открывает диалог выбора пути и вставляет его в виджет."""
    if path_type == "folder":
        selected_path = filedialog.askdirectory()
    elif path_type == "file":
        selected_path = filedialog.askopenfilename()
    else:
        raise ValueError("Недопустимый тип пути: используйте 'folder' или 'file'.")

    if selected_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, selected_path)
        if saved_data is not None:
            key = 'path'
            saved_data.update({key: entry_widget.get()})

