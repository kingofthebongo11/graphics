from tkinter import ttk


def create_tab4(notebook: ttk.Notebook) -> ttk.Frame:
    """Создает четвертую вкладку приложения."""

    tab4 = ttk.Frame(notebook)
    notebook.add(tab4, text="Вкладка 4")
    return tab4
