import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

import logging

from mylibproject.myutils import to_percent
from widgets.text_widget import create_text, clear_text
from tabs.tab3 import create_tab3
from tabs.tab2 import create_tab2
from tabs.tab1 import create_tab1







def configure_matplotlib():
    """Configure global matplotlib settings used across the application."""
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 14  # Общий размер шрифта
    plt.rcParams['axes.titlesize'] = 14  # Размер шрифта для заголовков осей
    plt.rcParams['axes.labelsize'] = 14  # Размер шрифта для подписей осей
    plt.rcParams['xtick.labelsize'] = 14  # Размер шрифта для меток оси X
    plt.rcParams['ytick.labelsize'] = 14  # Размер шрифта для меток оси Y
    plt.rcParams['legend.fontsize'] = 14  # Размер шрифта для легенды





def create_plot(curves_info, X_label, Y_label, title, prY=False, savefile=False, file_plt='', fig=None, ax=None, legend=None):
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
                ax.plot(curve_info['X_values'], curve_info['Y_values'], marker=None, linestyle='-', label=curve_info['curve_legend'])
        else:
            for curve_info in curves_info:
                ax.plot(curve_info['X_values'], curve_info['Y_values'], marker=None, linestyle='-')
        ax.set_title(title, fontsize=16, fontweight='bold', loc='left')
        # Обработка названий осей
        ax.set_xlabel(X_label)
        ax.set_ylabel(Y_label)
        ax.grid(True)
        fig.tight_layout()
        fig.subplots_adjust(bottom=0.15)
        # Условное добавление легенды в зависимости от состояния чекбокса
        if legend:
            ax.legend()
def on_closing(root):
    root.quit()  # Останавливаем цикл Tkinter
    root.destroy()  # Уничтожаем окно


def main():
    configure_matplotlib()
    # Создание главного окна
    root = tk.Tk()
    root.geometry("1500x1100")
    root.title("Работа с графиками")
    root.resizable(True, True)

    # Создание вкладок
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill=tk.BOTH)

    # Добавляем вкладки
    create_tab1(notebook, create_text)
    create_tab2(notebook)

    create_tab3(notebook, create_text, clear_text)

    # Привязка обработчика закрытия окна
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    # Запуск окна
    root.mainloop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
