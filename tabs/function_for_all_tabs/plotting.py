import logging
import warnings
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter
from settings import configure_matplotlib

from mylibproject.myutils import to_percent


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
        **kwargs: Поддержка устаревших имен параметров для обратной совместимости.
    """

    logger.info("Начало построения графика")
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
        x_label = kwargs.pop("X_label")
    if "Y_label" in kwargs:
        warnings.warn(
            "Y_label is deprecated, use y_label", DeprecationWarning, stacklevel=2
        )
        logger.warning("Использован устаревший параметр Y_label")
        y_label = kwargs.pop("Y_label")

    if fig is None:
        logger.debug("Создание новой фигуры (pr_y=%s)", pr_y)
        if pr_y:
            fig = plt.figure(figsize=(8, 4.8))
            formatter = FuncFormatter(to_percent)
            plt.gca().yaxis.set_major_formatter(formatter)
        else:
            fig = plt.figure(figsize=(6.4, 4.8))
    if ax is None:
        for curve_info in curves_info:
            plt.plot(
                curve_info["X_values"],
                curve_info["Y_values"],
                marker=None,
                linestyle="-",
            )
        plt.title(title, loc="left", fontsize=16, fontweight="bold")
        plt.xlabel(x_label, fontname="Times New Roman")
        plt.ylabel(y_label, fontname="Times New Roman")
        plt.grid(True)
        fig.tight_layout()
        fig.subplots_adjust(bottom=0.15)
        if save_file:
            logger.info("Сохранение графика в файл %s", file_plt)
            fig.savefig(file_plt)
        plt.close(fig)
        logger.info("График построен и закрыт")
    else:
        logger.debug("Построение на существующей оси (legend=%s)", legend)
        if legend:
            for curve_info in curves_info:
                ax.plot(
                    curve_info["X_values"],
                    curve_info["Y_values"],
                    marker=None,
                    linestyle="-",
                    label=curve_info["curve_legend"],
                )
        else:
            for curve_info in curves_info:
                ax.plot(
                    curve_info["X_values"],
                    curve_info["Y_values"],
                    marker=None,
                    linestyle="-",
                )
        ax.set_title(title, fontsize=16, fontweight="bold", loc="left", fontname="Times New Roman")
        ax.set_xlabel(x_label, fontname="Times New Roman")
        ax.set_ylabel(y_label, fontname="Times New Roman")
        ax.grid(True)
        fig.tight_layout()
        fig.subplots_adjust(bottom=0.15)
        if legend:
            logger.debug("Добавление легенды")
            ax.legend()
        logger.info("График построен")
