import logging
import warnings
from typing import Any, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from matplotlib.mathtext import MathTextParser
from settings import configure_matplotlib

from mylibproject.myutils import to_percent
from tabs.title_utils import split_signature


logger = logging.getLogger(__name__)


def create_plot(
    curves_info: List[Dict[str, List[float]]],
    x_label: List[Tuple[str, bool]],
    y_label: List[Tuple[str, bool]],
    title: List[Tuple[str, bool]],
    pr_y: bool = False,
    save_file: bool = False,
    file_plt: str = "",
    fig: Optional[Figure] = None,
    ax: Optional[Axes] = None,
    legend: Optional[bool] = None,
    title_fontstyle: str = "normal",
    **kwargs: Any,
) -> None:
    """Create a plot based on provided curve data.

    Parameters:
        curves_info: Список словарей с данными кривых. Каждый словарь должен
            содержать ключи ``'X_values'`` и ``'Y_values'``.
        x_label: Подпись оси X (список сегментов ``split_signature``).
        y_label: Подпись оси Y (список сегментов ``split_signature``).
        title: Заголовок графика (список сегментов ``split_signature``).
        pr_y: Если ``True``, значения Y отображаются в процентах.
        save_file: Флаг сохранения графика в файл.
        file_plt: Путь к файлу для сохранения графика.
        fig: Существующая фигура для построения графика.
        ax: Существующая ось для построения графика.
        legend: Отображать легенду при наличии ``ax``.
        title_fontstyle: Стиль шрифта заголовка.
        **kwargs: Поддержка устаревших имен параметров для обратной совместимости.
    """

    logger.info("Начало построения графика")
    old_usetex = plt.rcParams.get("text.usetex", False)
    configure_matplotlib()
    if "prY" in kwargs:
        warnings.warn("prY is deprecated, use pr_y", DeprecationWarning, stacklevel=2)
        logger.warning("Использован устаревший параметр prY")
        pr_y = kwargs.pop("prY")
    if "savefile" in kwargs:
        warnings.warn(
            "savefile is deprecated, use save_file", DeprecationWarning, stacklevel=2
        )
        logger.warning("Использован устаревший параметр savefile")
        save_file = kwargs.pop("savefile")
    if "X_label" in kwargs:
        warnings.warn(
            "X_label is deprecated, use x_label", DeprecationWarning, stacklevel=2
        )
        logger.warning("Использован устаревший параметр X_label")
        x_label = split_signature(kwargs.pop("X_label"), bold=False)
    if "Y_label" in kwargs:
        warnings.warn(
            "Y_label is deprecated, use y_label", DeprecationWarning, stacklevel=2
        )
        logger.warning("Использован устаревший параметр Y_label")
        y_label = split_signature(kwargs.pop("Y_label"), bold=False)

    try:
        parser = MathTextParser("agg")
        for frag, is_latex in x_label:
            if not is_latex:
                continue
            try:
                parser.parse(frag)
            except ValueError as exc:
                message = f"Некорректная LaTeX-формула в подписи оси X: {frag}"
                logger.error(message)
                raise ValueError(message) from exc
        for frag, is_latex in y_label:
            if not is_latex:
                continue
            try:
                parser.parse(frag)
            except ValueError as exc:
                message = f"Некорректная LaTeX-формула в подписи оси Y: {frag}"
                logger.error(message)
                raise ValueError(message) from exc
        for frag, is_latex in title:
            if not is_latex:
                continue
            try:
                parser.parse(frag)
            except ValueError as exc:
                message = f"Некорректная LaTeX-формула в заголовке: {frag}"
                logger.error(message)
                raise ValueError(message) from exc

        for frag, is_latex in (*x_label, *y_label, *title):
            if not is_latex and "$" in frag:
                message = f"Некорректная LaTeX-формула: {frag}"
                logger.error(message)
                raise ValueError(message) from ValueError(message)

        created_fig = fig is None
        if fig is None:
            logger.debug("Создание новой фигуры (pr_y=%s)", pr_y)
            if pr_y:
                fig, ax = plt.subplots(figsize=(8, 4.8))
                formatter = FuncFormatter(to_percent)
                ax.yaxis.set_major_formatter(formatter)
            else:
                fig, ax = plt.subplots(figsize=(6.4, 4.8))
        if ax is None:
            ax = fig.gca()

        if legend:
            for curve_info in curves_info:
                ax.plot(
                    curve_info["X_values"],
                    curve_info["Y_values"],
                    marker=None,
                    linestyle="-",
                    label=curve_info.get("curve_legend"),
                )
        else:
            for curve_info in curves_info:
                ax.plot(
                    curve_info["X_values"],
                    curve_info["Y_values"],
                    marker=None,
                    linestyle="-",
                )

        fig.canvas.draw()

        def _render_segments(
            segments: List[Tuple[str, bool]],
            *,
            x: float,
            y: float,
            vertical: bool = False,
            rotation: float = 0.0,
            **text_kwargs: Any,
        ) -> None:
            trans = ax.transAxes
            renderer = fig.canvas.get_renderer()
            for frag, is_latex in segments:
                if is_latex:
                    txt = ax.text(
                        x,
                        y,
                        f"${frag}$",
                        transform=trans,
                        usetex=True,
                        rotation=rotation,
                        **text_kwargs,
                    )
                    try:
                        bbox = txt.get_window_extent(renderer=renderer)
                    except RuntimeError:
                        txt.remove()
                        txt = ax.text(
                            x,
                            y,
                            f"${frag}$",
                            transform=trans,
                            usetex=False,
                            rotation=rotation,
                            **text_kwargs,
                        )
                        bbox = txt.get_window_extent(renderer=renderer)
                else:
                    with mpl.rc_context(
                        {"text.usetex": False, "font.family": "Times New Roman"}
                    ):
                        txt = ax.text(
                            x,
                            y,
                            frag,
                            transform=trans,
                            rotation=rotation,
                            **text_kwargs,
                        )
                        bbox = txt.get_window_extent(renderer=renderer)
                if vertical:
                    dy = (
                        ax.transAxes.inverted().transform((0, bbox.height))[1]
                        - ax.transAxes.inverted().transform((0, 0))[1]
                    )
                    y -= dy
                else:
                    dx = (
                        ax.transAxes.inverted().transform((bbox.width, 0))[0]
                        - ax.transAxes.inverted().transform((0, 0))[0]
                    )
                    x += dx

        def _segments_width(segments: List[Tuple[str, bool]]) -> float:
            """Вычислить суммарную ширину сегментов в координатах осей."""
            trans = ax.transAxes
            renderer = fig.canvas.get_renderer()
            total = 0.0
            for frag, is_latex in segments:
                if is_latex:
                    txt = ax.text(
                        0.0,
                        0.0,
                        f"${frag}$",
                        transform=trans,
                        usetex=True,
                        ha="left",
                        va="center",
                    )
                    try:
                        bbox = txt.get_window_extent(renderer=renderer)
                    except RuntimeError:
                        txt.remove()
                        txt = ax.text(
                            0.0,
                            0.0,
                            f"${frag}$",
                            transform=trans,
                            usetex=False,
                            ha="left",
                            va="center",
                        )
                        bbox = txt.get_window_extent(renderer=renderer)
                else:
                    with mpl.rc_context(
                        {"text.usetex": False, "font.family": "Times New Roman"}
                    ):
                        txt = ax.text(
                            0.0,
                            0.0,
                            frag,
                            transform=trans,
                            ha="left",
                            va="center",
                        )
                        bbox = txt.get_window_extent(renderer=renderer)
                dx = (
                    ax.transAxes.inverted().transform((bbox.width, 0))[0]
                    - ax.transAxes.inverted().transform((0, 0))[0]
                )
                total += dx
                txt.remove()
            return total

        _render_segments(
            title,
            x=0.0,
            y=1.02,
            fontweight="bold",
            fontstyle=title_fontstyle,
            fontsize=16,
            ha="left",
            va="bottom",
        )
        width = _segments_width(x_label)
        start_x = 0.5 - width / 2
        _render_segments(
            x_label,
            x=start_x,
            y=-0.1,
            fontweight="normal",
            fontstyle="normal",
            fontsize=12,
            ha="left",
            va="center",
        )
        _render_segments(
            y_label,
            x=-0.1,
            y=1.0,
            vertical=True,
            rotation=90,
            fontweight="normal",
            fontstyle="normal",
            fontsize=12,
            ha="center",
            va="top",
        )

        ax.grid(True)
        fig.tight_layout()
        fig.subplots_adjust(bottom=0.15)
        if legend:
            logger.debug("Добавление легенды")
            ax.legend()
        if save_file:
            logger.info("Сохранение графика в файл %s", file_plt)
            fig.savefig(file_plt)
        if created_fig:
            plt.close(fig)
            logger.info("График построен и закрыт")
        else:
            logger.info("График построен")
    finally:
        plt.rcParams["text.usetex"] = old_usetex
