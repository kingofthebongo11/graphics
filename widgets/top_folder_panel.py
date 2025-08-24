"""Панель свойств верхней папки."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from topfolder_codec import encode_topfolder


class TopFolderPanel(ttk.LabelFrame):
    """Панель редактирования свойств верхней папки.

    Отображает поля ``user_name``, ``entity_kind`` и ``element_type``.
    Итоговое имя папки вычисляется автоматически функцией
    :func:`encode_topfolder` и отображается только для чтения.
    """

    ELEMENT_TYPES = ("beam", "shell", "solid")
    ENTITY_KINDS = ("element", "node")

    def __init__(self, master: tk.Widget | None = None, **kwargs) -> None:
        super().__init__(master, text="Свойства", padding=5, **kwargs)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.user_name_var = tk.StringVar()
        self.entity_kind_var = tk.StringVar(value=self.ENTITY_KINDS[0])
        self.element_type_var = tk.StringVar()
        self.top_folder_var = tk.StringVar()

        ttk.Label(self, text="user_name").grid(row=0, column=0, sticky="w")
        user_entry = ttk.Entry(self, textvariable=self.user_name_var)
        user_entry.grid(row=0, column=1, sticky="ew")
        top_entry = ttk.Entry(
            self, textvariable=self.top_folder_var, state="readonly"
        )
        top_entry.grid(row=0, column=2, sticky="ew")

        ttk.Label(self, text="entity_kind").grid(row=1, column=0, sticky="w")
        entity_combo = ttk.Combobox(
            self,
            textvariable=self.entity_kind_var,
            values=self.ENTITY_KINDS,
            state="readonly",
        )
        entity_combo.grid(row=1, column=1, columnspan=2, sticky="ew")

        self._element_label = ttk.Label(self, text="element_type")
        self._element_combo = ttk.Combobox(
            self,
            textvariable=self.element_type_var,
            values=self.ELEMENT_TYPES,
            state="readonly",
        )
        self._element_label.grid(row=2, column=0, sticky="w")
        self._element_combo.grid(row=2, column=1, columnspan=2, sticky="ew")

        self.user_name_var.trace_add("write", self._update_name)
        self.entity_kind_var.trace_add("write", self._on_kind_change)
        self.element_type_var.trace_add("write", self._update_name)

        self._on_kind_change()

    def _on_kind_change(self, *_: object) -> None:
        """Показать или скрыть выбор типа элемента и пересчитать имя."""
        kind = self.entity_kind_var.get()
        if kind == "element":
            self._element_label.grid()
            self._element_combo.grid()
        else:
            self._element_label.grid_remove()
            self._element_combo.grid_remove()
            self.element_type_var.set("")
        self._update_name()

    def _update_name(self, *_: object) -> None:
        """Пересчитать имя папки."""
        user = self.user_name_var.get().strip()
        kind = self.entity_kind_var.get()
        elem = self.element_type_var.get().strip() or None
        try:
            name = encode_topfolder(user, kind, elem)
        except Exception:
            name = ""
        self.top_folder_var.set(name)


__all__ = ["TopFolderPanel"]
