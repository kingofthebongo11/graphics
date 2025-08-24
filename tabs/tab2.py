"""Каркас второй вкладки приложения."""

import json
import logging
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from tabs.function_for_all_tabs import (
    create_plot_canvas,
    plot_on_canvas,
    parse_pairs_text,
)
from tabs.function_for_all_tabs.validation import ValidationError, ensure_min_length
from tabs.function_for_all_tabs.parsing_utils import parse_numbers
from tabs.functions_for_tab2 import ComputedSegment, IntervalSpec, stitch_segments
from tabs.functions_for_tab2.presets import PRESETS
from tabs.functions_for_tab2.exporting import export_curve_txt
from tabs.functions_for_tab2.segment_builder import build_segment
from widgets import select_path
from dataclasses import replace


logger = logging.getLogger(__name__)


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
        self.manual_text.bind(
            "<FocusOut>",
            lambda _e: self._update_numbers_status(
                self.manual_text, self.manual_count, highlight=True, min_count=2
            ),
        )
        ttk.Label(
            self.manual_frame,
            text="Разделители: пробел, запятая, ;\nПример: 0 1 2",
        ).pack(anchor="w", padx=5)
        self.manual_count = ttk.Label(self.manual_frame, foreground="gray")
        self.manual_count.pack(anchor="w", padx=5)
        self._text_bg = self.manual_text.cget("background")
        self._error_bg = "#ffcccc"

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
        self.array_text.bind(
            "<FocusOut>",
            lambda _e: self._update_numbers_status(
                self.array_text, self.array_count, highlight=True
            ),
        )
        ttk.Label(
            self.array_frame,
            text="Разделители: пробел, запятая, ;\nПример: 0 1 2",
        ).pack(anchor="w", padx=5)
        self.array_count = ttk.Label(self.array_frame, foreground="gray")
        self.array_count.pack(anchor="w", padx=5)

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
        self.manual_pairs_text.bind(
            "<FocusOut>",
            lambda _e: self._update_pairs_status(
                self.manual_pairs_text, self.manual_pairs_count, highlight=True
            ),
        )
        ttk.Label(
            self.manual_pairs_frame,
            text="Каждая строка: X Y\nРазделители: пробел, запятая, ;\nПример: 0 1",
        ).pack(anchor="w", padx=5)
        self.manual_pairs_count = ttk.Label(
            self.manual_pairs_frame, foreground="gray"
        )
        self.manual_pairs_count.pack(anchor="w", padx=5)

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
        self._update_numbers_status(self.manual_text, self.manual_count)
        self._update_numbers_status(self.array_text, self.array_count)
        self._update_pairs_status(self.manual_pairs_text, self.manual_pairs_count)

    # служебные методы -------------------------------------------------
    def _notify_var(self, *_args) -> None:
        if not self._updating:
            self._notify()

    def _on_text_change(self, event) -> None:
        widget = event.widget
        widget.edit_modified(False)
        if widget is self.manual_text:
            self._update_numbers_status(self.manual_text, self.manual_count)
        elif widget is self.array_text:
            self._update_numbers_status(self.array_text, self.array_count)
        elif widget is self.manual_pairs_text:
            self._update_pairs_status(
                self.manual_pairs_text, self.manual_pairs_count
            )
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

    def _update_numbers_status(
        self,
        widget: tk.Text,
        label: ttk.Label,
        *,
        highlight: bool = False,
        min_count: int = 0,
    ) -> None:
        text = widget.get("1.0", tk.END).strip()
        try:
            numbers = parse_numbers(text)
            count = len(numbers)
            if min_count and count < min_count:
                raise ValidationError(f"Нужно минимум {min_count} чисел")
            label.config(text=f"Распознано: {count} чисел", foreground="green")
            widget.configure(background=self._text_bg)
        except ValidationError as exc:
            label.config(text=f"Ошибка: {exc}", foreground="red")
            widget.configure(
                background=self._error_bg if highlight else self._text_bg
            )

    def _update_pairs_status(
        self,
        widget: tk.Text,
        label: ttk.Label,
        *,
        highlight: bool = False,
        min_count: int = 1,
    ) -> None:
        text = widget.get("1.0", tk.END).strip()
        try:
            xs, _ = parse_pairs_text(text)
            ensure_min_length(xs, min_count, name="пар")
            label.config(text=f"Распознано: {len(xs)} пар", foreground="green")
            widget.configure(background=self._text_bg)
        except ValidationError as exc:
            label.config(text=f"Ошибка: {exc}", foreground="red")
            widget.configure(
                background=self._error_bg if highlight else self._text_bg
            )

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
        self._update_numbers_status(self.manual_text, self.manual_count)
        self._update_numbers_status(self.array_text, self.array_count)
        self._update_pairs_status(self.manual_pairs_text, self.manual_pairs_count)
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


class Tab2Frame(ttk.Frame):
    """Основной виджет второй вкладки."""

    def __init__(self, parent: ttk.Notebook) -> None:
        super().__init__(parent)
        self._init_state()

        # Панель со списком интервалов и кнопками управления
        list_panel = ttk.Frame(self)
        list_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.listbox = tk.Listbox(list_panel, exportselection=False)
        self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        btns = ttk.Frame(list_panel)
        btns.pack(side=tk.TOP, fill=tk.X, pady=5)
        ttk.Button(btns, text="Добавить", command=self._add_interval).pack(fill=tk.X)
        preset_btn = ttk.Menubutton(btns, text="Добавить пресет")
        preset_menu = tk.Menu(preset_btn, tearoff=False)
        for label, factory in PRESETS.items():
            preset_menu.add_command(
                label=label, command=lambda f=factory: self._add_preset(f)
            )
        preset_btn["menu"] = preset_menu
        preset_btn.pack(fill=tk.X)
        ttk.Button(btns, text="Дублировать", command=self._duplicate_interval).pack(fill=tk.X)
        ttk.Button(btns, text="Удалить", command=self._delete_interval).pack(fill=tk.X)
        ttk.Button(btns, text="Вверх", command=lambda: self._move(-1)).pack(fill=tk.X)
        ttk.Button(btns, text="Вниз", command=lambda: self._move(1)).pack(fill=tk.X)

        # Редактор параметров
        self.editor = IntervalEditor(self, on_change=self._on_editor_change)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Область предварительного просмотра графика
        preview_frame = ttk.Frame(self)
        preview_frame.place(x=800, y=30, width=640, height=480)
        self.fig, self.ax, self.canvas = create_plot_canvas(preview_frame)

        control_frame = ttk.Frame(self)
        control_frame.place(x=800, y=520, width=640, height=40)
        # Опция выравнивания соседних сегментов по оси аргумента
        self.stitch_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            control_frame, text="Стыковать интервалы", variable=self.stitch_var
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            control_frame, text="Построить", command=self.build_segments
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            control_frame, text="Экспорт TXT", command=self.export_txt
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            control_frame, text="Сохранить проект", command=self.save_project
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            control_frame, text="Загрузить проект", command=self.load_project
        ).pack(side=tk.LEFT, padx=5)

        # Создаём первый интервал по умолчанию
        self._add_interval()

    # работа со списком интервалов ---------------------------------
    def _init_state(self) -> None:
        self.intervals: list[ComputedSegment] = []
        self.specs: list[IntervalSpec] = []
        self._next_id = 1
        self._current_index: int | None = None

    def _generate_id(self) -> int:
        iid = self._next_id
        self._next_id += 1
        return iid

    def _refresh_list(self) -> None:
        self.listbox.delete(0, tk.END)
        for i, spec in enumerate(self.specs):
            self.listbox.insert(tk.END, f"{i + 1}: id={spec.id}")
        if self._current_index is not None and self.specs:
            self.listbox.selection_set(self._current_index)

    def _add_interval(self) -> None:
        spec = IntervalSpec(id=self._generate_id(), primary_axis="X")
        self.specs.append(spec)
        self._current_index = len(self.specs) - 1
        self._refresh_list()
        self.editor.set_spec(spec)

    def _add_preset(self, factory) -> None:
        spec = factory(self._generate_id())
        self.specs.append(spec)
        self._current_index = len(self.specs) - 1
        self._refresh_list()
        self.editor.set_spec(spec)

    def _duplicate_interval(self) -> None:
        if self._current_index is None:
            return
        spec = replace(self.specs[self._current_index])
        spec.id = self._generate_id()
        self.specs.insert(self._current_index + 1, spec)
        self._current_index += 1
        self._refresh_list()
        self.editor.set_spec(spec)

    def _delete_interval(self) -> None:
        if self._current_index is None:
            return
        del self.specs[self._current_index]
        if self.specs:
            if self._current_index >= len(self.specs):
                self._current_index = len(self.specs) - 1
            self.editor.set_spec(self.specs[self._current_index])
        else:
            self._current_index = None
        self._refresh_list()

    def _move(self, delta: int) -> None:
        if self._current_index is None:
            return
        new_index = self._current_index + delta
        if 0 <= new_index < len(self.specs):
            self.specs[self._current_index], self.specs[new_index] = (
                self.specs[new_index],
                self.specs[self._current_index],
            )
            self._current_index = new_index
            self._refresh_list()

    def _on_select(self, _event) -> None:
        selection = self.listbox.curselection()
        if not selection:
            return
        self._current_index = selection[0]
        self.editor.set_spec(self.specs[self._current_index])

    def _on_editor_change(self, spec: IntervalSpec) -> None:
        if self._current_index is None:
            return
        self.specs[self._current_index] = spec
        self._refresh_list()

    # методы для работы с графиком ----------------------------------
    def build_segments(self) -> None:
        """Строит сегменты и обновляет предпросмотр."""

        if not self.specs:
            messagebox.showwarning(
                "Нет интервалов", "Добавьте хотя бы один интервал"
            )
            return

        try:
            self.intervals = [build_segment(spec) for spec in self.specs]
        except ValidationError as exc:
            messagebox.showerror("Ошибка построения", str(exc))
            return
        except Exception as exc:  # noqa: BLE001
            logger.exception("Ошибка построения сегментов")
            messagebox.showerror(
                "Ошибка построения",
                f"{exc}\nПроверьте параметры интервалов и повторите попытку.",
            )
            return

        try:
            stitched = stitch_segments(
                self.intervals,
                [spec.primary_axis for spec in self.specs],
                require_continuity=bool(self.stitch_var.get()),
            )
        except ValidationError as exc:
            messagebox.showerror("Ошибка склейки", str(exc))
            return
        except Exception as exc:  # noqa: BLE001
            logger.exception("Ошибка склейки сегментов")
            messagebox.showerror(
                "Ошибка склейки",
                f"{exc}\nПроверьте параметры и попробуйте снова.",
            )
            return

        plot_on_canvas(
            self.ax,
            self.fig,
            self.canvas,
            [{"X_values": stitched.X, "Y_values": stitched.Y}],
            "X",
            "Y",
        )

    def on_data_changed(self) -> None:
        self.redraw_plot()

    def redraw_plot(self) -> None:
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
        """Экспортирует построенную кривую в текстовый файл."""

        if not self.specs:
            messagebox.showwarning(
                "Нет интервалов", "Добавьте хотя бы один интервал"
            )
            return

        try:
            segments = [build_segment(spec) for spec in self.specs]
            stitched = stitch_segments(
                segments,
                [spec.primary_axis for spec in self.specs],
                require_continuity=bool(self.stitch_var.get()),
            )
        except ValidationError as exc:
            messagebox.showerror("Ошибка построения", str(exc))
            return
        except Exception as exc:  # noqa: BLE001
            logger.exception("Ошибка построения сегментов для экспорта")
            messagebox.showerror(
                "Ошибка построения",
                f"{exc}\nПроверьте данные и повторите попытку.",
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("TXT", "*.txt"), ("All files", "*.*")],
        )
        if not path:
            return

        precision = max(spec.precision for spec in self.specs)
        try:
            export_curve_txt(path, stitched.X, stitched.Y, precision)
            messagebox.showinfo("Успех", f"Кривая сохранена: {path}")
        except ValidationError as exc:
            messagebox.showerror("Ошибка экспорта", str(exc))
        except Exception as exc:  # noqa: BLE001
            logger.exception("Ошибка экспорта кривой")
            messagebox.showerror(
                "Ошибка экспорта",
                f"{exc}\nПроверьте путь и повторите попытку.",
            )

    def save_project(self) -> None:
        """Сохраняет текущую конфигурацию интервалов в JSON."""

        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return
        data = {
            "specs": [spec.to_dict() for spec in self.specs],
            "stitch": bool(self.stitch_var.get()),
        }
        try:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(data, fh, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успех", f"Проект сохранён: {path}")
        except Exception as exc:  # noqa: BLE001
            logger.exception("Ошибка сохранения проекта")
            messagebox.showerror(
                "Ошибка сохранения",
                f"{exc}\nУбедитесь, что путь доступен и попробуйте снова.",
            )

    def load_project(self) -> None:
        """Загружает конфигурацию интервалов из JSON."""

        path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            self.specs = [
                IntervalSpec.from_dict(d) for d in data.get("specs", [])
            ]
            self.stitch_var.set(bool(data.get("stitch", True)))
            self._next_id = max((s.id for s in self.specs), default=0) + 1
            self._current_index = 0 if self.specs else None
            self.intervals = []
            self._refresh_list()
            if self.specs:
                self.editor.set_spec(self.specs[0])
            self.redraw_plot()
            messagebox.showinfo("Успех", f"Проект загружен: {path}")
        except Exception as exc:  # noqa: BLE001
            logger.exception("Ошибка загрузки проекта")
            messagebox.showerror(
                "Ошибка загрузки",
                f"{exc}\nПроверьте файл и повторите попытку.",
            )


def create_tab2(notebook: ttk.Notebook) -> ttk.Frame:
    """Создаёт вкладку и возвращает виджет-контейнер."""
    tab = Tab2Frame(notebook)
    notebook.add(tab, text="Создание графиков для LS-DYNA")
    return tab


__all__ = ["create_tab2", "Tab2Frame", "IntervalEditor"]

