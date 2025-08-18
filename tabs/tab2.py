"""Каркас второй вкладки приложения."""

import tkinter as tk  # noqa: F401
from tkinter import ttk


class Tab2:
    """Класс-контейнер для логики второй вкладки."""

    def __init__(self, parent: ttk.Notebook) -> None:
        self.frame = ttk.Frame(parent)
        self._init_state()

    def _init_state(self) -> None:
        """Инициализирует и хранит состояние интервалов."""
        self.intervals = []

    def on_data_changed(self) -> None:
        """Колбэк, вызываемый при изменении исходных данных."""
        pass

    def redraw_plot(self) -> None:
        """Перерисовывает график в соответствии с текущими данными."""
        pass

    def export_txt(self) -> None:
        """Экспортирует данные в текстовый файл."""
        pass

    def save_project(self, path: str) -> None:
        """Сохраняет проект во внешний файл."""
        pass

    def load_project(self, path: str) -> None:
        """Загружает проект из файла."""
        pass


def create_tab2(notebook: ttk.Notebook) -> ttk.Frame:
    """Создаёт вкладку и возвращает виджет-контейнер."""
    tab = Tab2(notebook)
    notebook.add(tab.frame, text="Создание графиков для LS-DYNA")
    return tab.frame


__all__ = ["create_tab2", "Tab2"]

