import tkinter as tk
from typing import List, Dict, Tuple, Optional

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from tabs.function_for_all_tabs import create_plot

Curve = Dict[str, List[float]]


def create_plot_canvas(parent: tk.Widget) -> Tuple[Figure, Axes, FigureCanvasTkAgg]:
    """Create a Matplotlib canvas embedded in ``parent`` widget."""
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    return fig, ax, canvas


def plot_on_canvas(
    ax: Axes,
    fig: Figure,
    canvas: FigureCanvasTkAgg,
    curves: List[Curve],
    x_label: str,
    y_label: str,
    title: str = "",
    pr_y: bool = False,
    legend: Optional[bool] = None,
) -> None:
    """Clear ``ax`` and render ``curves`` using shared style utilities."""
    ax.clear()
    create_plot(
        curves,
        x_label,
        y_label,
        title,
        pr_y=pr_y,
        fig=fig,
        ax=ax,
        legend=legend,
    )
    canvas.draw()
