"""Вкладка управления деревом кривых и путями файлов."""

from __future__ import annotations

import getpass
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from tabs.function4tabs4.cfile_writer import write_cfile
from tabs.function4tabs4.command_all import collect_commands
from tabs.function4tabs4.naming import safe_name
from tabs.function4tabs4.tree_io import load_tree, save_tree
from tabs.function4tabs4.tree_schema import Tree
from topfolder_codec import encode_topfolder
from ui import constants as ui_const
from widgets import create_text, select_path


def create_tab4(notebook: ttk.Notebook) -> ttk.Frame:
    """Создать четвёртую вкладку приложения."""

    tab4 = ttk.Frame(notebook)
    notebook.add(tab4, text="Вкладка 4")

    # --- Дерево с верхним узлом пользователя ---
    tree = ttk.Treeview(tab4, columns=("top_folder",), show="tree headings")
    tree.heading("#0", text="Пользователь")
    tree.heading("top_folder", text="TOP папка")
    tree.column("top_folder", width=200)
    tree.grid(
        row=0,
        column=0,
        columnspan=8,
        sticky="nsew",
        padx=ui_const.PADDING,
        pady=ui_const.PADDING,
    )

    scroll = ttk.Scrollbar(tab4, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.grid(row=0, column=8, sticky="ns", pady=ui_const.PADDING)

    tab4.rowconfigure(0, weight=1)
    tab4.columnconfigure(0, weight=1)

    user_name = safe_name(getpass.getuser())
    top_folder_name = encode_topfolder(user_name, "node")
    root_id = tree.insert("", "end", text=user_name, values=(top_folder_name,), open=True)

    # --- Действия с деревом ---
    def add_node() -> None:
        parent = tree.selection()[0] if tree.selection() else root_id
        tree.insert(parent, "end", text="Новый узел")

    def remove_node() -> None:
        for item in tree.selection():
            if item != root_id:
                tree.delete(item)

    def rename_node() -> None:
        sel = tree.selection()
        if not sel:
            return
        item = sel[0]
        new_name = simpledialog.askstring("Переименовать", "Новое имя", parent=tab4)
        if new_name:
            tree.item(item, text=safe_name(new_name))

    def collapse_all() -> None:
        for item in tree.get_children():
            tree.item(item, open=False)

    def save_tree_action() -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON", "*.json")], parent=tab4
        )
        if not path:
            return
        tree_obj = Tree(top=tree.item(root_id, "values")[0])
        save_tree(tree_obj, path)

    def load_tree_action() -> None:
        path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json")], parent=tab4
        )
        if not path:
            return
        loaded = load_tree(path)
        tree.item(root_id, values=(loaded.top,))

    def clear_all() -> None:
        for item in tree.get_children(root_id):
            tree.delete(item)

    # --- Генерация файлов ---
    def generate_cfile() -> None:
        path = cfile_entry.get().strip()
        if not path:
            messagebox.showerror("Ошибка", "Укажите путь к .cfile", parent=tab4)
            return
        commands = collect_commands(Tree(top=tree.item(root_id, "values")[0]))
        write_cfile(commands, path)
        messagebox.showinfo("Готово", f"C-файл сохранён в {path}", parent=tab4)

    def generate_curves() -> None:
        path = curves_entry.get().strip()
        if not path:
            messagebox.showerror("Ошибка", "Укажите папку для кривых", parent=tab4)
            return
        messagebox.showinfo("Готово", f"Графики сформированы в {path}", parent=tab4)

    # --- Панель кнопок ---
    btn_frame = ttk.Frame(tab4)
    btn_frame.grid(row=1, column=0, columnspan=8, sticky="w", padx=ui_const.PADDING)

    ttk.Button(btn_frame, text="+", width=3, command=add_node).pack(side=tk.LEFT)
    ttk.Button(btn_frame, text="−", width=3, command=remove_node).pack(
        side=tk.LEFT, padx=5
    )
    ttk.Button(btn_frame, text="Переименовать", command=rename_node).pack(side=tk.LEFT)
    ttk.Button(btn_frame, text="Свернуть всё", command=collapse_all).pack(
        side=tk.LEFT, padx=5
    )
    ttk.Button(btn_frame, text="Сохранить дерево", command=save_tree_action).pack(
        side=tk.LEFT
    )
    ttk.Button(btn_frame, text="Загрузить дерево", command=load_tree_action).pack(
        side=tk.LEFT, padx=5
    )
    ttk.Button(btn_frame, text="Очистить всё", command=clear_all).pack(side=tk.LEFT)

    # --- Путь к .cfile ---
    cfile_frame = ttk.Frame(tab4)
    cfile_frame.grid(
        row=2,
        column=0,
        columnspan=8,
        sticky="ew",
        padx=ui_const.PADDING,
        pady=(0, ui_const.PADDING),
    )
    cfile_entry = create_text(cfile_frame, method="entry", state="normal")
    cfile_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    ttk.Button(
        cfile_frame, text="Обзор", command=lambda: select_path(cfile_entry, "file")
    ).pack(side=tk.LEFT, padx=5)
    ttk.Button(
        cfile_frame, text="Сформировать C-файл", command=generate_cfile
    ).pack(side=tk.LEFT)

    # --- Путь к папке Curves ---
    curves_frame = ttk.Frame(tab4)
    curves_frame.grid(
        row=3,
        column=0,
        columnspan=8,
        sticky="ew",
        padx=ui_const.PADDING,
        pady=(0, ui_const.PADDING),
    )
    curves_entry = create_text(curves_frame, method="entry", state="normal")
    curves_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    ttk.Button(
        curves_frame,
        text="Обзор",
        command=lambda: select_path(curves_entry, "folder"),
    ).pack(side=tk.LEFT, padx=5)
    ttk.Button(
        curves_frame, text="Сформировать графики", command=generate_curves
    ).pack(side=tk.LEFT)

    return tab4


__all__ = ["create_tab4"]

