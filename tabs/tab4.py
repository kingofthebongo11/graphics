import tkinter as tk
from tkinter import ttk

from widgets import ask_numeric_id


def create_tab4(notebook: ttk.Notebook) -> ttk.Frame:
    """Создает четвертую вкладку приложения."""

    tab4 = ttk.Frame(notebook)
    notebook.add(tab4, text="Вкладка 4")

    tree = ttk.Treeview(tab4)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    entity = tree.insert("", "end", text="Сущность", open=True)
    analysis = tree.insert(entity, "end", text="Анализ", open=True)

    def add_file_node():
        selected = tree.selection()
        if not selected or selected[0] != analysis:
            return
        number = ask_numeric_id(tab4, title="Номер элемента/узла")
        if number is not None:
            tree.insert(analysis, "end", text=str(number))

    add_btn = ttk.Button(tab4, text="+", command=add_file_node)
    add_btn.pack(side=tk.LEFT, padx=5, pady=5)

    return tab4
