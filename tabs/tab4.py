import tkinter as tk
from tkinter import ttk

from widgets import TopFolderPanel


def create_tab4(notebook: ttk.Notebook) -> ttk.Frame:
    """Создает четвертую вкладку приложения."""

    tab4 = ttk.Frame(notebook)
    notebook.add(tab4, text="Вкладка 4")

    panel = TopFolderPanel(tab4)
    panel.pack(fill=tk.X, padx=10, pady=10)

    return tab4
