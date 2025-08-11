import tkinter as tk
from tkinter import ttk


def create_tab2(notebook: ttk.Notebook) -> ttk.Frame:
    """Создаёт вкладку для построения графиков LS-DYNA."""
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Создание графиков для LS-DYNA")
    return tab2
