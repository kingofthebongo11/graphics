"""Каркас второй вкладки приложения."""

import tkinter as tk  # noqa: F401
from tkinter import ttk

from function_for_all_tabs import create_plot_canvas, plot_on_canvas
from functions_for_tab2.models import ComputedSegment


class Tab2:
    """Класс-контейнер для логики второй вкладки."""

    def __init__(self, parent: ttk.Notebook) -> None:
        self.frame = ttk.Frame(parent)
        self._init_state()

        preview_frame = ttk.Frame(self.frame)
        preview_frame.place(x=800, y=30, width=640, height=480)
        self.fig, self.ax, self.canvas = create_plot_canvas(preview_frame)

    def _init_state(self) -> None:
        """Инициализирует и хранит состояние интервалов."""
        self.intervals: list[ComputedSegment] = []

    def on_data_changed(self) -> None:
        """Колбэк, вызываемый при изменении исходных данных."""
        self.redraw_plot()

    def redraw_plot(self) -> None:
        """Перерисовывает график в соответствии с текущими данными."""
        curves = [
            {"X_values": seg.X, "Y_values": seg.Y}
            for seg in self.intervals
        ]
        if curves:
            plot_on_canvas(self.ax, self.fig, self.canvas, curves, "X", "Y")
        else:
            self.ax.clear()
            self.canvas.draw()

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

