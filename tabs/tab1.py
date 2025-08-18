import tkinter as tk  # Alias for Tk functionality
from tkinter import ttk

from .functions_for_tab1 import update_curves, generate_graph, save_file, last_graph
from widgets import PlotEditor

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from widgets.text_widget import create_text


def sort_options(options):
    first = ["Нет"] if "Нет" in options else []
    middle = sorted([opt for opt in options if opt not in ("Нет", "Другое")])
    last = ["Другое"] if "Другое" in options else []
    return first + middle + last


def on_combo_changeX_Y_labels(combo, entry, label_size, size_combo):
    """
    Обрабатывает выбор в комбобоксе для осей:
    - Если выбрано "Другое", отображает текстовое поле для ввода и скрывает выбор размерности.
    - Иначе скрывает текстовое поле, показывает метку и комбобокс размерности с нужными единицами.
    """

    STRESS_UNITS = sort_options([
        "Па",
        "кПа",
        "МПа",
        "Н/мм²",
        "Н/см²",
        "Н/м²",
        "кН/мм²",
        "кН/см²",
        "кН/м²",
        "МН/мм²",
        "МН/см²",
        "МН/м²",
        "кгс/мм²",
        "кгс/см²",
        "кгс/м²",
        "тс/см²",
        "тс/м²",
    ])

    UNITS_MAPPING = {
        "Время": sort_options(["мс", "с", "мин", "ч"]),
        "Перемещение по X": sort_options(["мм", "см", "м"]),
        "Перемещение по Y": sort_options(["мм", "см", "м"]),
        "Перемещение по Z": sort_options(["мм", "см", "м"]),
        "Удлинение": sort_options(["мм", "см", "м"]),
        "Удлинение по X": sort_options(["мм", "см", "м"]),
        "Удлинение по Y": sort_options(["мм", "см", "м"]),
        "Удлинение по Z": sort_options(["мм", "см", "м"]),
        "Деформация": sort_options(["—", "%"]),
        "Пластическая деформация": sort_options(["—", "%"]),
        "Сила": sort_options(["мН", "Н", "кН", "кгс", "тс"]),
        "Продольная сила": sort_options(["мН", "Н", "кН", "кгс", "тс"]),
        "Поперечная сила": sort_options(["мН", "Н", "кН", "кгс", "тс"]),
        "Поперечная сила по Y": sort_options(["мН", "Н", "кН", "кгс", "тс"]),
        "Поперечная сила по Z": sort_options(["мН", "Н", "кН", "кгс", "тс"]),
        "Масса": sort_options(["г", "кг", "т"]),
        "Напряжение": STRESS_UNITS,
        "Интенсивность напряжений": STRESS_UNITS,
        "Нормальное напряжение X": STRESS_UNITS,
        "Нормальное напряжение Y": STRESS_UNITS,
        "Нормальное напряжение Z": STRESS_UNITS,
        "Касательное напряжение XY": STRESS_UNITS,
        "Касательное напряжение YX": STRESS_UNITS,
        "Касательное напряжение YZ": STRESS_UNITS,
        "Касательное напряжение ZY": STRESS_UNITS,
        "Касательное напряжение ZX": STRESS_UNITS,
        "Касательное напряжение XZ": STRESS_UNITS,
        "Крутящий момент Mx": sort_options(["Н·м", "кН·м"]),
        "Изгибающий момент Mx": sort_options(["Н·м", "кН·м"]),
        "Изгибающий момент My": sort_options(["Н·м", "кН·м"]),
        "Изгибающий момент Mz": sort_options(["Н·м", "кН·м"]),
        "Частота 1": sort_options(["Гц", "кГц"]),
        "Частота 2": sort_options(["Гц", "кГц"]),
        "Частота 3": sort_options(["Гц", "кГц"]),
        "Другое": [],
    }

    DEFAULT_UNITS = {
        "Время": "с",
        "Перемещение по X": "м",
        "Перемещение по Y": "м",
        "Перемещение по Z": "м",
        "Удлинение": "м",
        "Удлинение по X": "м",
        "Удлинение по Y": "м",
        "Удлинение по Z": "м",
        "Деформация": "—",
        "Пластическая деформация": "—",
        "Сила": "Н",
        "Продольная сила": "Н",
        "Поперечная сила": "Н",
        "Поперечная сила по Y": "Н",
        "Поперечная сила по Z": "Н",
        "Масса": "кг",
        "Напряжение": "Па",
        "Интенсивность напряжений": "Па",
        "Нормальное напряжение X": "Па",
        "Нормальное напряжение Y": "Па",
        "Нормальное напряжение Z": "Па",
        "Касательное напряжение XY": "Па",
        "Касательное напряжение YX": "Па",
        "Касательное напряжение YZ": "Па",
        "Касательное напряжение ZY": "Па",
        "Касательное напряжение ZX": "Па",
        "Касательное напряжение XZ": "Па",
        "Крутящий момент Mx": "Н·м",
        "Изгибающий момент Mx": "Н·м",
        "Изгибающий момент My": "Н·м",
        "Изгибающий момент Mz": "Н·м",
        "Частота 1": "Гц",
        "Частота 2": "Гц",
        "Частота 3": "Гц",
    }
    selection = combo.get()
    if selection == "Другое":
        if not entry.winfo_ismapped():
            entry.place(x=combo.winfo_x() + 250, y=combo.winfo_y(), width=300)
            entry.config(state='normal')
        label_size.place_forget()
        size_combo.place_forget()
        size_combo['values'] = []
        size_combo.set("")
    elif selection == "Нет":
        entry.place_forget()
        label_size.place_forget()
        size_combo.place_forget()
        size_combo['values'] = []
        size_combo.set("")
    else:
        entry.place_forget()
        label_size.place(x=combo.winfo_x() + 250, y=combo.winfo_y())
        values = UNITS_MAPPING.get(selection, [])
        size_combo['values'] = values
        size_combo.set("")
        if values:
            size_combo.place(x=combo.winfo_x() + 400, y=combo.winfo_y(), width=100)
            default_unit = DEFAULT_UNITS.get(selection)
            if default_unit in values:
                size_combo.current(values.index(default_unit))
        else:
            size_combo.place_forget()


def create_tab1(notebook):
    # Список физических величин для прочностных расчетов
    PHYSICAL_QUANTITIES = sort_options([
        "Нет",
        "Время",
        "Деформация",
        "Изгибающий момент Mx",
        "Изгибающий момент My",
        "Изгибающий момент Mz",
        "Интенсивность напряжений",
        "Касательное напряжение XY",
        "Касательное напряжение XZ",
        "Касательное напряжение YX",
        "Касательное напряжение YZ",
        "Касательное напряжение ZX",
        "Касательное напряжение ZY",
        "Крутящий момент Mx",
        "Масса",
        "Напряжение",
        "Нормальное напряжение X",
        "Нормальное напряжение Y",
        "Нормальное напряжение Z",
        "Перемещение по X",
        "Перемещение по Y",
        "Перемещение по Z",
        "Пластическая деформация",
        "Поперечная сила",
        "Поперечная сила по Y",
        "Поперечная сила по Z",
        "Продольная сила",
        "Сила",
        "Удлинение",
        "Удлинение по X",
        "Удлинение по Y",
        "Удлинение по Z",
        "Частота 1",
        "Частота 2",
        "Частота 3",
        "Другое",
    ])

    # Создание первой вкладки
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Создание изображения графика")

    input_frame = ttk.Frame(tab1)
    input_frame.place(x=10, y=10, width=750, height=160)

    # Вспомогательная функция для создания элементов управления осями
    def add_axis_control(parent, label_text, options, y_pos):
        label = ttk.Label(parent, text=label_text)
        label.place(x=10, y=y_pos)
        combo = ttk.Combobox(parent, values=options, state='readonly')
        combo.place(x=200, y=y_pos, width=200)
        combo.current(0)
        entry = create_text(parent, method="entry", height=1, state='disabled', scrollbar=False)
        entry.place(x=450, y=y_pos, width=300)
        entry.place_forget()
        size_label = ttk.Label(parent, text="Выберите размерность:")
        size_label.place(x=combo.winfo_x() + 250, y=combo.winfo_y())
        size_label.place_forget()
        size_combo = ttk.Combobox(parent, values=[], state='readonly')
        size_combo.place(x=combo.winfo_x() + 400, y=combo.winfo_y(), width=100)
        size_combo.place_forget()
        combo.bind(
            "<<ComboboxSelected>>",
            lambda e: on_combo_changeX_Y_labels(combo, entry, size_label, size_combo)
        )
        return combo, entry, size_label, size_combo

    # Поле для заголовка графика
    label_title = ttk.Label(input_frame, text="Укажите название графика:")
    label_title.place(x=10, y=0)
    path_entry_title = create_text(
        input_frame, method="entry", height=1, state='normal', scrollbar=False
    )
    path_entry_title.place(x=10, y=30, width=300)

    # Выбор языка
    label_language = ttk.Label(input_frame, text="Выберите язык:")
    label_language.place(x=550, y=0)
    combo_language = ttk.Combobox(
        input_frame,
        values=["Русский", "Английский"],
        state='readonly'
    )
    combo_language.current(0)
    combo_language.place(x=550, y=30, width=150)

    # Поля для осей X и Y, используя список физических величин
    combo_titleX, path_entry_titleX, label_titleX_size, combo_titleX_size = add_axis_control(
        input_frame, "Выберите величину для оси X:", PHYSICAL_QUANTITIES, 60
    )
    combo_titleY, path_entry_titleY, label_titleY_size, combo_titleY_size = add_axis_control(
        input_frame, "Выберите величину для оси Y:", PHYSICAL_QUANTITIES, 90
    )
    # Фрейм для сохранения файла
    save_frame = ttk.Frame(tab1)
    save_frame.place(x=10, y=300, width=600, height=100)

    # Переменная для чекбокса легенды
    checkbox_var = tk.BooleanVar(value=False)


    # Управление количеством кривых
    label_curves = ttk.Label(input_frame, text="Выберите количество кривых на графике:")
    label_curves.place(x=10, y=120)
    saved_data_curves = []
    curve_options = [str(i) for i in range(1, 6)]
    combo_curves = ttk.Combobox(input_frame, values=curve_options, state='readonly')
    combo_curves.place(x=250, y=120, width=150)
    combo_curves.current(0)  # select '1'

    # Фрейм для полей ввода кривых
    curves_frame = ttk.Frame(tab1)
    curves_frame.place(x=10, y=170, width=1500, height=200)
    update_curves(curves_frame, '1', save_frame, checkbox_var, saved_data_curves)
    combo_curves.bind(
        "<<ComboboxSelected>>",
        lambda e: update_curves(
            curves_frame, combo_curves.get(), save_frame, checkbox_var, saved_data_curves
        )
    )

    # Фрейм для предпросмотра графика
    preview_frame = ttk.Frame(tab1)
    preview_frame.place(x=800, y=30, width=640, height=480)
    
    def show_usage():
        text = (
            "1. Укажите название графика и подписи осей.\n"
            "2. Выберите размерности осей при необходимости.\n"
            "3. Выберите количество кривых и загрузите данные для каждой.\n"
            "4. Нажмите «Построить график» для отображения.\n"
            "5. Для сохранения изображения укажите имя файла и формат, затем нажмите «Сохранить»."
        )
        win = tk.Toplevel(tab1)
        win.title("Как использовать")
        tk.Label(win, text=text, justify=tk.LEFT, wraplength=400).pack(padx=10, pady=10)
        ttk.Button(win, text="Ок", command=win.destroy).pack(pady=(0, 10))

    info_button = ttk.Button(tab1, text="Как использовать", command=show_usage)
    info_button.place(x=800, y=0)
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=preview_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    editor_visible = {"shown": False}
    plot_editor = PlotEditor(tab1, ax, canvas)
    plot_editor.place(x=800, y=560, width=640, height=180)
    plot_editor.place_forget()

    def build_graph():
        generate_graph(
            ax, fig, canvas, path_entry_title,
            combo_titleX, combo_titleX_size, path_entry_titleX,
            combo_titleY, combo_titleY_size, path_entry_titleY,
            checkbox_var, curves_frame, combo_curves, combo_language
        )
        plot_editor.refresh()
        if not editor_visible["shown"]:
            plot_editor.place(x=800, y=560, width=640, height=180)
            editor_visible["shown"] = True

    # Кнопка построения графика
    btn_generate_graph = ttk.Button(
        tab1,
        text="Построить график",
        command=build_graph
    )
    btn_generate_graph.place(x=1050, y=520)

    # Элементы для сохранения файла
    label_save = ttk.Label(save_frame, text="Введите имя файла:")
    label_save.place(x=10, y=0)
    entry_save = create_text(
        save_frame, method="entry", height=1, state='normal', scrollbar=False
    )
    entry_save.place(x=10, y=30, width=300)
    label_format = ttk.Label(save_frame, text="Формат:")
    label_format.place(x=330, y=0)
    combo_format = ttk.Combobox(save_frame, values=["png", "jpg", "svg", "pdf"], state='readonly')
    combo_format.place(x=330, y=30, width=80)
    combo_format.current(0)
    save_button = ttk.Button(
        save_frame,
        text="Сохранить",
        command=lambda: save_file(entry_save, combo_format, last_graph)
    )
    save_button.place(x=420, y=30)

    # Чекбокс легенды
    checkbox = ttk.Checkbutton(
        input_frame,
        text="Легенда",
        variable=checkbox_var,
        command=lambda: update_curves(
            curves_frame, combo_curves.get(), save_frame, checkbox_var, saved_data_curves
        )
    )
    checkbox.place(x=450, y=120)


