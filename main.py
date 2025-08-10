import tkinter as tk
from tkinter import ttk

import openpyxl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import os
from pathlib import Path


import logging

from mylibproject.Figurenameclass import FigureNames

from mylibproject.myutils import to_percent

from mylibproject.myutils_work_with_file import extract_data_frec_from_file

from mylibproject.myutils_widgets import make_context_menu, message_log, add_hotkeys
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





def create_text(parent, method='text', height=10, wrap='word', state='normal', scrollbar=False, max_lines=0):
    """Создает текстовое поле с возможностью прокрутки и контекстного меню."""
    # Создаем текстовое поле с заданными параметрами
    if method == 'entry':
        text_widget = tk.Entry(parent, state=state)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Заполнение области фрейма

    elif method == 'text':
        text_widget = tk.Text(parent, height=height, wrap=wrap, state=state)
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Заполнение области фрейма
        if max_lines > 0:
            def limit_text_lines(text_widget, max_lines):
                """Ограничивает количество строк в текстовом поле."""

                def check_lines(event):
                    if max_lines > 0:
                        current_text = text_widget.get("1.0", tk.END)  # Получаем текущий текст
                        lines = current_text.splitlines()  # Разбиваем на строки
                        if len(lines) > max_lines:  # Если строк больше чем допустимо
                            text_widget.delete(f"{max_lines + 1}.0", tk.END)  # Удаляем лишние строки

                text_widget.bind("<KeyRelease>", check_lines)  # Проверяем после каждой клавиши
            limit_text_lines(text_widget, max_lines)  # Применяем ограничение по количеству строк

        if scrollbar:
            def bind_scrollbar(log_text, log_scrollbar):
                def update_scrollbar(log_text, log_scrollbar):
                    # Обновление позиции и размера скроллбара в зависимости от содержимого текстового поля
                    log_scrollbar.config(command=log_text.yview)
                    log_text['yscrollcommand'] = log_scrollbar.set

                # Привязываем события к текстовому полю и скроллбару
                log_text.bind("<KeyRelease>", lambda event: update_scrollbar(log_text, log_scrollbar))
                log_text.bind("<MouseWheel>", lambda event: update_scrollbar(log_text, log_scrollbar))
                log_text.bind("<Configure>", lambda event: update_scrollbar(log_text, log_scrollbar))
            # Создаем и размещаем скроллбар, если требуется
            text_scrollbar = ttk.Scrollbar(parent, command=text_widget.yview)
            text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Размещение скроллбара справа
            text_widget['yscrollcommand'] = text_scrollbar.set  # Привязываем скроллбар к текстовому полю
            bind_scrollbar(text_widget, text_scrollbar)  # Привязываем события для скроллбара
    else:
        raise ValueError("Некорректное значение параметра method. Должно быть 'entry' или 'text'.")
    # Применяем контекстное меню к текстовому полю
    make_context_menu(text_widget)
    # Добавляем горячие клавиши для текстового поля
    add_hotkeys(text_widget)
    return text_widget


def clear_text(text_widget):
    """
    Функция для очистки текстового виджета (лога).

    :param text_widget: Виджет текста для очистки.
    """
    text_widget.config(state='normal')  # Разрешаем редактирование
    text_widget.delete(1.0, tk.END)  # Удаляем весь текст
    text_widget.config(state='disabled')  # Запрещаем редактирование


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


def create_txt_file_with_result(file_out_txt, data_for_file, log_text):
    with open(file_out_txt, 'w') as file:
        for name, graph in data_for_file.items():
            file.write(str(name) + '\n')
            for time_value in graph:
                file.write(str(time_value) + '\n')
            file.write('\n')
    message_log(log_text, "Создан текстовый файл со всеми параметрами")


def create_xlsx_file_with_result(file_out_xlsx, data_for_file, log_text):
    # Создаем новый Excel файл
    wb = openpyxl.Workbook()
    ws = wb.active

    # Записываем данные в Excel
    row = 1
    for name, graph in data_for_file.items():
        names = name.split()
        for i, word in enumerate(names):
            header_cell = ws.cell(row=row, column=i + 1)
            header_cell.value = str(word)  # Записываем название
        row += 1
        for time_value in graph:
            for i, value in enumerate(time_value):
                if isinstance(value, str):
                    if value[-1] == '%':
                        value = value[:-1]
                ws.cell(row=row, column=i + 1).value = float(value)  # Записываем данные
            row += 1
        row += 1  # Пропускаем строку для разделения графов

    # Сохраняем файл
    wb.save(file_out_xlsx)
    message_log(log_text, "Создан эксель файл со всеми параметрами")


def create_png_plots(graph_with_time, file_path_outeig, log_text):
    for name, graph in graph_with_time.items():
        X_values = [float(item[0]) for item in graph]
        xlabel = 'Время $t$, с'
        namefig = FigureNames(name)

        # Список ключей для проверки в name
        keys = ['XR', 'YR', 'ZR', 'X', 'Y', 'Z']
        # Цикл для проверки каждого ключа в списке
        for key in keys:
            if key in name:
                directory = os.path.join(file_path_outeig, key)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                file_plt = os.path.join(directory, f'{namefig.generate_filename()}.png')
                break  # Выход из цикла после первого совпадения
        if 'pr' in name:
            Y_values = [float(value[1].strip('%')) if isinstance(value[1], str) else value[1] for value in graph]
            curves_info = [{
                'X_values': X_values,
                'Y_values': Y_values
            }]
            create_plot(curves_info, xlabel, namefig.generate_plot_ylabel(), namefig.generate_plot_title(),
                        True, True, file_plt)
        else:
            Y_values = [float(item[1]) for item in graph]
            curves_info = [{
                'X_values': X_values,
                'Y_values': Y_values
            }]
            create_plot(curves_info, xlabel, namefig.generate_plot_ylabel(), namefig.generate_plot_title(),
                        False, True, file_plt)

    message_log(log_text, "Созданы графики всех характеристик")


def function1(log_text, path_entry):
    # Вывод текста в окно логов
    file_path_str = path_entry.get()
    if file_path_str:
        file_path = Path(file_path_str)
        message_log(log_text, f"Выбранный путь к проетку LS-Dyna: {file_path}")
        file_path_outeig = file_path / "eigresults"
        file_out_txt = file_path_outeig / "eigoutput.txt"
        file_out_xlsx = file_path_outeig / "eigoutput.xlsx"
        file_path_outeig.mkdir(parents=True, exist_ok=True)
        all_frequencies = []
        all_modal_mass = []
        time_data = []
        index = 1
        while True:
            file_name = f"eigout{index}"
            try:
                data_freq = extract_data_frec_from_file(file_path, file_name)
                frequencies = data_freq['cycles_values']
                modal_data = data_freq['modal_data']
                time = data_freq['time']
                time_data.append(time)
                all_modal_mass.append(modal_data)
                all_frequencies.append(frequencies)
                index += 1
            except FileNotFoundError:
                if index == 1:
                    message_log(log_text, "В данной папке нет расчетных файлов по частотному анализу")
                    return
                else:
                    n_file = index - 1
                    message_log(log_text, f"eigout{index} не найден. Значит последний eigout{n_file}")
                    message_log(log_text, "Точки во времени для модального анализа:")
                    message_log(log_text, str(time_data))
                break
        graphs = {
            "Xmass": [],
            "totalprXmass": [],
            "Ymass": [],
            "totalprYmass": [],
            "Zmass": [],
            "totalprZmass": [],
            "XRmass": [],
            "totalprXRmass": [],
            "YRmass": [],
            "totalprYRmass": [],
            "ZRmass": [],
            "totalprZRmass": [],
            "Xeig": [],
            "Yeig": [],
            "Zeig": [],
            "XReig": [],
            "YReig": [],
            "ZReig": [],
            "XN": [],
            "YN": [],
            "ZN": [],
            "XRN": [],
            "YRN": [],
            "ZRN": [],
            "prXmass": [],
            "prYmass": [],
            "prZmass": [],
            "prXRmass": [],
            "prYRmass": [],
            "prZRmass": [],
        }
        for mass, frequencies in zip(all_modal_mass, all_frequencies):
            onecoord = {
                "Xmass": 0,
                "Ymass": 0,
                "Zmass": 0,
                "XRmass": 0,
                "YRmass": 0,
                "ZRmass": 0,
            }
            for i, item in enumerate(mass):
                for key, value in item.items():
                    if key in ["X", "Y", "Z", "XR", "YR", "ZR"]:
                        if float(value) > onecoord[key + 'mass']:
                            onecoord[key + 'mass'] = float(value)
                            onecoord[key + 'eig'] = frequencies[int(item['N']) - 1]
                            onecoord[key + 'N'] = item['N']
                            onecoord['pr' + key + 'mass'] = item['pr' + key]
                            if i > 0:
                                onecoord['pr' + key + 'mass'] = str(float(onecoord['pr' + key + 'mass'].strip('%')) - float(
                                    mass[i - 1]['pr' + key].strip('%')))+'%'
                        onecoord['totalpr' + key + 'mass'] = item['pr' + key]

            for key, value in onecoord.items():
                if key in graphs:
                    graphs[key].append(value)
        data_for_file = {
            't XN Xeig Xmass prXmass totalprXmass': [],
            't YN Yeig Ymass prYmass totalprYmass': [],
            't ZN Zeig Zmass prZmass totalprZmass': [],
            't XRN XReig XRmass prXRmass totalprXRmass': [],
            't YRN YReig YRmass prYRmass totalprYRmass': [],
            't ZRN ZReig ZRmass prZRmass totalprZRmass': []
        }
        for i in range(n_file):
            for s in ['X', 'Y', 'Z', 'XR', 'YR', 'ZR']:
                data_for_file[f't {s}N {s}eig {s}mass pr{s}mass totalpr{s}mass'].append(
                    [time_data[i], graphs[f'{s}N'][i], graphs[f'{s}eig'][i], graphs[f'{s}mass'][i],
                     graphs[f'pr{s}mass'][i], graphs[f'totalpr{s}mass'][i]])

        graph_with_time = {
        }
        for key, graph in graphs.items():
            values_with_time = []
            for time, value in zip(time_data, graph):
                values_with_time.append([time, value])
            graph_with_time[key] = values_with_time
        # Создаем изображения графиков результатов
        create_png_plots(graph_with_time, file_path_outeig, log_text)

        # Создаем текстовый файл результатов
        create_txt_file_with_result(file_out_txt, data_for_file, log_text)
        # Создаем эксель файл результатов
        create_xlsx_file_with_result(file_out_xlsx, data_for_file, log_text)

    else:
        message_log(log_text, "Вы не выбрали путь к проетку LS-Dyna, выберите путь в ячейке выше...")


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

    create_tab3(notebook, create_text, function1, clear_text)

    # Привязка обработчика закрытия окна
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    # Запуск окна
    root.mainloop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
