import tkinter as tk
from tkinter import ttk
from widgets.select_path import select_path

from .events import on_combobox_event, on_combo_change_curve_type


def create_curve_box(input_frame, i, checkbox_var, saved_data):
    """Создает ячейку для настройки параметров кривой."""
    from widgets.text_widget import create_text  # локальный импорт для избегания циклической зависимости

    # Определяем высоту ячейки на основе состояния чекбокса
    dy = 210 if checkbox_var.get() else 150

    # Метка о параметрах кривой
    label_curve_box = ttk.Label(input_frame, text=f"Настройка параметров кривой {i}:")
    label_curve_box.place(x=10, y=0 + dy * (i - 1))

    # Метка о выборе типа кривой
    label_curve_type = ttk.Label(input_frame, text=f"Выберите тип кривой {i}:")
    label_curve_type.place(x=10, y=30 + dy * (i - 1))

    # Создание выпадающего меню для типа кривой
    combo_curve_type = ttk.Combobox(
        input_frame,
        values=["Частотный анализ", "Текстовой файл", "Файл кривой LS-Dyna", "Excel файл"],
        state='readonly'
    )
    combo_curve_type.place(x=250, y=30 + dy * (i - 1), width=150)
    combo_curve_type._name = f"curve_{i}_type"

    # Создане элементов для параметров X и Y
    label_curve_typeX = ttk.Label(input_frame, text="Выберите параметр для Х:")
    combo_curve_typeX = ttk.Combobox(input_frame, values=["Время", "Номер доминантной частота", "Частота",
                                                          "Масса", "Процент от общей массы", "Процент общей массы"],
                                     state='readonly')
    combo_curve_typeX._name = f"curve_{i}_typeXF"
    label_curve_typeY = ttk.Label(input_frame, text="Выберите параметр для Y:")
    combo_curve_typeY = ttk.Combobox(input_frame, values=["Время", "Номер доминантной частота", "Частота",
                                                          "Масса", "Процет от общей массы", "Процент общей массы"],
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

    # Метка для выбора файла с кривой
    label_path = ttk.Label(input_frame, text="Выберите файл с кривой:")
    label_path.place(x=10, y=90 + dy * (i - 1))

    # Создание текстового поля для ввода пути
    path_entry = create_text(input_frame, method="entry", height=1, state='normal', scrollbar=False)
    path_entry.place(x=10, y=110 + dy * (i - 1), width=600)

    path_entry._name = f"curve_{i}_filename"

    # Элементы для Excel файлов
    horizontal_var = tk.IntVar()
    horizontal_check = ttk.Checkbutton(input_frame, text="По горизонтали", variable=horizontal_var)
    horizontal_check.var = horizontal_var
    horizontal_check._name = f"curve_{i}_horizontal"

    label_X_range = ttk.Label(input_frame, text="Диапазон X:")
    entry_X_range = create_text(input_frame, method="entry", height=1, state='normal', scrollbar=False)
    entry_X_range._name = f"curve_{i}_X_range"
    label_Y_range = ttk.Label(input_frame, text="Диапазон Y:")
    entry_Y_range = create_text(input_frame, method="entry", height=1, state='normal', scrollbar=False)
    entry_Y_range._name = f"curve_{i}_Y_range"

    def toggle_ranges():
        if horizontal_var.get():
            y_pos = path_entry.winfo_y() + 30
            label_X_range.place(x=10, y=y_pos)
            entry_X_range.place(x=110, y=y_pos, width=100)
            label_Y_range.place(x=230, y=y_pos)
            entry_Y_range.place(x=330, y=y_pos, width=100)
        else:
            label_X_range.place_forget()
            entry_X_range.place_forget()
            label_Y_range.place_forget()
            entry_Y_range.place_forget()

    horizontal_check.config(command=toggle_ranges)

    # Привязка события изменения выбора в combo_curve_type
    combo_curve_type.bind(
        "<<ComboboxSelected>>",
        lambda event: on_combobox_event(
            event,
            lambda e: on_combo_change_curve_type(
                input_frame,
                combo_curve_type,
                label_curve_typeX,
                combo_curve_typeX,
                label_curve_typeY,
                combo_curve_typeY,
                label_curve_typeX_type,
                combo_curve_typeX_type,
                label_curve_typeY_type,
                combo_curve_typeY_type,
                path_entry,
                horizontal_check,
                label_X_range,
                entry_X_range,
                label_Y_range,
                entry_Y_range,
            ),
            lambda e: saved_data[i - 1].update({'curve_type': combo_curve_type.get()})
        )
    )

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
    frame_height = 230 * num_curves_int if checkbox_var.get() else 170 * num_curves_int
    frame.place_configure(height=frame_height)

    # Восстанавливаем данные, если они есть
    for i in range(len(saved_data), num_curves_int):
        saved_data.append({'curve_type': "", 'path': "", 'legend': "", 'curve_typeX': "", 'curve_typeY': "",
                           'curve_typeX_type': "", 'curve_typeY_type': "", 'horizontal': 0, 'X_range': "", 'Y_range': ""})

    for i in range(1, num_curves_int + 1):
        create_curve_box(frame, i, checkbox_var, saved_data)

    next_frame.place(x=10, y=frame.winfo_y() + frame_height + 10)  # Обновляем координаты следующего фрейма
