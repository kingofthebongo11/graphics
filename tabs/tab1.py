import tkinter as tk  # Alias for Tk functionality
from tkinter import ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def on_combo_changeX_Y_labels(combo, entry, label_size, size_combo):
    """
    Обрабатывает выбор в комбобоксе для осей:
    - Если выбрано "Другое", отображает текстовое поле для ввода и скрывает выбор размерности.
    - Иначе скрывает текстовое поле, показывает метку и комбобокс размерности с нужными единицами.
    """
    UNITS_MAPPING = {
        "Время": ["мс", "с", "мин", "ч"],
        "Перемещение по X": ["мм", "см", "м"],
        "Перемещение по Y": ["мм", "см", "м"],
        "Перемещение по Z": ["мм", "см", "м"],
        "Удлинение": ["мм", "см", "м"],
        "Деформация": ["%"],
        "Сила": ["мН", "Н", "кН"],
        "Масса": ["г", "кг", "т"],
        "Напряжение": ["Па", "кПа", "МПа"],
        "Частота 1": ["Гц", "кГц"],
        "Частота 2": ["Гц", "кГц"],
        "Частота 3": ["Гц", "кГц"],
        "Другое": []
    }
    selection = combo.get()
    if selection == "Другое":
        if not entry.winfo_ismapped():
            entry.place(x=combo.winfo_x() + 200, y=combo.winfo_y(), width=300)
            entry.config(state='normal')
        label_size.place_forget()
        size_combo.place_forget()
    else:
        entry.place_forget()
        label_size.place(x=combo.winfo_x() + 200, y=combo.winfo_y())
        values = UNITS_MAPPING.get(selection, [])
        size_combo['values'] = values
        if values:
            size_combo.place(x=combo.winfo_x() + 350, y=combo.winfo_y(), width=150)
        else:
            size_combo.place_forget()


def create_tab1(notebook, create_text, update_curves, generate_graph, save_file):
    # Список физических величин для прочностных расчетов
    PHYSICAL_QUANTITIES = [
        "Время", "Деформация", "Масса", "Напряжение",
        "Перемещение по X", "Перемещение по Y", "Перемещение по Z",
        "Сила", "Удлинение", "Частота 1", "Частота 2", "Частота 3",
        "Другое",

    ]

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
        combo.place(x=200, y=y_pos, width=150)
        entry = create_text(parent, method="entry", height=1, state='disabled', scrollbar=False)
        entry.place(x=400, y=y_pos, width=300)
        entry.place_forget()
        size_label = ttk.Label(parent, text="Выберите размерность:")
        size_label.place(x=combo.winfo_x() + 200, y=combo.winfo_y())
        size_label.place_forget()
        size_combo = ttk.Combobox(parent, values=[], state='readonly')
        size_combo.place(x=combo.winfo_x() + 350, y=combo.winfo_y(), width=150)
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
    combo_language.place(x=550, y=30, width=150)

    # Поля для осей X и Y, используя список физических величин
    combo_titleX, path_entry_titleX, label_titleX_size, combo_titleX_size = add_axis_control(
        input_frame, "Выберите величину для оси X:", PHYSICAL_QUANTITIES, 60
    )
    combo_titleY, path_entry_titleY, label_titleY_size, combo_titleY_size = add_axis_control(
        input_frame, "Выберите величину для оси Y:", PHYSICAL_QUANTITIES, 90
    )

    # Управление количеством кривых
    label_curves = ttk.Label(input_frame, text="Выберите количество кривых на графике:")
    label_curves.place(x=10, y=120)
    saved_data_curves = []
    curve_options = [str(i) for i in range(1, 6)]
    combo_curves = ttk.Combobox(input_frame, values=curve_options, state='readonly')
    combo_curves.place(x=250, y=120, width=150)

    # Прокручиваемая область для полей ввода кривых
    curves_canvas = tk.Canvas(tab1)
    curves_canvas.place(x=10, y=170, width=1460, height=0)

    curves_scrollbar = ttk.Scrollbar(tab1, orient="vertical", command=curves_canvas.yview)
    curves_canvas.configure(yscrollcommand=curves_scrollbar.set)
    curves_scrollbar.place_forget()

    curves_frame = ttk.Frame(curves_canvas)
    curves_canvas.create_window((0, 0), window=curves_frame, anchor="nw", width=1460)

    combo_curves.bind(
        "<<ComboboxSelected>>",
        lambda e: update_curves(
            curves_frame, combo_curves.get(), save_frame, checkbox_var, saved_data_curves, curves_canvas, curves_scrollbar
        )
    )

    # Фрейм для предпросмотра графика
    preview_frame = ttk.Frame(tab1)
    preview_frame.place(x=800, y=200, width=640, height=480)
    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, master=preview_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Кнопка построения графика
    btn_generate_graph = ttk.Button(
        tab1,
        text="Построить график",
        command=lambda: generate_graph(
            ax, fig, canvas, path_entry_title,
            combo_titleX, combo_titleX_size,
            combo_titleY, combo_titleY_size,
            checkbox_var, curves_frame, combo_curves
        )
    )
    btn_generate_graph.place(x=1050, y=690)

    # Фрейм и элементы для сохранения файла
    save_frame = ttk.Frame(tab1)
    save_frame.place(x=10, y=300, width=600, height=100)
    label_save = ttk.Label(save_frame, text="Введите имя файла:")
    label_save.place(x=10, y=0)
    entry_save = create_text(
        save_frame, method="entry", height=1, state='normal', scrollbar=False
    )
    entry_save.place(x=10, y=30, width=300)
    save_button = ttk.Button(
        save_frame,
        text="Сохранить",
        command=lambda: save_file(entry_save, {})
    )
    save_button.place(x=330, y=30)

    # Чекбокс легенды
    checkbox_var = tk.BooleanVar(value=False)
    checkbox = ttk.Checkbutton(
        input_frame,
        text="Легенда",
        variable=checkbox_var,
        command=lambda: update_curves(
            curves_frame, combo_curves.get(), save_frame, checkbox_var, saved_data_curves, curves_canvas, curves_scrollbar
        )
    )
    checkbox.place(x=450, y=120)


