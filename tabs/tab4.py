"""Вкладка с деревом результатов анализа.

На вкладке отображается ``Treeview`` с иерархией узлов.  ПКМ-меню
предоставляет действия **только** для выбранного узла: добавление
дочернего элемента, переименование и удаление.  Глобальные действия
«Свернуть всё» и «Очистить всё» вынесены в отдельную панель над деревом.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import simpledialog, ttk


def create_tab4(notebook: ttk.Notebook) -> ttk.Frame:
    """Создает четвертую вкладку приложения."""

    tab4 = ttk.Frame(notebook)
    notebook.add(tab4, text="Вкладка 4")

    # ---- Панель с глобальными действиями ---------------------------------
    panel = ttk.Frame(tab4)
    panel.pack(side=tk.TOP, fill=tk.X)

    tree = ttk.Treeview(tab4, show="tree")
    tree.pack(fill=tk.BOTH, expand=True)

    root = tree.insert("", "end", text="Корень")

    def collapse_all() -> None:
        def _collapse(item: str) -> None:
            tree.item(item, open=False)
            for child in tree.get_children(item):
                _collapse(child)

        for item in tree.get_children(""):
            _collapse(item)

    def clear_all() -> None:
        tree.delete(*tree.get_children(""))

    ttk.Button(panel, text="Свернуть всё", command=collapse_all).pack(
        side=tk.LEFT, padx=2
    )
    ttk.Button(panel, text="Очистить всё", command=clear_all).pack(
        side=tk.LEFT, padx=2
    )

    # ---- Контекстное меню для узлов --------------------------------------
    menu = tk.Menu(tree, tearoff=False)

    def add_child(item: str) -> None:
        name = simpledialog.askstring("Добавить", "Имя узла:", parent=tab4)
        if name:
            tree.insert(item, "end", text=name)
            tree.item(item, open=True)

    def rename_item(item: str) -> None:
        current = tree.item(item, "text")
        new_name = simpledialog.askstring(
            "Переименовать", "Новое имя:", initialvalue=current, parent=tab4
        )
        if new_name:
            tree.item(item, text=new_name)

    def show_menu(event: tk.Event) -> None:
        iid = tree.identify_row(event.y)
        if not iid:
            return
        tree.selection_set(iid)
        menu.delete(0, tk.END)
        if iid != root:
            menu.add_command(label="Переименовать", command=lambda: rename_item(iid))
        menu.add_command(label="Добавить", command=lambda: add_child(iid))
        if iid != root:
            menu.add_command(label="Удалить", command=lambda: tree.delete(iid))
        menu.tk_popup(event.x_root, event.y_root)

    tree.bind("<Button-3>", show_menu)

    return tab4
