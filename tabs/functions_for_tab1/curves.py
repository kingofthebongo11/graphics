import tkinter as tk
from tkinter import ttk
from widgets.select_path import select_path

from .events import on_combobox_event, on_combo_change_curve_type


def create_curve_box(input_frame, i, checkbox_var, saved_data):
    """Создает ячейку для настройки параметров кривой."""
    from widgets.text_widget import create_text  # локальный импорт для избегания циклической зависимости

    # Определяем высоту ячейки на основе состояния чекбокса
    dy = 210 if checkbox_var.get() else 180

    # Метка о параметрах кривой
    label_curve_box = ttk.Label(input_frame, text=f"Настройка параметров кривой {i}:")
    label_curve_box.place(x=10, y=0 + dy * (i - 1))

    # Метка о выборе типа кривой
    label_curve_type = ttk.Label(input_frame, text=f"Выберите тип кривой {i}:")
    label_curve_type.place(x=10, y=30 + dy * (i - 1))

    # Создание выпадающего меню для типа кривой
    combo_curve_type = ttk.Combobox(
        input_frame,
        values=["Частотный анализ", "Текстовой файл", "Файл кривой LS-Dyna", "Excel файл", "Комбинированный"],
        state='readonly'
    )
    combo_curve_type.place(x=250, y=30 + dy * (i - 1), width=150)
    combo_curve_type._name = f"curve_{i}_type"
    saved_curve_type = saved_data[i - 1].get('curve_type', '')
    if saved_curve_type:
        combo_curve_type.set(saved_curve_type)

    # Создане элементов для параметров X и Y
    label_curve_typeX = ttk.Label(input_frame, text="Выберите параметр для Х:")
    combo_curve_typeX = ttk.Combobox(input_frame, values=["Время", "Номер доминантной частота", "Частота",
                                                          "Масса", "Процент от общей массы", "Процент общей массы"],
                                     state='readonly')
    combo_curve_typeX._name = f"curve_{i}_typeXF"
    combo_curve_typeX.set(saved_data[i - 1].get('curve_typeX', ''))
    label_curve_typeY = ttk.Label(input_frame, text="Выберите параметр для Y:")
    combo_curve_typeY = ttk.Combobox(input_frame, values=["Время", "Номер доминантной частота", "Частота",
                                                          "Масса", "Процет от общей массы", "Процент общей массы"],
                                     state='readonly')
    combo_curve_typeY._name = f"curve_{i}_typeYF"
    combo_curve_typeY.set(saved_data[i - 1].get('curve_typeY', ''))
    label_curve_typeX_type = ttk.Label(input_frame, text="По какой оси:")
    combo_curve_typeX_type = ttk.Combobox(input_frame, values=["X", "Y", "Z", "XR", "YR", "ZR"],
                                          state='readonly')
    combo_curve_typeX_type._name = f"curve_{i}_typeXFtype"
    combo_curve_typeX_type.set(saved_data[i - 1].get('curve_typeX_type', ''))
    label_curve_typeY_type = ttk.Label(input_frame, text="По какой оси:")
    combo_curve_typeY_type = ttk.Combobox(input_frame, values=["X", "Y", "Z", "XR", "YR", "ZR"],
                                          state='readonly')
    combo_curve_typeY_type._name = f"curve_{i}_typeYFtype"
    combo_curve_typeY_type.set(saved_data[i - 1].get('curve_typeY_type', ''))

    # Элементы для комбинированного типа
    label_source_X = ttk.Label(input_frame, text="Выберите тип для X:")
    combo_source_X = ttk.Combobox(
        input_frame,
        values=["Частотный анализ", "Текстовой файл", "Файл кривой LS-Dyna", "Excel файл"],
        state='readonly'
    )
    combo_source_X._name = f"curve_{i}_X_source"
    combo_source_X.set(saved_data[i - 1].get('X_source', {}).get('source', ''))

    label_param_X = ttk.Label(input_frame, text="Параметр:")
    combo_param_X = ttk.Combobox(
        input_frame,
        values=["Время", "Номер доминантной частота", "Частота",
                "Масса", "Процент от общей массы", "Процент общей массы"],
        state='readonly'
    )
    combo_param_X._name = f"curve_{i}_X_parameter"
    combo_param_X.bind(
        "<<ComboboxSelected>>",
        lambda e: saved_data[i - 1].setdefault('X_source', {}).update({'parameter': combo_param_X.get()})
    )

    label_axis_X = ttk.Label(input_frame, text="По какой оси:")
    combo_axis_X = ttk.Combobox(
        input_frame,
        values=["X", "Y", "Z", "XR", "YR", "ZR"],
        state='readonly'
    )
    combo_axis_X._name = f"curve_{i}_X_direction"
    combo_axis_X.bind(
        "<<ComboboxSelected>>",
        lambda e: saved_data[i - 1].setdefault('X_source', {}).update({'direction': combo_axis_X.get()})
    )

    label_column_X = ttk.Label(input_frame, text="Столбец:")
    combo_column_X = ttk.Combobox(
        input_frame,
        values=["X", "Y"],
        state='readonly'
    )
    combo_column_X._name = f"curve_{i}_X_column"
    saved_column_x = saved_data[i - 1].get('X_source', {}).get('column')
    if saved_column_x in (0, 1):
        combo_column_X.set('X' if saved_column_x == 0 else 'Y')
    combo_column_X.bind(
        "<<ComboboxSelected>>",
        lambda e: saved_data[i - 1].setdefault('X_source', {}).update({'column': 0 if combo_column_X.get() == 'X' else 1})
    )

    label_range_Xc = ttk.Label(input_frame, text="Диапазон:")
    entry_range_Xc = ttk.Entry(input_frame, width=10)
    entry_range_Xc.insert(0, saved_data[i - 1].get('X_source', {}).get('range_x', ''))
    entry_range_Xc._name = f"curve_{i}_X_range"
    entry_range_Xc.bind(
        '<KeyRelease>',
        lambda e: saved_data[i - 1].setdefault('X_source', {}).update({'use_ranges': True, 'range_x': entry_range_Xc.get(), 'column': 0})
    )

    def toggle_X_source_options():
        for w in [label_param_X, combo_param_X, label_axis_X, combo_axis_X,
                  label_column_X, combo_column_X, label_range_Xc, entry_range_Xc]:
            w.place_forget()
        if combo_curve_type.get() != "Комбинированный":
            return
        source = combo_source_X.get()
        if source == "Частотный анализ":
            input_frame.update_idletasks()
            label_param_X.place(x=combo_source_X.winfo_x(), y=combo_source_X.winfo_y() + 30)
            combo_param_X.place(x=combo_source_X.winfo_x(), y=combo_source_X.winfo_y() + 50, width=150)
            label_axis_X.place(x=combo_source_X.winfo_x(), y=combo_source_X.winfo_y() + 75)
            combo_axis_X.place(x=combo_source_X.winfo_x(), y=combo_source_X.winfo_y() + 95, width=150)
        elif source in ("Текстовой файл", "Файл кривой LS-Dyna"):
            input_frame.update_idletasks()
            label_column_X.place(x=combo_source_X.winfo_x(), y=combo_source_X.winfo_y() + 30)
            combo_column_X.place(x=combo_source_X.winfo_x(), y=combo_source_X.winfo_y() + 50, width=150)
            saved_data[i - 1].setdefault('X_source', {}).setdefault('column', 0)
        elif source == "Excel файл":
            input_frame.update_idletasks()
            label_range_Xc.place(x=combo_source_X.winfo_x(), y=combo_source_X.winfo_y() + 30)
            entry_range_Xc.place(x=combo_source_X.winfo_x(), y=combo_source_X.winfo_y() + 50, width=150)
            saved_data[i - 1].setdefault('X_source', {}).update({'column': 0})

    combo_source_X.bind(
        "<<ComboboxSelected>>",
        lambda e: on_combobox_event(
            e,
            lambda e: saved_data[i - 1].setdefault('X_source', {}).update({'source': combo_source_X.get()}),
            lambda e: toggle_X_source_options()
        )
    )

    label_source_Y = ttk.Label(input_frame, text="Выберите тип для данных Y:")
    combo_source_Y = ttk.Combobox(
        input_frame,
        values=["Частотный анализ", "Текстовой файл", "Файл кривой LS-Dyna", "Excel файл"],
        state='readonly'
    )
    combo_source_Y._name = f"curve_{i}_Y_source"
    combo_source_Y.set(saved_data[i - 1].get('Y_source', {}).get('source', ''))

    label_param_Y = ttk.Label(input_frame, text="Параметр:")
    combo_param_Y = ttk.Combobox(
        input_frame,
        values=["Время", "Номер доминантной частота", "Частота",
                "Масса", "Процент от общей массы", "Процент общей массы"],
        state='readonly'
    )
    combo_param_Y._name = f"curve_{i}_Y_parameter"
    combo_param_Y.bind(
        "<<ComboboxSelected>>",
        lambda e: saved_data[i - 1].setdefault('Y_source', {}).update({'parameter': combo_param_Y.get()})
    )

    label_axis_Y = ttk.Label(input_frame, text="По какой оси:")
    combo_axis_Y = ttk.Combobox(
        input_frame,
        values=["X", "Y", "Z", "XR", "YR", "ZR"],
        state='readonly'
    )
    combo_axis_Y._name = f"curve_{i}_Y_direction"
    combo_axis_Y.bind(
        "<<ComboboxSelected>>",
        lambda e: saved_data[i - 1].setdefault('Y_source', {}).update({'direction': combo_axis_Y.get()})
    )

    label_column_Y = ttk.Label(input_frame, text="Столбец:")
    combo_column_Y = ttk.Combobox(
        input_frame,
        values=["X", "Y"],
        state='readonly'
    )
    combo_column_Y._name = f"curve_{i}_Y_column"
    saved_column_y = saved_data[i - 1].get('Y_source', {}).get('column')
    if saved_column_y in (0, 1):
        combo_column_Y.set('X' if saved_column_y == 0 else 'Y')
    combo_column_Y.bind(
        "<<ComboboxSelected>>",
        lambda e: saved_data[i - 1].setdefault('Y_source', {}).update({'column': 0 if combo_column_Y.get() == 'X' else 1})
    )

    label_range_Yc = ttk.Label(input_frame, text="Диапазон:")
    entry_range_Yc = ttk.Entry(input_frame, width=10)
    entry_range_Yc.insert(0, saved_data[i - 1].get('Y_source', {}).get('range_y', ''))
    entry_range_Yc._name = f"curve_{i}_Y_range"
    entry_range_Yc.bind(
        '<KeyRelease>',
        lambda e: saved_data[i - 1].setdefault('Y_source', {}).update({'use_ranges': True, 'range_y': entry_range_Yc.get(), 'column': 1})
    )

    def toggle_Y_source_options():
        for w in [label_param_Y, combo_param_Y, label_axis_Y, combo_axis_Y,
                  label_column_Y, combo_column_Y, label_range_Yc, entry_range_Yc]:
            w.place_forget()
        if combo_curve_type.get() != "Комбинированный":
            return
        source = combo_source_Y.get()
        if source == "Частотный анализ":
            input_frame.update_idletasks()
            label_param_Y.place(x=combo_source_Y.winfo_x(), y=combo_source_Y.winfo_y() + 30)
            combo_param_Y.place(x=combo_source_Y.winfo_x(), y=combo_source_Y.winfo_y() + 50, width=150)
            label_axis_Y.place(x=combo_source_Y.winfo_x(), y=combo_source_Y.winfo_y() + 75)
            combo_axis_Y.place(x=combo_source_Y.winfo_x(), y=combo_source_Y.winfo_y() + 95, width=150)
        elif source in ("Текстовой файл", "Файл кривой LS-Dyna"):
            input_frame.update_idletasks()
            label_column_Y.place(x=combo_source_Y.winfo_x(), y=combo_source_Y.winfo_y() + 30)
            combo_column_Y.place(x=combo_source_Y.winfo_x(), y=combo_source_Y.winfo_y() + 50, width=150)
            saved_data[i - 1].setdefault('Y_source', {}).setdefault('column', 1)
        elif source == "Excel файл":
            input_frame.update_idletasks()
            label_range_Yc.place(x=combo_source_Y.winfo_x(), y=combo_source_Y.winfo_y() + 30)
            entry_range_Yc.place(x=combo_source_Y.winfo_x(), y=combo_source_Y.winfo_y() + 50, width=150)
            saved_data[i - 1].setdefault('Y_source', {}).update({'column': 1})

    combo_source_Y.bind(
        "<<ComboboxSelected>>",
        lambda e: on_combobox_event(
            e,
            lambda e: saved_data[i - 1].setdefault('Y_source', {}).update({'source': combo_source_Y.get()}),
            lambda e: toggle_Y_source_options()
        )
    )

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

    horizontal_var = tk.BooleanVar(value=saved_data[i - 1].get('horizontal', False))
    checkbox_horizontal = ttk.Checkbutton(
        input_frame,
        text="По-горизонтали",
        variable=horizontal_var,
        command=lambda: saved_data[i - 1].update({'horizontal': horizontal_var.get()})
    )
    checkbox_horizontal._name = f"curve_{i}_horizontal"
    checkbox_horizontal.var = horizontal_var

    offset_var = tk.BooleanVar(value=saved_data[i - 1].get('use_offset', False))
    checkbox_offset = ttk.Checkbutton(
        input_frame,
        text="Смещение",
        variable=offset_var,
        command=lambda: (saved_data[i - 1].update({'use_offset': offset_var.get()}), toggle_excel_options())
    )
    checkbox_offset._name = f"curve_{i}_use_offset"
    checkbox_offset.var = offset_var

    label_offset_h = ttk.Label(input_frame, text="Гор:")
    entry_offset_h = ttk.Entry(input_frame, width=5)
    entry_offset_h.insert(0, str(saved_data[i - 1].get('offset_horizontal', 0)))
    entry_offset_h._name = f"curve_{i}_offset_h"
    entry_offset_h.bind(
        '<KeyRelease>',
        lambda e: saved_data[i - 1].update({
            'offset_horizontal': int(entry_offset_h.get() or 0) if entry_offset_h.get().isdigit() else 0
        })
    )

    label_offset_v = ttk.Label(input_frame, text="Верт:")
    entry_offset_v = ttk.Entry(input_frame, width=5)
    entry_offset_v.insert(0, str(saved_data[i - 1].get('offset_vertical', 0)))
    entry_offset_v._name = f"curve_{i}_offset_v"
    entry_offset_v.bind(
        '<KeyRelease>',
        lambda e: saved_data[i - 1].update({
            'offset_vertical': int(entry_offset_v.get() or 0) if entry_offset_v.get().isdigit() else 0
        })
    )

    ranges_var = tk.BooleanVar(value=saved_data[i - 1].get('use_ranges', False))
    checkbox_ranges = ttk.Checkbutton(
        input_frame,
        text="Диапазоны",
        variable=ranges_var,
        command=lambda: (saved_data[i - 1].update({'use_ranges': ranges_var.get()}), toggle_excel_options())
    )
    checkbox_ranges._name = f"curve_{i}_use_ranges"
    checkbox_ranges.var = ranges_var

    label_range_x = ttk.Label(input_frame, text="X:")
    entry_range_x = ttk.Entry(input_frame, width=10)
    entry_range_x.insert(0, saved_data[i - 1].get('range_x', ''))
    entry_range_x._name = f"curve_{i}_range_x"
    entry_range_x.bind(
        '<KeyRelease>',
        lambda e: saved_data[i - 1].update({'range_x': entry_range_x.get()})
    )

    label_range_y = ttk.Label(input_frame, text="Y:")
    entry_range_y = ttk.Entry(input_frame, width=10)
    entry_range_y.insert(0, saved_data[i - 1].get('range_y', ''))
    entry_range_y._name = f"curve_{i}_range_y"
    entry_range_y.bind(
        '<KeyRelease>',
        lambda e: saved_data[i - 1].update({'range_y': entry_range_y.get()})
    )

    def toggle_excel_options():
        if combo_curve_type.get() == "Excel файл":
            checkbox_horizontal.place(x=10, y=60 + dy * (i - 1))
            checkbox_offset.place(x=150, y=60 + dy * (i - 1))
            checkbox_ranges.place(x=410, y=60 + dy * (i - 1))
            if ranges_var.get():
                checkbox_horizontal.var.set(False)
                checkbox_offset.var.set(False)
                saved_data[i - 1].update({'horizontal': False, 'use_offset': False})
                checkbox_horizontal.config(state='disabled')
                checkbox_offset.config(state='disabled')
                label_offset_h.place_forget()
                entry_offset_h.place_forget()
                label_offset_v.place_forget()
                entry_offset_v.place_forget()
                label_range_x.place(x=500, y=60 + dy * (i - 1))
                entry_range_x.place(x=520, y=60 + dy * (i - 1), width=80)
                label_range_y.place(x=610, y=60 + dy * (i - 1))
                entry_range_y.place(x=630, y=60 + dy * (i - 1), width=80)
            else:
                checkbox_horizontal.config(state='normal')
                checkbox_offset.config(state='normal')
                label_range_x.place_forget()
                entry_range_x.place_forget()
                label_range_y.place_forget()
                entry_range_y.place_forget()
                if offset_var.get():
                    label_offset_h.place(x=240, y=60 + dy * (i - 1))
                    entry_offset_h.place(x=270, y=60 + dy * (i - 1), width=40)
                    label_offset_v.place(x=320, y=60 + dy * (i - 1))
                    entry_offset_v.place(x=360, y=60 + dy * (i - 1), width=40)
                else:
                    label_offset_h.place_forget()
                    entry_offset_h.place_forget()
                    label_offset_v.place_forget()
                    entry_offset_v.place_forget()
        else:
            checkbox_horizontal.place_forget()
            checkbox_offset.place_forget()
            checkbox_ranges.place_forget()
            label_offset_h.place_forget()
            entry_offset_h.place_forget()
            label_offset_v.place_forget()
            entry_offset_v.place_forget()
            label_range_x.place_forget()
            entry_range_x.place_forget()
            label_range_y.place_forget()
            entry_range_y.place_forget()

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
                label_source_X,
                combo_source_X,
                label_source_Y,
                combo_source_Y,
                label_path,
                path_entry,
                select_button,
                label_path_X,
                path_entry_X,
                select_button_X,
                label_path_Y,
                path_entry_Y,
                select_button_Y,
            ),
            lambda e: saved_data[i - 1].update({'curve_type': combo_curve_type.get()}),
            lambda e: toggle_excel_options(),
            lambda e: (toggle_X_source_options(), toggle_Y_source_options()),
        ),
    )

    # Метка для выбора файла с кривой
    label_path = ttk.Label(input_frame, text="Выберите файл с кривой:")
    label_path.place(x=10, y=90 + dy * (i - 1))

    # Создание текстового поля для ввода пути
    path_entry = create_text(input_frame, method="entry", height=1, state='normal', scrollbar=False)
    path_entry.place(x=10, y=110 + dy * (i - 1), width=600)

    path_entry._name = f"curve_{i}_filename"
    path_entry.insert(0, saved_data[i - 1].get('path', ''))
    path_entry.bind(
        '<KeyRelease>',
        lambda e: saved_data[i - 1].update({'path': path_entry.get()})
    )

    # Кнопка для выбора файла
    select_button = ttk.Button(
        input_frame,
        text="Выбор файла",
        command=lambda: select_path(path_entry, path_type='file', saved_data=saved_data[i - 1])
    )
    select_button.place(x=620, y=108 + dy * (i - 1))

    # Отдельные поля для комбинированного типа
    label_path_X = ttk.Label(input_frame, text="Файл для X:")
    label_path_X.place(x=10, y=90 + dy * (i - 1))
    path_entry_X = create_text(input_frame, method="entry", height=1, state='normal', scrollbar=False)
    path_entry_X.place(x=10, y=110 + dy * (i - 1), width=600)
    path_entry_X._name = f"curve_{i}_filename_X"
    path_entry_X.insert(0, saved_data[i - 1].get('X_source', {}).get('curve_file', ''))
    path_entry_X.bind(
        '<KeyRelease>',
        lambda e: saved_data[i - 1].setdefault('X_source', {}).update({'curve_file': path_entry_X.get()})
    )
    select_button_X = ttk.Button(
        input_frame,
        text="Выбор файла",
        command=lambda: (
            select_path(path_entry_X, path_type='file'),
            saved_data[i - 1].setdefault('X_source', {}).update({'curve_file': path_entry_X.get()})
        )
    )
    select_button_X.place(x=620, y=108 + dy * (i - 1))

    label_path_Y = ttk.Label(input_frame, text="Файл для Y:")
    label_path_Y.place(x=10, y=140 + dy * (i - 1))
    path_entry_Y = create_text(input_frame, method="entry", height=1, state='normal', scrollbar=False)
    path_entry_Y.place(x=10, y=160 + dy * (i - 1), width=600)
    path_entry_Y._name = f"curve_{i}_filename_Y"
    path_entry_Y.insert(0, saved_data[i - 1].get('Y_source', {}).get('curve_file', ''))
    path_entry_Y.bind(
        '<KeyRelease>',
        lambda e: saved_data[i - 1].setdefault('Y_source', {}).update({'curve_file': path_entry_Y.get()})
    )
    select_button_Y = ttk.Button(
        input_frame,
        text="Выбор файла",
        command=lambda: (
            select_path(path_entry_Y, path_type='file'),
            saved_data[i - 1].setdefault('Y_source', {}).update({'curve_file': path_entry_Y.get()})
        )
    )
    select_button_Y.place(x=620, y=158 + dy * (i - 1))

    label_path_X.place_forget()
    path_entry_X.place_forget()
    select_button_X.place_forget()
    label_path_Y.place_forget()
    path_entry_Y.place_forget()
    select_button_Y.place_forget()

    # Если чекбокс легенды отмечен, добавляем поле для легенды
    if checkbox_var.get():
        label_legend = ttk.Label(input_frame, text="Подпись легенды:")
        label_legend.place(x=10, y=150 + dy * (i - 1))
        legend_entry = create_text(input_frame, method="entry", height=1, state='normal', scrollbar=False)
        legend_entry.place(x=10, y=170 + dy * (i - 1), width=300)
        legend_entry._name = f"curve_{i}_legend"
        legend_entry.insert(0, saved_data[i - 1].get('legend', ''))
        legend_entry.bind(
            '<KeyRelease>',
            lambda e: saved_data[i - 1].update({'legend': legend_entry.get()})
        )
    if saved_curve_type:
        on_combo_change_curve_type(
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
            label_source_X,
            combo_source_X,
            label_source_Y,
            combo_source_Y,
            label_path,
            path_entry,
            select_button,
            label_path_X,
            path_entry_X,
            select_button_X,
            label_path_Y,
            path_entry_Y,
            select_button_Y,
        )

    combo_param_X.set(saved_data[i - 1].get('X_source', {}).get('parameter', ''))
    combo_axis_X.set(saved_data[i - 1].get('X_source', {}).get('direction', ''))
    combo_param_Y.set(saved_data[i - 1].get('Y_source', {}).get('parameter', ''))
    combo_axis_Y.set(saved_data[i - 1].get('Y_source', {}).get('direction', ''))

    toggle_excel_options()
    toggle_X_source_options()
    toggle_Y_source_options()

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
    frame_height = 210 * num_curves_int if checkbox_var.get() else 180 * num_curves_int
    frame.place_configure(height=frame_height)

    # Восстанавливаем данные, если они есть
    for i in range(len(saved_data), num_curves_int):
        saved_data.append({'curve_type': "", 'path': "", 'legend': "", 'curve_typeX': "", 'curve_typeY': "",
                           'curve_typeX_type': "", 'curve_typeY_type': "", 'horizontal': False,
                           'use_offset': False, 'offset_horizontal': 0, 'offset_vertical': 0,
                           'use_ranges': False, 'range_x': '', 'range_y': '',
                           'X_source': {}, 'Y_source': {}})

    for i in range(1, num_curves_int + 1):
        create_curve_box(frame, i, checkbox_var, saved_data)

    next_frame.place(x=10, y=frame.winfo_y() + frame_height + 10)  # Обновляем координаты следующего фрейма
