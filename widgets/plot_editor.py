"""Tkinter-панель для интерактивной настройки линий графика.

Виджет повторяет возможности Qt-версии и дополняет их отдельной панелью
фильтрации точек.  Для каждой кривой отображаются элементы управления
цветом, типом линии и толщиной, а также пара ползунков «до» и «от»,
расположенных на одной линии.  Ползунки позволяют ограничить диапазон
данных без повторного чтения файлов: исходные точки сохраняются в объекте
линии и переиспользуются при перемещении бегунков.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import List, Optional

import tkinter as tk
from tkinter import ttk, colorchooser

from color_palettes import PALETTES


@dataclass
class _RowWidgets:
    """Хранит элементы управления, связанные с одной кривой."""

    frame: ttk.Frame
    label: ttk.Label
    colour: tk.Label
    style: ttk.Combobox
    width: ttk.Scale


@dataclass
class _RangeWidgets:
    """Набор виджетов панели диапазона для одной кривой."""

    frame: ttk.Frame
    upper_scale: ttk.Scale
    lower_scale: ttk.Scale
    upper_var: tk.DoubleVar
    lower_var: tk.DoubleVar
    upper_value: tk.StringVar
    lower_value: tk.StringVar
    upper_label: ttk.Label
    lower_label: ttk.Label
    line: object
    index: int


class PlotEditor(ttk.Frame):
    """Компактная панель с настройками внешнего вида и диапазона кривых."""

    def __init__(
        self,
        parent: tk.Widget,
        ax,
        canvas,
        saved_data: Optional[List[dict]] = None,
    ) -> None:
        super().__init__(parent)
        self.ax = ax
        self.canvas = canvas
        self.saved_data = saved_data if saved_data is not None else []
        self._rows: List[_RowWidgets] = []
        self._range_controls: List[_RangeWidgets] = []
        self._range_lock = False

        self._init_range_styles()

        self.palette_combo = ttk.Combobox(
            self, values=list(PALETTES.keys()), state="readonly"
        )
        self.palette_combo.current(0)
        self.palette_combo.pack(fill=tk.X, pady=2)
        self.palette_combo.bind(
            "<<ComboboxSelected>>", lambda _e: self.apply_selected_palette()
        )

        self.row_container = ttk.Frame(self)
        self.row_container.pack(fill=tk.X, expand=False)

        self.separator = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.range_container = ttk.Frame(self)

    # ------------------------------------------------------------------
    def _init_range_styles(self) -> None:
        """Создает стили для верхнего и нижнего ползунков."""

        style = ttk.Style()
        base_layout = style.layout("Horizontal.TScale")

        def _make_layout(slider_side: str) -> list:
            layout_copy = copy.deepcopy(base_layout)

            def _patch(children: list) -> None:
                for element, options in children:
                    if element == "Scale.slider":
                        options["side"] = slider_side
                    if "children" in options:
                        _patch(options["children"])

            _patch(layout_copy)
            return layout_copy

        style.layout("RangeUpper.Horizontal.TScale", _make_layout("top"))
        style.layout("RangeLower.Horizontal.TScale", _make_layout("bottom"))

    # ------------------------------------------------------------------
    def refresh(self) -> None:
        """Перестраивает панели на основе текущих линий осей."""

        for row in self._rows:
            row.frame.destroy()
        self._rows.clear()

        for controls in self._range_controls:
            controls.frame.destroy()
        self._range_controls.clear()

        for child in self.range_container.winfo_children():
            child.destroy()
        self.separator.pack_forget()
        self.range_container.pack_forget()

        lines = list(self.ax.lines)
        for idx, line in enumerate(lines, start=1):
            self._append_row(line, idx)

        if lines:
            self.separator.pack(fill=tk.X, pady=(6, 4))
            self.range_container.pack(fill=tk.X, pady=(0, 0))
            self._build_range_controls(lines)

        self.apply_selected_palette()

    # ------------------------------------------------------------------
    def _append_row(self, line, index: int) -> None:
        row_frame = ttk.Frame(self.row_container)
        row_frame.pack(fill=tk.X, pady=2)

        name_lbl = ttk.Label(row_frame, text=f"Кривая {index}")
        name_lbl.pack(side=tk.LEFT, padx=5)

        colour_lbl = tk.Label(row_frame, bg=line.get_color(), width=4)
        colour_lbl.pack(side=tk.LEFT, padx=5)
        colour_lbl.bind(
            "<Button-1>", lambda _e, ln=line, lbl=colour_lbl: self._choose_colour(ln, lbl)
        )

        style_box = ttk.Combobox(row_frame, values=["-", "--", "-.", ":"], width=5)
        style_box.set(line.get_linestyle())
        style_box.pack(side=tk.LEFT, padx=5)
        style_box.bind(
            "<<ComboboxSelected>>",
            lambda _e, ln=line, box=style_box: self._update_style(ln, box.get()),
        )

        width_scale = ttk.Scale(row_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        width_scale.set(line.get_linewidth())
        width_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        width_scale.configure(
            command=lambda v, ln=line: self._update_width(ln, float(v))
        )

        self._rows.append(
            _RowWidgets(row_frame, name_lbl, colour_lbl, style_box, width_scale)
        )

    # ------------------------------------------------------------------
    def _build_range_controls(self, lines: List) -> None:
        header = ttk.Label(self.range_container, text="Диапазон точек, %")
        header.pack(anchor="w", padx=5)

        for idx, line in enumerate(lines, start=1):
            self._append_range_row(line, idx)

    def _append_range_row(self, line, index: int) -> None:
        frame = ttk.Frame(self.range_container)
        frame.pack(fill=tk.X, padx=5, pady=6)

        title = ttk.Label(frame, text=f"Кривая {index}")
        title.pack(side=tk.LEFT, padx=(0, 10))

        slider_holder = ttk.Frame(frame)
        slider_holder.pack(side=tk.LEFT, fill=tk.X, expand=True)

        scales_frame = ttk.Frame(slider_holder)
        scales_frame.pack(fill=tk.X)

        end_val, start_val = self._initial_range_values(line, index)

        upper_var = tk.DoubleVar(value=end_val)
        lower_var = tk.DoubleVar(value=start_val)

        upper_scale = ttk.Scale(
            scales_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            style="RangeUpper.Horizontal.TScale",
            variable=upper_var,
        )
        upper_scale.place(relx=0.0, rely=0.0, relwidth=1.0)

        lower_scale = ttk.Scale(
            scales_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            style="RangeLower.Horizontal.TScale",
            variable=lower_var,
        )
        lower_scale.place(relx=0.0, rely=0.0, relwidth=1.0)

        values_frame = ttk.Frame(frame)
        values_frame.pack(side=tk.RIGHT, padx=(10, 0))

        upper_value = tk.StringVar()
        lower_value = tk.StringVar()
        upper_label = ttk.Label(values_frame, textvariable=upper_value)
        lower_label = ttk.Label(values_frame, textvariable=lower_value)
        upper_label.pack(anchor="e")
        lower_label.pack(anchor="e")

        controls = _RangeWidgets(
            frame,
            upper_scale,
            lower_scale,
            upper_var,
            lower_var,
            upper_value,
            lower_value,
            upper_label,
            lower_label,
            line,
            index,
        )
        self._range_controls.append(controls)

        self._update_range_labels(controls)
        self._apply_range(controls)

        upper_scale.configure(
            command=lambda value, ctrl=controls: self._on_upper_change(ctrl, value)
        )
        lower_scale.configure(
            command=lambda value, ctrl=controls: self._on_lower_change(ctrl, value)
        )

    # ------------------------------------------------------------------
    def _coerce_percentage(self, value, default: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def _initial_range_values(self, line, index: int) -> tuple[float, float]:
        start = getattr(line, "_slider_start", None)
        end = getattr(line, "_slider_end", None)
        if start is None or end is None:
            if len(self.saved_data) >= index:
                saved = self.saved_data[index - 1]
                start = self._coerce_percentage(saved.get("slider_start"), 0.0)
                end = self._coerce_percentage(saved.get("slider_end"), 100.0)
            else:
                start, end = 0.0, 100.0
        start = max(0.0, min(100.0, float(start)))
        end = max(0.0, min(100.0, float(end)))
        if end < start:
            start, end = end, start
        return end, start

    def _update_range_labels(self, controls: _RangeWidgets) -> None:
        controls.upper_value.set(f"До: {controls.upper_var.get():.0f}%")
        controls.lower_value.set(f"От: {controls.lower_var.get():.0f}%")

    def _on_upper_change(self, controls: _RangeWidgets, value: str) -> None:
        if self._range_lock:
            return
        self._range_lock = True
        val = max(0.0, min(100.0, float(value)))
        controls.upper_var.set(val)
        if val < controls.lower_var.get():
            controls.lower_var.set(val)
        self._apply_range(controls)
        self._range_lock = False

    def _on_lower_change(self, controls: _RangeWidgets, value: str) -> None:
        if self._range_lock:
            return
        self._range_lock = True
        val = max(0.0, min(100.0, float(value)))
        controls.lower_var.set(val)
        if val > controls.upper_var.get():
            controls.upper_var.set(val)
        self._apply_range(controls)
        self._range_lock = False

    def _apply_range(self, controls: _RangeWidgets) -> None:
        self._update_range_labels(controls)
        start = controls.lower_var.get()
        end = controls.upper_var.get()
        self._update_saved_data(controls.index, start, end)
        self._update_line_range(controls.line, start, end)

    def _update_saved_data(self, index: int, start: float, end: float) -> None:
        if len(self.saved_data) >= index:
            self.saved_data[index - 1]["slider_start"] = start
            self.saved_data[index - 1]["slider_end"] = end

    def _update_line_range(self, line, start: float, end: float) -> None:
        full_x = getattr(line, "_full_x", None)
        full_y = getattr(line, "_full_y", None)
        if not full_x or not full_y:
            return
        if len(full_x) != len(full_y):
            return
        if len(full_x) <= 1:
            line.set_data(full_x, full_y)
        else:
            max_index = len(full_x) - 1
            start_idx = int(round(max_index * start / 100))
            end_idx = int(round(max_index * end / 100))
            if end_idx < start_idx:
                start_idx, end_idx = end_idx, start_idx
            start_idx = max(0, min(start_idx, max_index))
            end_idx = max(start_idx, min(end_idx, max_index))
            new_x = full_x[start_idx : end_idx + 1]
            new_y = full_y[start_idx : end_idx + 1]
            if not new_x or not new_y:
                return
            line.set_data(new_x, new_y)
        setattr(line, "_slider_start", start)
        setattr(line, "_slider_end", end)
        if hasattr(self.ax, "relim") and hasattr(self.ax, "autoscale_view"):
            self.ax.relim()
            self.ax.autoscale_view()
        if hasattr(self.canvas, "draw_idle"):
            self.canvas.draw_idle()
        else:
            self.canvas.draw()

    # ------------------------------------------------------------------
    def _refresh_legend(self) -> None:
        legend = self.ax.get_legend()
        if legend:
            title = legend.get_title().get_text()
            self.ax.legend(title=title)
        self.canvas.draw()

    def apply_palette(self, palette_name: str) -> None:
        colors = PALETTES.get(palette_name, [])
        for line, color, row in zip(self.ax.lines, colors, self._rows):
            line.set_color(color)
            row.colour.config(bg=color)
        self._refresh_legend()

    def apply_selected_palette(self) -> None:
        self.apply_palette(self.palette_combo.get())

    # ------------------------------------------------------------------
    def _choose_colour(self, line, label: tk.Label) -> None:
        colour_code = colorchooser.askcolor(color=line.get_color())[1]
        if colour_code:
            line.set_color(colour_code)
            label.config(bg=colour_code)
            self._refresh_legend()

    def _update_style(self, line, style: str) -> None:
        line.set_linestyle(style)
        self._refresh_legend()

    def _update_width(self, line, width: float) -> None:
        line.set_linewidth(width)
        if hasattr(self.canvas, "draw_idle"):
            self.canvas.draw_idle()
        else:
            self.canvas.draw()
