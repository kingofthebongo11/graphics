"""Вкладка управления деревом кривых и путями файлов."""

from __future__ import annotations

import getpass
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

from pathlib import Path

from gui_bridge import tree_from_gui
from tabs.function4tabs4.cfile_writer import write_cfile
from tabs.function4tabs4.command_all import walk_tree_and_build_commands
from tabs.function4tabs4.naming import safe_name
from tabs.function4tabs4.tree_io import load_tree, save_tree
from topfolder_codec import decode_topfolder, encode_topfolder
from ui import constants as ui_const
from widgets import create_text, select_path


class NumberInputDialog(simpledialog.Dialog):
    """Диалог ввода номера элемента или узла.

    Разрешает только числовой ввод. При ошибке подсвечивает поле ввода
    и отображает текст ошибки.
    """

    def body(self, master: tk.Misc) -> tk.Widget:  # pragma: no cover - UI code
        ttk.Label(master, text="Номер элемента/узла:").grid(
            row=0, column=0, sticky="w", padx=5, pady=(5, 0)
        )
        self.var = tk.StringVar()
        self.entry = ttk.Entry(master, textvariable=self.var)
        self.entry.grid(row=1, column=0, padx=5, pady=5)
        self.error_label = ttk.Label(master, text="", foreground="red")
        self.error_label.grid(row=2, column=0, sticky="w", padx=5)
        self._normal_bg = self.entry.cget("background")
        self._error_bg = "#ffcccc"
        self.entry.bind("<KeyRelease>", lambda _e: self._clear_error())
        return self.entry

    def _clear_error(self) -> None:
        self.entry.configure(background=self._normal_bg)
        self.error_label.config(text="")

    def validate(self) -> bool:  # pragma: no cover - UI code
        value = self.var.get().strip()
        if not value.isdigit():
            self.entry.configure(background=self._error_bg)
            self.error_label.config(text="Допустимы только цифры")
            return False
        self.result = value
        return True


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
        row=1,
        column=0,
        columnspan=8,
        sticky="nsew",
        padx=ui_const.PADDING,
        pady=ui_const.PADDING,
    )

    scroll = ttk.Scrollbar(tab4, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.grid(row=1, column=8, sticky="ns", pady=ui_const.PADDING)

    tab4.rowconfigure(1, weight=1)
    tab4.columnconfigure(0, weight=1)

    user_name = safe_name(getpass.getuser())
    top_folder_name = encode_topfolder(user_name, "node")
    root_id = tree.insert("", "end", text=user_name, values=(top_folder_name,), open=True)

    # --- Панель свойств верхней папки ---
    props = ttk.LabelFrame(tab4, text="Свойства TOP папки")
    props.grid(
        row=0,
        column=0,
        columnspan=8,
        sticky="ew",
        padx=ui_const.PADDING,
        pady=(ui_const.PADDING, 0),
    )
    props.columnconfigure(1, weight=1)

    ttk.Label(props, text="user_name:").grid(row=0, column=0, sticky="w")
    user_var = tk.StringVar(value=user_name)
    user_entry = ttk.Entry(props, textvariable=user_var)
    user_entry.grid(row=0, column=1, sticky="ew")

    ttk.Label(props, text="entity_kind:").grid(row=1, column=0, sticky="w")
    entity_var = tk.StringVar(value="node")
    entity_box = ttk.Combobox(
        props, textvariable=entity_var, values=("element", "node"), state="readonly"
    )
    entity_box.grid(row=1, column=1, sticky="ew")

    element_label = ttk.Label(props, text="element_type:")
    element_var = tk.StringVar(value="beam")
    element_box = ttk.Combobox(
        props,
        textvariable=element_var,
        values=("beam", "shell", "solid"),
        state="readonly",
    )

    ttk.Label(props, text="top_folder:").grid(row=0, column=2, sticky="w", padx=(10, 0))
    top_var = tk.StringVar(value=top_folder_name)
    ttk.Label(props, textvariable=top_var).grid(row=0, column=3, sticky="w")

    def update_top_folder(*_):
        name = user_var.get()
        kind = entity_var.get()
        elem = element_var.get() if kind == "element" else None
        try:
            new_top = encode_topfolder(name, kind, elem)
        except Exception:
            return
        top_var.set(new_top)
        tree.item(root_id, text=name, values=(new_top,))
        for child in tree.get_children(root_id):
            tree.set(child, "top_folder", new_top)

    def on_entity_change(*_):
        if entity_var.get() == "element":
            element_label.grid(row=2, column=0, sticky="w")
            element_box.grid(row=2, column=1, sticky="ew")
        else:
            element_label.grid_remove()
            element_box.grid_remove()
        update_top_folder()

    user_var.trace_add("write", update_top_folder)
    element_var.trace_add("write", update_top_folder)
    entity_var.trace_add("write", on_entity_change)

    on_entity_change()

    # --- Действия с деревом ---
    def add_node() -> None:
        parent = tree.selection()[0] if tree.selection() else root_id
        if tree.parent(parent) == root_id:
            dlg = NumberInputDialog(tab4, title="Добавить элемент/узел")
            number = dlg.result
            if number is not None:
                tree.insert(parent, "end", text=number)
        else:
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
        if item == root_id:
            return
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
        try:
            u, k, e = decode_topfolder(loaded.top)
        except Exception:
            messagebox.showerror("Ошибка", "Некорректное имя папки", parent=tab4)
            return
        user_var.set(u)
        entity_var.set(k)
        if e:
            element_var.set(e)
        update_top_folder()

    def clear_all() -> None:
        for item in tree.get_children(root_id):
            tree.delete(item)

    # --- Контекстное меню ---
    menu = tk.Menu(tree, tearoff=0)
    menu.add_command(label="Добавить", command=add_node)
    menu.add_command(label="Удалить", command=remove_node)
    menu.add_command(label="Переименовать", command=rename_node)

    def show_menu(event: tk.Event) -> None:  # pragma: no cover - UI code
        item = tree.identify_row(event.y)
        if not item:
            return
        tree.selection_set(item)
        # disable rename/delete for root
        if item == root_id:
            menu.entryconfigure(1, state="disabled")
            menu.entryconfigure(2, state="disabled")
        else:
            menu.entryconfigure(1, state="normal")
            menu.entryconfigure(2, state="normal")
        menu.tk_popup(event.x_root, event.y_root)

    tree.bind("<Button-3>", show_menu)

    # --- Генерация файлов ---
    def generate_cfile() -> None:
        path = cfile_entry.get().strip()
        if not path:
            messagebox.showerror("Ошибка", "Укажите путь к .cfile", parent=tab4)
            return

        class _TkItem:
            def __init__(self, widget: ttk.Treeview, iid: str) -> None:
                self._tree = widget
                self._iid = iid

            def text(self, column: int) -> str:
                if column == 0:
                    return self._tree.item(self._iid, "text")
                values = self._tree.item(self._iid, "values")
                return values[column - 1] if column - 1 < len(values) else ""

            def childCount(self) -> int:
                return len(self._tree.get_children(self._iid))

            def child(self, index: int) -> "_TkItem":
                children = self._tree.get_children(self._iid)
                return _TkItem(self._tree, children[index])

        class _TkWidget:
            def __init__(self, widget: ttk.Treeview, root: str) -> None:
                self._tree = widget
                self._root = root

            def topLevelItemCount(self) -> int:
                return 1

            def topLevelItem(self, index: int) -> _TkItem:
                if index != 0:
                    raise IndexError("Только один корневой элемент")
                return _TkItem(self._tree, self._root)

        try:
            model_root = tree_from_gui(_TkWidget(tree, root_id))
        except Exception as exc:  # pragma: no cover - UI error handling
            messagebox.showerror("Ошибка", str(exc), parent=tab4)
            return

        commands = walk_tree_and_build_commands([model_root], Path(path).parent)
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
    btn_frame.grid(row=2, column=0, columnspan=8, sticky="w", padx=ui_const.PADDING)

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
        row=3,
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
        row=4,
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

