import tkinter as tk
from tkinter import simpledialog


class NumericIDDialog(simpledialog.Dialog):
    """Диалог ввода числового идентификатора."""

    def body(self, master):
        tk.Label(master, text="Номер элемента/узла:").grid(row=0, column=0, padx=5, pady=5)
        self.var = tk.StringVar()
        vcmd = master.register(self._on_validate)
        self.entry = tk.Entry(master, textvariable=self.var, validate="key", validatecommand=(vcmd, "%P"))
        self.entry.grid(row=0, column=1, padx=5, pady=5)
        return self.entry

    def _on_validate(self, new_value: str) -> bool:
        """Позволяет вводить только цифры."""
        if new_value.isdigit() or new_value == "":
            self.entry.config(bg="white")
            return True
        self.entry.config(bg="#ffdddd")
        return False

    def validate(self) -> bool:  # type: ignore[override]
        value = self.var.get()
        if not value.isdigit():
            self.entry.config(bg="#ffdddd")
            return False
        return True

    def apply(self) -> None:  # type: ignore[override]
        self.result = int(self.var.get())


def ask_numeric_id(parent, title: str = "Введите номер"):
    """Запросить у пользователя числовой идентификатор."""
    dialog = NumericIDDialog(parent, title)
    return dialog.result
