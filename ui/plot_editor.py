"""Interactive editor for matplotlib graphs using PyQt widgets.

This module provides a :class:`PlotEditor` widget that displays a matplotlib
figure alongside a :class:`QTableWidget`.  The table contains a row for each
plotted line with controls to edit its appearance:

* **Цвет** – clicking the cell opens a :class:`QColorDialog` and updates the
  line colour.
* **Тип линии** – a :class:`QComboBox` with styles ``['-', '--', '-.', ':']``.
* **Толщина** – a horizontal :class:`QSlider` with a range of ``1``–``10``.

Any change to these controls immediately updates the corresponding line and
triggers ``canvas.draw()`` so that the graph is redrawn.  When saving the
figure using ``savefig``, the current properties are preserved.
"""

from __future__ import annotations

from typing import List

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QColorDialog,
    QComboBox,
    QSlider,
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.colors as mcolors

from color_palettes import PALETTES


class PlotEditor(QWidget):
    """Widget combining a matplotlib canvas with a parameter table."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.ax = self.fig.add_subplot(111)
        self._lines: List = []

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        self.palette_combo = QComboBox()
        self.palette_combo.addItems(PALETTES.keys())
        self.palette_combo.currentTextChanged.connect(self._apply_palette)
        layout.addWidget(self.palette_combo)

        # Table with three columns: colour, line style, and width
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Цвет", "Тип линии", "Толщина"])
        self.table.cellClicked.connect(self._handle_colour_click)
        layout.addWidget(self.table)

    # ------------------------------------------------------------------
    # Plotting and table management
    # ------------------------------------------------------------------
    def plot(self, x, y, **kwargs):
        """Plot data and add a row in the table for the new line."""

        line, = self.ax.plot(x, y, **kwargs)
        self._lines.append(line)
        self._append_row(line)
        self._apply_palette(self.palette_combo.currentText())
        return line

    def _append_row(self, line) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)

        # ---- Colour cell -------------------------------------------------
        colour_item = QTableWidgetItem()
        colour_item.setFlags(Qt.ItemIsEnabled)
        colour_item.setBackground(QColor(mcolors.to_hex(line.get_color())))
        self.table.setItem(row, 0, colour_item)

        # ---- Line style selector ----------------------------------------
        style_combo = QComboBox()
        styles = ['-', '--', '-.', ':']
        style_combo.addItems(styles)
        current_style = line.get_linestyle()
        if current_style in styles:
            style_combo.setCurrentText(current_style)
        style_combo.currentTextChanged.connect(
            lambda s, ln=line: self._update_style(ln, s)
        )
        self.table.setCellWidget(row, 1, style_combo)

        # ---- Line width slider ------------------------------------------
        width_slider = QSlider(Qt.Horizontal)
        width_slider.setRange(1, 10)
        width_slider.setValue(int(line.get_linewidth()))
        width_slider.valueChanged.connect(
            lambda v, ln=line: self._update_width(ln, v)
        )
        self.table.setCellWidget(row, 2, width_slider)

    # ------------------------------------------------------------------
    def _refresh_legend(self) -> None:
        legend = self.ax.get_legend()
        if legend:
            title = legend.get_title().get_text()
            self.ax.legend(title=title)
        self.canvas.draw()

    def _apply_palette(self, name: str) -> None:
        colors = PALETTES.get(name, [])
        for idx, (line, color) in enumerate(zip(self._lines, colors)):
            line.set_color(color)
            item = self.table.item(idx, 0)
            if item is not None:
                item.setBackground(QColor(color))
        self._refresh_legend()

    # ------------------------------------------------------------------
    # Update handlers
    # ------------------------------------------------------------------
    def _handle_colour_click(self, row: int, column: int) -> None:
        if column != 0 or row >= len(self._lines):
            return

        line = self._lines[row]
        initial = QColor(mcolors.to_hex(line.get_color()))
        colour = QColorDialog.getColor(initial, self, "Выберите цвет")
        if colour.isValid():
            line.set_color(colour.name())
            item = self.table.item(row, 0)
            if item is not None:
                item.setBackground(colour)
            self._refresh_legend()

    def _update_style(self, line, style: str) -> None:
        line.set_linestyle(style)
        self._refresh_legend()

    def _update_width(self, line, width: int) -> None:
        line.set_linewidth(width)
        self.canvas.draw()

    # ------------------------------------------------------------------
    # Saving
    # ------------------------------------------------------------------
    def savefig(self, path: str, **kwargs) -> None:
        """Save the current figure to *path* using its current properties."""

        self.fig.savefig(path, **kwargs)

