"""Каркас второй вкладки приложения."""

import tkinter as tk
from tkinter import ttk

from function_for_all_tabs import create_plot_canvas, plot_on_canvas
from functions_for_tab2.models import ComputedSegment, IntervalSpec
from widgets.select_path import select_path


class IntervalEditor(ttk.Frame):
    """Простейший редактор параметров одного интервала.

    Виджет предоставляет элементы управления для настройки сетки, зависимой
    координаты и параметров экспорта.  При любом изменении настроек вызывает
    переданный колбэк ``on_change`` с актуальным экземпляром
    :class:`IntervalSpec`.
    """

    def __init__(self, parent: tk.Widget, on_change) -> None:
        super().__init__(parent)
        self.on_change = on_change
        self._spec_id = 0
        self._updating = False

        # Аргумент
        axis_frame = ttk.LabelFrame(self, text="Аргумент")
        self.axis_var = tk.StringVar(value="X")
        ttk.Radiobutton(
            axis_frame, text="X", value="X", variable=self.axis_var, command=self._notify
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            axis_frame, text="Y", value="Y", variable=self.axis_var, command=self._notify
        ).pack(side=tk.LEFT, padx=5)
        axis_frame.pack(fill=tk.X, pady=5)

        # Сетка
        grid_frame = ttk.LabelFrame(self, text="Сетка")
        self.grid_kind_var = tk.StringVar(value="uniform")
        grid_box = ttk.Combobox(
            grid_frame,
            textvariable=self.grid_kind_var,
            state="readonly",
            values=["uniform", "manual", "file_pairs"],
        )
        grid_box.pack(fill=tk.X, padx=5, pady=2)
        self.grid_kind_var.trace_add("write", self._on_grid_kind_change)

        # uniform grid
        self.uniform_frame = ttk.Frame(grid_frame)
        self.start_var = tk.StringVar(value="0.0")
        self.stop_var = tk.StringVar(value="1.0")
        self.step_var = tk.StringVar(value="1.0")
        self.include_endpoint_var = tk.BooleanVar(value=True)
        ttk.Label(self.uniform_frame, text="от").grid(row=0, column=0)
        ttk.Entry(self.uniform_frame, textvariable=self.start_var, width=10).grid(
            row=0, column=1, padx=2
        )
        ttk.Label(self.uniform_frame, text="до").grid(row=0, column=2)
        ttk.Entry(self.uniform_frame, textvariable=self.stop_var, width=10).grid(
            row=0, column=3, padx=2
        )
        ttk.Label(self.uniform_frame, text="шаг").grid(row=0, column=4)
        ttk.Entry(self.uniform_frame, textvariable=self.step_var, width=10).grid(
            row=0, column=5, padx=2
        )
        ttk.Checkbutton(
            self.uniform_frame,
            text="включить конец",
            variable=self.include_endpoint_var,
            command=self._notify,
        ).grid(row=0, column=6, padx=5)
        for var in (self.start_var, self.stop_var, self.step_var):
            var.trace_add("write", self._notify_var)
        self.include_endpoint_var.trace_add("write", self._notify_var)

        # manual grid
        self.manual_frame = ttk.Frame(grid_frame)
        self.manual_text = tk.Text(self.manual_frame, height=4)
        self.manual_text.pack(fill=tk.BOTH, expand=True)
        self.manual_text.bind("<<Modified>>", self._on_text_change)

        # file_pairs grid
        self.file_frame = ttk.Frame(grid_frame)
        self.file_pairs_var = tk.StringVar()
        self.file_entry = ttk.Entry(self.file_frame, textvariable=self.file_pairs_var)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(
            self.file_frame,
            text="Обзор",
            command=lambda: select_path(self.file_entry, "file"),
        ).pack(side=tk.LEFT, padx=5)
        self.file_pairs_var.trace_add("write", self._notify_var)

        grid_frame.pack(fill=tk.BOTH, pady=5)

        # Зависимая координата
        dep_frame = ttk.LabelFrame(self, text="Зависимая координата")
        self.dep_mode_var = tk.StringVar(value="const")
        dep_box = ttk.Combobox(
            dep_frame,
            textvariable=self.dep_mode_var,
            state="readonly",
            values=["const", "array", "expr", "from_file", "manual_pairs"],
        )
        dep_box.pack(fill=tk.X, padx=5, pady=2)
        self.dep_mode_var.trace_add("write", self._on_dep_mode_change)

        self.const_frame = ttk.Frame(dep_frame)
        self.const_var = tk.StringVar(value="0.0")
        ttk.Entry(self.const_frame, textvariable=self.const_var).pack(
            fill=tk.X, padx=5, pady=2
        )
        self.const_var.trace_add("write", self._notify_var)

        self.array_frame = ttk.Frame(dep_frame)
        self.array_text = tk.Text(self.array_frame, height=4)
        self.array_text.pack(fill=tk.BOTH, expand=True)
        self.array_text.bind("<<Modified>>", self._on_text_change)

        self.expr_frame = ttk.Frame(dep_frame)
        self.expr_var = tk.StringVar()
        ttk.Entry(self.expr_frame, textvariable=self.expr_var).pack(
            fill=tk.X, padx=5, pady=2
        )
        self.expr_var.trace_add("write", self._notify_var)

        self.dep_file_frame = ttk.Frame(dep_frame)
        self.dep_file_var = tk.StringVar()
        self.dep_file_entry = ttk.Entry(self.dep_file_frame, textvariable=self.dep_file_var)
        self.dep_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(
            self.dep_file_frame,
            text="Обзор",
            command=lambda: select_path(self.dep_file_entry, "file"),
        ).pack(side=tk.LEFT, padx=5)
        self.dep_file_var.trace_add("write", self._notify_var)

        self.manual_pairs_frame = ttk.Frame(dep_frame)
        self.manual_pairs_text = tk.Text(self.manual_pairs_frame, height=4)
        self.manual_pairs_text.pack(fill=tk.BOTH, expand=True)
        self.manual_pairs_text.bind("<<Modified>>", self._on_text_change)

        dep_frame.pack(fill=tk.BOTH, pady=5)

        # Опции
        options_frame = ttk.LabelFrame(self, text="Опции")
        ttk.Label(options_frame, text="Точность").pack(side=tk.LEFT, padx=5)
        self.precision_var = tk.IntVar(value=6)
        ttk.Spinbox(options_frame, from_=0, to=15, textvariable=self.precision_var, width=5).pack(
            side=tk.LEFT
        )
        self.precision_var.trace_add("write", self._notify_var)
        self.clamp_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            options_frame,
            text="убирать NaN/Inf",
            variable=self.clamp_var,
            command=self._notify,
        ).pack(side=tk.LEFT, padx=10)
        self.clamp_var.trace_add("write", self._notify_var)
        options_frame.pack(fill=tk.X, pady=5)

        self._update_grid_visibility()
        self._update_dep_visibility()

    # служебные методы -------------------------------------------------
    def _notify_var(self, *_args) -> None:
        if not self._updating:
            self._notify()

    def _on_text_change(self, event) -> None:
        widget = event.widget
        widget.edit_modified(False)
        if not self._updating:
            self._notify()

    def _on_grid_kind_change(self, *_args) -> None:
        self._update_grid_visibility()
        self._notify_var()

    def _on_dep_mode_change(self, *_args) -> None:
        self._update_dep_visibility()
        self._notify_var()

    def _update_grid_visibility(self) -> None:
        for frame in (self.uniform_frame, self.manual_frame, self.file_frame):
            frame.pack_forget()
        kind = self.grid_kind_var.get()
        if kind == "uniform":
            self.uniform_frame.pack(fill=tk.X, padx=5, pady=2)
        elif kind == "manual":
            self.manual_frame.pack(fill=tk.BOTH, padx=5, pady=2)
        elif kind == "file_pairs":
            self.file_frame.pack(fill=tk.X, padx=5, pady=2)

    def _update_dep_visibility(self) -> None:
        for frame in (
            self.const_frame,
            self.array_frame,
            self.expr_frame,
            self.dep_file_frame,
            self.manual_pairs_frame,
        ):
            frame.pack_forget()
        mode = self.dep_mode_var.get()
        if mode == "const":
            self.const_frame.pack(fill=tk.X, padx=5, pady=2)
        elif mode == "array":
            self.array_frame.pack(fill=tk.BOTH, padx=5, pady=2)
        elif mode == "expr":
            self.expr_frame.pack(fill=tk.X, padx=5, pady=2)
        elif mode == "from_file":
            self.dep_file_frame.pack(fill=tk.X, padx=5, pady=2)
        elif mode == "manual_pairs":
            self.manual_pairs_frame.pack(fill=tk.BOTH, padx=5, pady=2)

    def _float(self, value: str, default: float = 0.0) -> float:
        try:
            return float(value)
        except ValueError:
            return default

    def _notify(self) -> None:
        if self.on_change and not self._updating:
            self.on_change(self.pull_to_spec())

    # публичные методы -------------------------------------------------
    def set_spec(self, spec: IntervalSpec) -> None:
        """Заполняет элементы управления данными интервала."""

        self._updating = True
        self._spec_id = spec.id
        self.axis_var.set(spec.primary_axis)
        self.grid_kind_var.set(spec.grid_kind)
        self.start_var.set(str(spec.start))
        self.stop_var.set(str(spec.stop))
        self.step_var.set(str(spec.step))
        self.include_endpoint_var.set(spec.include_endpoint)
        self.manual_text.delete("1.0", tk.END)
        self.manual_text.insert("1.0", spec.manual_points)
        self.file_pairs_var.set(spec.file_pairs_path)

        self.dep_mode_var.set(spec.dep_mode)
        self.const_var.set(str(spec.const_value))
        self.array_text.delete("1.0", tk.END)
        self.array_text.insert("1.0", spec.array_values)
        self.expr_var.set(spec.expr_text)
        self.dep_file_var.set(spec.dep_file_path)
        self.manual_pairs_text.delete("1.0", tk.END)
        self.manual_pairs_text.insert("1.0", spec.manual_pairs_text)

        self.precision_var.set(spec.precision)
        self.clamp_var.set(spec.clamp_finite)

        self._updating = False
        self._update_grid_visibility()
        self._update_dep_visibility()
        self._notify()

    def pull_to_spec(self) -> IntervalSpec:
        """Собирает данные из элементов управления в ``IntervalSpec``."""

        return IntervalSpec(
            id=self._spec_id,
            primary_axis=self.axis_var.get(),
            grid_kind=self.grid_kind_var.get(),
            start=self._float(self.start_var.get()),
            stop=self._float(self.stop_var.get()),
            step=self._float(self.step_var.get(), 1.0),
            include_endpoint=bool(self.include_endpoint_var.get()),
            manual_points=self.manual_text.get("1.0", tk.END).strip(),
            file_pairs_path=self.file_pairs_var.get(),
            dep_mode=self.dep_mode_var.get(),
            const_value=self._float(self.const_var.get()),
            array_values=self.array_text.get("1.0", tk.END).strip(),
            expr_text=self.expr_var.get(),
            dep_file_path=self.dep_file_var.get(),
            manual_pairs_text=self.manual_pairs_text.get("1.0", tk.END).strip(),
            precision=int(self.precision_var.get()),
            clamp_finite=bool(self.clamp_var.get()),
        )


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


__all__ = ["create_tab2", "Tab2", "IntervalEditor"]

