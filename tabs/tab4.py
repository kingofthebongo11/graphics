"""Вкладка управления деревом кривых и путями файлов."""

from __future__ import annotations

import getpass
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk

import json
from pathlib import Path

from tabs.function4tabs4.cfile_writer import write_cfile
from tabs.function4tabs4.command_all import walk_tree_and_build_commands
from tabs.function4tabs4.config import CFILE_NAME
from tabs.function4tabs4.naming import safe_name
from tabs.function4tabs4.tree_schema import Tree
from topfolder_codec import decode_topfolder, encode_topfolder
from tree_schema import AnalysisNode, EntityNode, FileNode
from ui import constants as ui_const
from widgets import create_text, select_path
from curves_pipeline import build_curves_report
from analysis_types import ANALYSIS_TYPES_BY_ELEMENT


class AnalysisTypeDialog(simpledialog.Dialog):
    """Диалог выбора типа анализа."""

    def __init__(self, parent: tk.Misc, title: str, values: list[str]) -> None:
        self._values = values
        super().__init__(parent, title)

    def body(self, master: tk.Misc) -> tk.Widget:  # pragma: no cover - UI code
        ttk.Label(master, text="Тип анализа:").grid(
            row=0, column=0, sticky="w", padx=5, pady=(5, 0)
        )
        self.var = tk.StringVar()
        self.combo = ttk.Combobox(
            master, textvariable=self.var, values=self._values, state="readonly"
        )
        self.combo.grid(row=1, column=0, padx=5, pady=5)
        if self._values:
            self.combo.current(0)
        return self.combo

    def apply(self) -> None:  # pragma: no cover - UI code
        self.result = self.var.get()


class SectionDialog(simpledialog.Dialog):
    """Диалог создания или редактирования верхней папки дерева."""

    def __init__(
        self, parent: tk.Misc, tree: ttk.Treeview, item: str | None = None
    ) -> None:
        self._tree = tree
        self._item = item
        super().__init__(parent, title="Свойства раздела")

    def body(self, master: tk.Misc) -> tk.Widget:  # pragma: no cover - UI code
        master.columnconfigure(1, weight=1)
        ttk.Label(master, text="Название раздела").grid(
            row=0, column=0, sticky="w", padx=5, pady=(5, 0)
        )
        self.name_var = tk.StringVar()
        self.name_box = ttk.Combobox(
            master,
            textvariable=self.name_var,
            values=["Колонна", "Плита", "Стена", "Балка"],
            state="readonly",
        )
        self.name_box.grid(row=0, column=1, sticky="ew", padx=5, pady=(5, 0))
        if self.name_box["values"]:
            self.name_box.current(0)

        ttk.Label(master, text="Тип").grid(
            row=1, column=0, sticky="w", padx=5, pady=(5, 0)
        )
        self.entity_var = tk.StringVar(value="node")
        self.entity_box = ttk.Combobox(
            master,
            textvariable=self.entity_var,
            values=("element", "node"),
            state="readonly",
        )
        self.entity_box.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        self.element_label = ttk.Label(master, text="Тип элементов")
        self.element_var = tk.StringVar(value="beam")
        self.element_box = ttk.Combobox(
            master,
            textvariable=self.element_var,
            values=("beam", "shell", "solid"),
            state="readonly",
        )

        ttk.Label(master, text="top_folder:").grid(
            row=0, column=2, sticky="w", padx=(10, 0), pady=(5, 0)
        )
        self.top_var = tk.StringVar()
        ttk.Label(master, textvariable=self.top_var).grid(
            row=0, column=3, sticky="w", pady=(5, 0)
        )

        def update_top(*_):
            name = safe_name(self.name_var.get())
            kind = self.entity_var.get()
            elem = self.element_var.get() if kind == "element" else None
            try:
                new_top = encode_topfolder(name, kind, elem)
            except Exception:
                new_top = ""
            self.top_var.set(new_top)

        def on_entity_change(*_):
            if self.entity_var.get() == "element":
                self.element_label.grid(
                    row=2, column=0, sticky="w", padx=5, pady=(5, 0)
                )
                self.element_box.grid(
                    row=2, column=1, sticky="ew", padx=5, pady=5
                )
            else:
                self.element_label.grid_remove()
                self.element_box.grid_remove()
            update_top()

        self.name_var.trace_add("write", update_top)
        self.entity_var.trace_add("write", on_entity_change)
        self.element_var.trace_add("write", update_top)

        if self._item:
            try:
                u, k, e = decode_topfolder(self._tree.item(self._item, "text"))
            except Exception:
                u, k, e = "", "node", None
            values = list(self.name_box["values"])
            if u in values:
                self.name_box.current(values.index(u))
            else:
                values.append(u)
                self.name_box["values"] = values
                self.name_box.set(u)
            self.name_var.set(u)
            self.entity_var.set(k)
            if e:
                self.element_var.set(e)

        on_entity_change()
        return self.name_box

    def apply(self) -> None:  # pragma: no cover - UI code
        name = safe_name(self.name_var.get())
        kind = self.entity_var.get()
        elem = self.element_var.get() if kind == "element" else None
        try:
            text = encode_topfolder(name, kind, elem)
        except Exception:
            return
        if self._item:
            self._tree.item(self._item, text=text)
        else:
            self._tree.insert("", "end", text=text, open=True)
        self.result = text


def treeview_to_entity_nodes(tree: ttk.Treeview) -> list[EntityNode]:
    """Преобразовать ``ttk.Treeview`` в список ``EntityNode``."""

    roots: list[EntityNode] = []
    for root in tree.get_children():
        user_name, entity_kind, element_type = decode_topfolder(
            tree.item(root, "text")
        )
        entity = EntityNode(
            user_name=user_name,
            entity_kind=entity_kind,  # type: ignore[arg-type]
            element_type=element_type,  # type: ignore[arg-type]
        )
        for analysis in tree.get_children(root):
            analysis_type = tree.item(analysis, "text")
            analysis_node = AnalysisNode(analysis_type=analysis_type)
            for file in tree.get_children(analysis):
                file_id = int(tree.item(file, "text"))
                analysis_node.children.append(FileNode(id=file_id))
            entity.children.append(analysis_node)
        roots.append(entity)
    return roots


def create_tab4(notebook: ttk.Notebook) -> ttk.Frame:
    """Создать четвёртую вкладку приложения."""

    tab4 = ttk.Frame(notebook)
    notebook.add(tab4, text="Вкладка 4")

    # --- Дерево ---
    tree = ttk.Treeview(tab4, show="tree")
    tree.heading("#0", text="Полное имя")
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

    tab4.tree = tree  # type: ignore[attr-defined]

    # --- Действия с деревом ---
    def add_node() -> None:
        sel = tree.selection()
        if not sel:
            SectionDialog(tab4, tree)
            return

        item = sel[0]
        parent = tree.parent(item)

        try:
            _, _, element_type = decode_topfolder(tree.item(item, "text"))
        except Exception:
            element_type = None

        if parent == "":
            values = ANALYSIS_TYPES_BY_ELEMENT.get(element_type, [])
            dlg = AnalysisTypeDialog(
                tab4, title="Выбор типа анализа", values=values
            )
            choice = dlg.result
            if choice:
                tree.insert(item, "end", text=choice)
            return

        if tree.parent(parent) == "":
            number = simpledialog.askstring(
                "Номер элемента", "Введите номер", parent=tab4
            )
            if number:
                tree.insert(item, "end", text=safe_name(number))

    def remove_node() -> None:
        for item in tree.selection():
            tree.delete(item)

    def rename_node() -> None:
        sel = tree.selection()
        if not sel:
            return
        item = sel[0]
        if tree.parent(item) == "":
            SectionDialog(tab4, tree, item=item)
            return
        new_name = simpledialog.askstring("Переименовать", "Новое имя", parent=tab4)
        if new_name:
            tree.item(item, text=safe_name(new_name))

    def collapse_all() -> None:
        def _collapse(node: str) -> None:
            tree.item(node, open=False)
            for child in tree.get_children(node):
                _collapse(child)

        for item in tree.get_children():
            _collapse(item)

    def save_tree_action() -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON", "*.json")], parent=tab4
        )
        if not path:
            return
        data = [Tree(top=tree.item(i, "text")).to_dict() for i in tree.get_children()]
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def load_tree_action() -> None:
        path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json")], parent=tab4
        )
        if not path:
            return
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        for item in tree.get_children():
            tree.delete(item)
        for item in raw:
            t = Tree.from_dict(item)
            try:
                decode_topfolder(t.top)
            except Exception:
                messagebox.showerror("Ошибка", "Некорректное имя папки", parent=tab4)
                continue
            tree.insert("", "end", text=t.top, open=True)

    def clear_all() -> None:
        for item in tree.get_children():
            tree.delete(item)

    # --- Контекстное меню ---
    menu = tk.Menu(tree, tearoff=0)
    menu.add_command(label="Добавить", command=add_node)
    menu.add_command(label="Удалить", command=remove_node)
    menu.add_command(label="Переименовать", command=rename_node)

    def show_menu(event: tk.Event) -> None:  # pragma: no cover - UI code
        item = tree.identify_row(event.y)
        if item:
            tree.selection_set(item)
            if tree.parent(item) != "" and tree.parent(tree.parent(item)) != "":
                menu.entryconfigure(0, state="disabled")
            else:
                menu.entryconfigure(0, state="normal")
            menu.entryconfigure(1, state="normal")
            menu.entryconfigure(2, state="normal")
        else:
            tree.selection_remove(tree.selection())
            menu.entryconfigure(0, state="normal")
            menu.entryconfigure(1, state="disabled")
            menu.entryconfigure(2, state="disabled")
        menu.tk_popup(event.x_root, event.y_root)

    tree.bind("<Button-3>", show_menu)
    tree.bind("<Insert>", lambda e: add_node())
    tree.bind("<Delete>", lambda e: remove_node())
    tree.bind("<F2>", lambda e: rename_node())

    # --- Генерация файлов ---
    def generate_cfile() -> None:
        path_str = cfile_entry.get().strip()
        if not path_str:
            messagebox.showerror("Ошибка", "Укажите путь к .cfile", parent=tab4)
            return

        path = Path(path_str)

        try:
            roots = treeview_to_entity_nodes(tree)
        except Exception as exc:  # pragma: no cover - UI error handling
            messagebox.showerror("Ошибка", str(exc), parent=tab4)
            return

        curves_root = path.parent / "curves"
        for node in roots:
            top_folder = encode_topfolder(
                node.user_name, node.entity_kind, node.element_type
            )
            for analysis in node.children:
                (curves_root / top_folder / analysis.analysis_type).mkdir(
                    parents=True, exist_ok=True
                )

        commands = walk_tree_and_build_commands(roots, path.parent)
        write_cfile(commands, path)
        messagebox.showinfo("Готово", f"C-файл сохранён в {path}", parent=tab4)

    def generate_curves() -> None:
        path = curves_entry.get().strip()
        if not path:
            messagebox.showerror("Ошибка", "Укажите папку для кривых", parent=tab4)
            return

        root = Path(path)
        if not root.exists():
            messagebox.showerror("Ошибка", f"Папка {path} не найдена", parent=tab4)
            return

        docx_path, errors = build_curves_report(root)
        if errors:
            error_file = root / "errors.log"
            error_file.write_text("\n".join(errors), encoding="utf-8")
            messagebox.showwarning(
                "Готово с ошибками",
                f"Возникли ошибки. См. {error_file}",
                parent=tab4,
            )
        else:
            messagebox.showinfo(
                "Готово",
                f"Отчёт сформирован: {docx_path}",
                parent=tab4,
            )

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
        cfile_frame,
        text="Обзор",
        command=lambda: select_path(cfile_entry, "save_file", extension=CFILE_NAME),
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

    tab4.add_node = add_node  # type: ignore[attr-defined]
    tab4.remove_node = remove_node  # type: ignore[attr-defined]
    tab4.rename_node = rename_node  # type: ignore[attr-defined]

    return tab4


__all__ = ["create_tab4", "treeview_to_entity_nodes"]

