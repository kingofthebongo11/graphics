"""Tkinter-based plot editor for adjusting line appearance.

This widget is a simplified analogue of the Qt-based ``PlotEditor``.  It
provides controls for changing the colour, line style and width of lines in a
matplotlib ``Axes`` hosted in a Tkinter application.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

import tkinter as tk
from tkinter import ttk, colorchooser


@dataclass
class _RowWidgets:
    """Stores widgets associated with a single line."""

    frame: ttk.Frame
    label: ttk.Label
    colour: tk.Label
    style: ttk.Combobox
    width: ttk.Scale


class PlotEditor(ttk.Frame):
    """A small panel with controls for each plotted line."""

    def __init__(self, parent: tk.Widget, ax, canvas) -> None:
        super().__init__(parent)
        self.ax = ax
        self.canvas = canvas
        self._rows: List[_RowWidgets] = []

    # ------------------------------------------------------------------
    def refresh(self) -> None:
        """Rebuild the table based on current axes lines."""

        for row in self._rows:
            row.frame.destroy()
        self._rows.clear()

        for idx, line in enumerate(self.ax.lines, start=1):
            self._append_row(line, idx)

    # ------------------------------------------------------------------
    def _append_row(self, line, index: int) -> None:
        row_frame = ttk.Frame(self)
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
    def _choose_colour(self, line, label: tk.Label) -> None:
        colour_code = colorchooser.askcolor(color=line.get_color())[1]
        if colour_code:
            line.set_color(colour_code)
            label.config(bg=colour_code)
            self.canvas.draw()

    def _update_style(self, line, style: str) -> None:
        line.set_linestyle(style)
        self.canvas.draw()

    def _update_width(self, line, width: float) -> None:
        line.set_linewidth(width)
        self.canvas.draw()
