import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from mylibproject.myutils import to_percent


def create_plot(curves_info, X_label, Y_label, title, prY=False, savefile=False,
                file_plt='', fig=None, ax=None, legend=None):
    """Create a plot based on provided curve data.

    Parameters:
        curves_info (list[dict]): Список словарей с данными кривых. Каждый словарь должен
            содержать ключи ``'X_values'`` и ``'Y_values'``.
        X_label (str): Подпись оси X.
        Y_label (str): Подпись оси Y.
        title (str): Заголовок графика.
        prY (bool, optional): Если ``True``, значения Y отображаются в процентах.
        savefile (bool, optional): Флаг сохранения графика в файл.
        file_plt (str, optional): Путь к файлу для сохранения графика.
        fig (matplotlib.figure.Figure, optional): Существующая фигура для построения графика.
        ax (matplotlib.axes.Axes, optional): Существующая ось для построения графика.
        legend (bool, optional): Отображать легенду при наличии ``ax``.
    """
    if fig is None:
        if prY:
            fig = plt.figure(figsize=(8, 4.8))
            formatter = FuncFormatter(to_percent)
            plt.gca().yaxis.set_major_formatter(formatter)
        else:
            fig = plt.figure(figsize=(6.4, 4.8))
    if ax is None:
        for curve_info in curves_info:
            plt.plot(curve_info['X_values'], curve_info['Y_values'], marker=None, linestyle='-')
        plt.title(title, loc='left', fontsize=16, fontweight='bold')
        plt.xlabel(X_label)
        plt.ylabel(Y_label)
        plt.grid(True)
        fig.tight_layout()
        fig.subplots_adjust(bottom=0.15)
        if savefile:
            fig.savefig(file_plt)
        plt.close(fig)
    else:
        if legend:
            for curve_info in curves_info:
                ax.plot(curve_info['X_values'], curve_info['Y_values'], marker=None, linestyle='-',
                        label=curve_info['curve_legend'])
        else:
            for curve_info in curves_info:
                ax.plot(curve_info['X_values'], curve_info['Y_values'], marker=None, linestyle='-')
        ax.set_title(title, fontsize=16, fontweight='bold', loc='left')
        ax.set_xlabel(X_label)
        ax.set_ylabel(Y_label)
        ax.grid(True)
        fig.tight_layout()
        fig.subplots_adjust(bottom=0.15)
        if legend:
            ax.legend()
