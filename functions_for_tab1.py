import ast
import numpy as np
import logging
from tkinter import ttk, filedialog, messagebox

from mylibproject.myutils_widgets import select_path

logger = logging.getLogger(__name__)


def on_combobox_event(event, *callbacks):
    """Вызывает все переданные функции-обработчики последовательно."""
    for callback in callbacks:
        if callable(callback):
            try:
                callback(event)
            except TypeError:
                callback()


def on_combo_change_curve_type(frame, combo, label_curve_typeX, combo_curve_typeX, label_curve_typeY, combo_curve_typeY,
                               label_curve_typeX_type, combo_curve_typeX_type, label_curve_typeY_type,
                               combo_curve_typeY_type):
    if combo.get() == "Частотный анализ":
        if not label_curve_typeX.winfo_viewable():  # Проверяем, отображается ли виджет
            frame.update_idletasks()
            label_curve_typeX.place(x=combo.winfo_x() + 170,
                                    y=combo.winfo_y() - 20)  # Отступ от типа кривой

            combo_curve_typeX.place(x=combo.winfo_x() + 170,
                                    y=combo.winfo_y(), width=150)  # Позиция для X
            label_curve_typeX_type.place(x=combo.winfo_x() + 170,
                                         y=combo.winfo_y() + 25)  # Отступ от параметра X
            combo_curve_typeX_type.place(x=combo.winfo_x() + 170,
                                         y=combo.winfo_y() + 45, width=150)  # Позиция для Y
            frame.update_idletasks()
            label_curve_typeY.place(x=combo_curve_typeX_type.winfo_x() + 170,
                                    y=combo.winfo_y() - 20)  # Отступ от параметра X
            combo_curve_typeY.place(x=combo_curve_typeX_type.winfo_x() + 170,
                                    y=combo.winfo_y(), width=150)  # Позиция для Y
            label_curve_typeY_type.place(x=combo_curve_typeX_type.winfo_x() + 170,
                                         y=combo.winfo_y() + 25)  # Отступ от параметра X
            combo_curve_typeY_type.place(x=combo_curve_typeX_type.winfo_x() + 170,
                                         y=combo.winfo_y() + 45, width=150)  # Позиция для Y
    else:
        label_curve_typeX.place_forget()
        combo_curve_typeX.place_forget()
        label_curve_typeY.place_forget()
        combo_curve_typeY.place_forget()
        label_curve_typeX_type.place_forget()
        combo_curve_typeX_type.place_forget()
        label_curve_typeY_type.place_forget()
        combo_curve_typeY_type.place_forget()


def create_curve_box(input_frame, i, checkbox_var, saved_data):
    """Создает ячейку для настройки параметров кривой."""
    from main import create_text  # локальный импорт для избегания циклической зависимости

    # Определяем высоту ячейки на основе состояния чекбокса
    dy = 190 if checkbox_var.get() else 130

    # Метка о параметрах кривой
    label_curve_box = ttk.Label(input_frame, text=f"Настройка параметров кривой {i}:")
    label_curve_box.place(x=10, y=0 + dy * (i - 1))

    # Метка о выборе типа кривой
    label_curve_type = ttk.Label(input_frame, text=f"Выберите тип кривой {i}:")
    label_curve_type.place(x=10, y=30 + dy * (i - 1))

    # Создание выпадающего меню для типа кривой
    combo_curve_type = ttk.Combobox(input_frame, values=["Частотный анализ", "2", "3"], state='readonly')
    combo_curve_type.place(x=250, y=30 + dy * (i - 1), width=150)
    combo_curve_type._name = f"curve_{i}_type"

    # Создание элементов для параметров X и Y
    label_curve_typeX = ttk.Label(input_frame, text="Выберите параметр для Х:")
    combo_curve_typeX = ttk.Combobox(input_frame, values=["Время", "Номер доминантной частота", "Частота",
                                                          "Масса", "Процент от общей массы", "Процент общей массы"],
                                     state='readonly')
    combo_curve_typeX._name = f"curve_{i}_typeXF"
    label_curve_typeY = ttk.Label(input_frame, text="Выберите параметр для Y:")
    combo_curve_typeY = ttk.Combobox(input_frame, values=["Время", "Номер доминантной частота", "Частота",
                                                          "Масса", "Процент от общей массы", "Процент общей массы"],
                                     state='readonly')
    combo_curve_typeY._name = f"curve_{i}_typeYF"
    label_curve_typeX_type = ttk.Label(input_frame, text="По какой оси:")
    combo_curve_typeX_type = ttk.Combobox(input_frame, values=["X", "Y", "Z", "XR", "YR", "ZR"],
                                          state='readonly')
    combo_curve_typeX_type._name = f"curve_{i}_typeXFtype"
    label_curve_typeY_type = ttk.Label(input_frame, text="По какой оси:")
    combo_curve_typeY_type = ttk.Combobox(input_frame, values=["X", "Y", "Z", "XR", "YR", "ZR"],
                                          state='readonly')
    combo_curve_typeY_type._name = f"curve_{i}_typeYFtype"

    # Установка позиций для параметров X и Y
    input_frame.update_idletasks()
    label_curve_typeX.place(x=combo_curve_type.winfo_x() + 170,
                            y=combo_curve_type.winfo_y() - 20)  # Отступ от типа кривой
    combo_curve_typeX.place(x=combo_curve_type.winfo_x() + 170,
                            y=combo_curve_type.winfo_y(), width=150)  # Позиция для X
    label_curve_typeX_type.place(x=combo_curve_type.winfo_x() + 170,
                                 y=combo_curve_type.winfo_y() + 25)  # Отступ от параметра X
    combo_curve_typeX_type.place(x=combo_curve_type.winfo_x() + 170,
                                 y=combo_curve_type.winfo_y() + 45, width=150)  # Позиция для оси X
    input_frame.update_idletasks()
    label_curve_typeY.place(x=combo_curve_typeX_type.winfo_x() + 170,
                            y=combo_curve_type.winfo_y() - 20)  # Отступ от параметра X
    combo_curve_typeY.place(x=combo_curve_typeX_type.winfo_x() + 170,
                            y=combo_curve_type.winfo_y(), width=150)  # Позиция для Y
    label_curve_typeY_type.place(x=combo_curve_typeX_type.winfo_x() + 170,
                                 y=combo_curve_type.winfo_y() + 25)  # Отступ от параметра X
    combo_curve_typeY_type.place(x=combo_curve_typeX_type.winfo_x() + 170,
                                 y=combo_curve_type.winfo_y() + 45, width=150)  # Позиция для оси Y

    # Привязка события изменения выбора в combo_curve_type
    combo_curve_type.bind("<<ComboboxSelected>>",
                          lambda event: on_combobox_event(event,
                                                          lambda e: on_combo_change_curve_type(input_frame,
                                                                                               combo_curve_type,
                                                                                               label_curve_typeX,
                                                                                               combo_curve_typeX,
                                                                                               label_curve_typeY,
                                                                                               combo_curve_typeY,
                                                                                               label_curve_typeX_type,
                                                                                               combo_curve_typeX_type,
                                                                                               label_curve_typeY_type,
                                                                                               combo_curve_typeY_type),
                                                          lambda e: saved_data[i - 1].update(
                                                              {'curve_type': combo_curve_type.get()})))

    # Метка для выбора файла с кривой
    label_path = ttk.Label(input_frame, text="Выберите файл с кривой:")
    label_path.place(x=10, y=90 + dy * (i - 1))

    # Создание текстового поля для ввода пути
    path_entry = create_text(input_frame, method="entry", height=1, state='normal', scrollbar=False)
    path_entry.place(x=10, y=110 + dy * (i - 1), width=600)

    path_entry._name = f"curve_{i}_filename"

    # Кнопка для выбора файла
    select_button = ttk.Button(input_frame, text="Выбор файла",
                               command=lambda: select_path(path_entry, path_type='file', saved_data=saved_data[i - 1]))
    select_button.place(x=620, y=108 + dy * (i - 1))

    # Если чекбокс легенды отмечен, добавляем поле для легенды
    if checkbox_var.get():
        label_legend = ttk.Label(input_frame, text="Подпись легенды:")
        label_legend.place(x=10, y=150 + dy * (i - 1))
        legend_entry = create_text(input_frame, method="entry", height=1, state='normal', scrollbar=False)
        legend_entry.place(x=10, y=170 + dy * (i - 1), width=300)
        legend_entry._name = f"curve_{i}_legend"

    return None


def update_curves(frame, num_curves, next_frame, checkbox_var, saved_data):
    """Обновляет кривые в соответствии с выбранным количеством и состоянием чекбокса."""
    # Очищаем старые виджеты
    for widget in frame.winfo_children():
        widget.destroy()

    if num_curves == '':
        return
    else:
        num_curves_int = int(num_curves)

    # Меняем высоту фрейма в зависимости от количества кривых
    frame_height = 210 * num_curves_int if checkbox_var.get() else 150 * num_curves_int
    frame.place_configure(height=frame_height)

    # Восстанавливаем данные, если они есть
    for i in range(len(saved_data), num_curves_int):
        saved_data.append({'curve_type': "", 'path': "", 'legend': "", 'curve_typeX': "", 'curve_typeY': "",
                           'curve_typeX_type': "", 'curve_typeY_type': ""})

    for i in range(1, num_curves_int + 1):
        create_curve_box(frame, i, checkbox_var, saved_data)

    next_frame.place(x=10, y=frame.winfo_y() + frame_height + 10)  # Обновляем координаты следующего фрейма


def save_file(entry_widget, graph_info):
    from main import create_plot  # локальный импорт для избежания циклической зависимости

    file_name = entry_widget.get()
    if file_name:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                                                 initialfile=file_name)
        if file_path:
            try:
                curves_info = [{
                    'X_values': graph_info['X_values'],
                    'Y_values': graph_info['Y_values']
                }]
                create_plot(curves_info, graph_info['X_label'], graph_info['Y_label'], graph_info['title'],
                            savefile=True,
                            file_plt=file_path)  # Генерация и сохранение графика
                messagebox.showinfo("Успех", f"График сохранен: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")
    else:
        messagebox.showerror("Ошибка", "Имя файла не может быть пустым!")


class AxisTitleProcessor:
    def __init__(self, combo_title, combo_size, language='Русский'):
        self.combo_title = combo_title
        self.combo_size = combo_size
        self.language = language
        self.title_mapping = {
            "Время": {
                "Русский": "Время $t$",
                "Английский": "Time $t$",
            },
            "Частота 1": {
                "Русский": "Частота ${{f}}_{{\mathit{1}}}$",
                "Английский": "Frequency ${{f}}_{{\mathit{1}}}$",
            },
            "Частота 2": {
                "Русский": "Частота ${{f}}_{{\mathit{2}}}$",
                "Английский": "Frequency ${{f}}_{{\mathit{2}}}$",
            },
            "Частота 3": {
                "Русский": "Частота ${{f}}_{{\mathit{3}}}$",
                "Английский": "Frequency ${{f}}_{{\mathit{3}}}$",
            },
        }

    def _get_units(self):
        units = {
            "Время": {
                "Русский": "с",
                "Английский": "s",
            },
            "Частота 1": {
                "Русский": "Гц",
                "Английский": "Hz",
            },
            "Частота 2": {
                "Русский": "Гц",
                "Английский": "Hz",
            },
            "Частота 3": {
                "Русский": "Гц",
                "Английский": "Hz",
            },
        }
        selection = self.combo_title.get()
        unit = units.get(selection, {}).get(self.language, "")
        return f", {unit}" if unit else ""

    def _get_title(self):
        selection = self.combo_title.get()
        return self.title_mapping.get(selection, {}).get(self.language, selection)

    def get_processed_title(self):
        if self.combo_title.get() == "Другое" and self.combo_size.get():
            return f"{self.combo_size.get()}"
        title = self._get_title()
        return f"{title}{self._get_units()}"


def get_X_Y_data(curve_info):
    if curve_info['curve_type'] == 'Частотный анализ':
        try:
            # Открытие файла
            with open(curve_info['curve_file'], 'r') as file:
                lines = file.readlines()

            # Динамическое определение заголовков на основе curve_typeXF_type и curve_typeYF_type
            header_XF = f"t {curve_info['curve_typeXF_type']}N {curve_info['curve_typeXF_type']}eig {curve_info['curve_typeXF_type']}mass pr{curve_info['curve_typeXF_type']}mass totalpr{curve_info['curve_typeXF_type']}mass"
            header_YF = f"t {curve_info['curve_typeYF_type']}N {curve_info['curve_typeYF_type']}eig {curve_info['curve_typeYF_type']}mass pr{curve_info['curve_typeYF_type']}mass totalpr{curve_info['curve_typeYF_type']}mass"

            # Динамическое определение индекса столбца для каждого параметра curve_typeXF и curve_typeYF
            headers_map = {
                "Время": 0,
                "Номер доминантной частота": 1,
                "Частота": 2,
                "Масса": 3,
                "Процент от общей массы": 4,
                "Процент общей массы": 5
            }

            # Определяем, какой столбец нужно извлекать для X и Y в зависимости от curve_typeXF и curve_typeYF
            index_X = headers_map.get(curve_info['curve_typeXF'])
            index_Y = headers_map.get(curve_info['curve_typeYF'])

            if index_X is None or index_Y is None:
                logger.error("Ошибка: некорректные параметры curve_typeXF или curve_typeYF.")
                return

            # Переменные для хранения данных
            X_data = []
            Y_data = []
            current_block_X = False
            current_block_Y = False

            for line in lines:
                line = line.strip()

                # Определение начала блока
                if line == header_XF and line == header_YF:
                    current_block_X = True
                    current_block_Y = True
                    continue
                elif line == header_XF:
                    current_block_X = True
                    current_block_Y = False
                    continue
                elif line == header_YF:
                    current_block_Y = True
                    current_block_X = False
                    continue
                elif line == '':
                    current_block_X = False
                    current_block_Y = False
                    continue

                # Извлечение данных из блока X
                if current_block_X:
                    try:
                        data_list = ast.literal_eval(line)  # Преобразуем строку в список
                        if isinstance(data_list, list) and len(data_list) > index_X:
                            if index_X == 4 or index_X == 5:
                                X_data.append(float(data_list[index_X].strip('%')))
                            else:
                                X_data.append(float(data_list[index_X]))  # Извлекаем данные для X
                    except (ValueError, SyntaxError):
                        # Если строку нельзя преобразовать в список, пропускаем её
                        logger.error("Ошибка преобразования строки: %s", line)

                # Извлечение данных из блока Y
                if current_block_Y:
                    try:
                        data_list = ast.literal_eval(line)  # Преобразуем строку в список
                        if isinstance(data_list, list) and len(data_list) > index_Y:
                            if index_Y == 4 or index_Y == 5:
                                logger.debug("%s", data_list[index_Y])
                                Y_data.append(float(data_list[index_Y].strip('%')))
                            else:
                                Y_data.append(float(data_list[index_Y]))  # Извлекаем данные для Y
                    except (ValueError, SyntaxError):
                        # Если строку нельзя преобразовать в список, пропускаем её
                        logger.error("Ошибка преобразования строки: %s", line)

            # Сохранение данных в curve_info
            curve_info['X_values'] = X_data
            curve_info['Y_values'] = Y_data

        except FileNotFoundError:
            logger.error("Файл '%s' не найден.", curve_info['curve_file'])
        except IOError:
            logger.error("Ошибка при чтении файла '%s'.", curve_info['curve_file'])


def generate_graph(ax, fig, canvas, path_entry_title, combo_titleX, combo_titleX_size, combo_titleY, combo_titleY_size,
                   legend_checkbox, curves_frame, combo_curves, combo_language):
    from main import create_plot  # локальный импорт для избегания циклической зависимости

    # Очистка предыдущего графика
    ax.clear()
    # Считываем заголовок из поля ввода
    title = path_entry_title.get()
    language = combo_language.get() or 'Русский'
    xlabel_processor = AxisTitleProcessor(combo_titleX, combo_titleX_size, language)
    ylabel_processor = AxisTitleProcessor(combo_titleY, combo_titleY_size, language)
    xlabel = xlabel_processor.get_processed_title()
    ylabel = ylabel_processor.get_processed_title()

    # Считываем количество кривых из combobox
    num_curves = int(combo_curves.get())

    # Генерация данных для графика (пример - синусоида)
    x = np.linspace(0, 10, 100)
    curves_info = []
    # Построение каждой кривой в цикле
    for i in range(1, num_curves + 1):
        curve_info = {}
        for widget in curves_frame.winfo_children():
            if hasattr(widget, '_name'):
                widget_name = widget._name

                # Проверяем тип кривой
                if widget_name == f"curve_{i}_type":
                    curve_info['curve_type'] = widget.get()

                # Если тип кривой "Частотный анализ", собираем дополнительные данные
                if 'curve_type' in curve_info and curve_info['curve_type'] == "Частотный анализ":
                    if widget_name == f"curve_{i}_typeXF":
                        curve_info['curve_typeXF'] = widget.get()
                    elif widget_name == f"curve_{i}_typeYF":
                        curve_info['curve_typeYF'] = widget.get()
                    elif widget_name == f"curve_{i}_typeXFtype":
                        curve_info['curve_typeXF_type'] = widget.get()
                    elif widget_name == f"curve_{i}_typeYFtype":
                        curve_info['curve_typeYF_type'] = widget.get()

                # Получаем имя файла для каждой кривой
                if widget_name == f"curve_{i}_filename":
                    curve_info['curve_file'] = widget.get()

                # Проверяем наличие легенды, если отмечен чекбокс
                if legend_checkbox.get() and widget_name == f"curve_{i}_legend":
                    curve_info['curve_legend'] = widget.get()

        # Добавляем информацию о кривой в общий список
        get_X_Y_data(curve_info)
        curves_info.append(curve_info)

    create_plot(curves_info, xlabel, ylabel, title,
                fig=fig, ax=ax, legend=legend_checkbox.get())

    # Перерисовка графика
    canvas.draw()
