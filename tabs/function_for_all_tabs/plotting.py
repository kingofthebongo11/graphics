import logging
import warnings
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from matplotlib.mathtext import MathTextParser
from settings import configure_matplotlib

from mylibproject.myutils import to_percent
from tabs.title_utils import format_signature


logger = logging.getLogger(__name__)


def create_plot(
    curves_info: List[Dict[str, List[float]]],
    x_label: str,
    y_label: str,
    title: str,
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
        x_label: Подпись оси X.
        y_label: Подпись оси Y.
        title: Заголовок графика.
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
        x_label = format_signature(kwargs.pop("X_label"), bold=False)
    if "Y_label" in kwargs:
        warnings.warn(
            "Y_label is deprecated, use y_label", DeprecationWarning, stacklevel=2
        )
        logger.warning("Использован устаревший параметр Y_label")
        y_label = format_signature(kwargs.pop("Y_label"), bold=False)

    try:
        parser = MathTextParser("agg")
        for text, desc in (
            (x_label, "подписи оси X"),
            (y_label, "подписи оси Y"),
            (title, "заголовке"),
        ):
            try:
                parser.parse(text)
            except ValueError as exc:
                message = f"Некорректная LaTeX-формула в {desc}: {text}"
                logger.error(message)
                raise ValueError(message) from exc

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

        try:
            ax.set_title(
                title,
                fontweight="bold",
                fontstyle=title_fontstyle,
                fontsize=16,
                loc="left",
                usetex=True,
            )
        except RuntimeError:
            ax.set_title(
                title,
                fontweight="bold",
                fontstyle=title_fontstyle,
                fontsize=16,
                loc="left",
                usetex=False,
            )
        try:
            ax.set_xlabel(
                x_label,
                fontweight="normal",
                fontstyle="normal",
                fontsize=12,
                usetex=True,
            )
        except RuntimeError:
            ax.set_xlabel(
                x_label,
                fontweight="normal",
                fontstyle="normal",
                fontsize=12,
                usetex=False,
            )
        try:
            ax.set_ylabel(
                y_label,
                fontweight="normal",
                fontstyle="normal",
                fontsize=12,
                usetex=True,
            )
        except RuntimeError:
            ax.set_ylabel(
                y_label,
                fontweight="normal",
                fontstyle="normal",
                fontsize=12,
                usetex=False,
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
