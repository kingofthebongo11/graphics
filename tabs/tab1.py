from logging_utils import get_logger
import tkinter as tk  # Alias for Tk functionality
from tkinter import ttk, messagebox
from typing import Dict, List, Tuple
from .functions_for_tab1 import (
    update_curves,
    generate_graph,
    save_file,
    apply_axis_limits,
)
from .functions_for_tab1.plotting import last_graph
from widgets import PlotEditor, create_text
from tabs.function_for_all_tabs import create_plot_canvas
from .constants import (
    DEFAULT_UNITS,
    PHYSICAL_QUANTITIES,
    UNITS_MAPPING,
    LEGEND_TITLE_TRANSLATIONS,
)
from ui import constants as ui_const


logger = get_logger(__name__)


def on_title_combo_change(
    combo: ttk.Combobox,
    entry: tk.Entry,
    title_var: tk.StringVar,
) -> None:
    """Обновляет выбор заголовка графика.

    При выборе "Другое" отображает поле ввода и сохраняет выбранный вариант.
    При выборе готового варианта скрывает поле ввода и устанавливает
    выбранный текст в переменную заголовка.
    """

    other_label = "Другое"

    selection = combo.get()
    if selection == other_label:
        entry.place(
            x=combo.winfo_x() + ui_const.LABEL_SIZE_OFFSET,
            y=combo.winfo_y(),
            width=ui_const.ENTRY_WIDTH,
        )
        title_var.set(other_label)
    else:
        entry.place_forget()
        title_var.set(selection)


def on_legend_title_change(
    combo: ttk.Combobox,
    entry: tk.Entry,
    title_var: tk.StringVar,
    language: str,
) -> None:
    """Обрабатывает выбор подписи легенды.

    Если выбран вариант «Другое», показывает поле ввода и сохраняет выбор.
    Иначе скрывает поле ввода и записывает выбранный текст в переменную.
    """

    other_label = LEGEND_TITLE_TRANSLATIONS["Другое"].get(language, "Другое")

    selection = combo.get()
    if selection == other_label:
        combo.place_forget()
        entry.place(
            x=ui_const.LEGEND_TITLE_ENTRY_X,
            y=ui_const.LEGEND_TITLE_Y,
            width=ui_const.ENTRY_WIDTH,
        )
        title_var.set(other_label)
    else:
        combo.place(
            x=ui_const.LEGEND_TITLE_COMBO_X,
            y=ui_const.LEGEND_TITLE_Y,
            width=ui_const.COMBO_WIDTH,
        )
        entry.place_forget()
        title_var.set(selection)


def on_combo_changeX_Y_labels(
    combo: ttk.Combobox,
    entry: tk.Entry,
    label_size: ttk.Label,
    size_combo: ttk.Combobox,
    size_entry: tk.Entry,
) -> None:
    """
    Обрабатывает выбор в комбобоксе для осей:
    - Если выбрано "Другое", отображает текстовое поле для ввода и скрывает выбор размерности.
    - Иначе скрывает текстовое поле, показывает метку и комбобокс размерности с нужными единицами.
    """

    other_label = "Другое"
    none_label = "Нет"
    units_mapping = UNITS_MAPPING
    default_units = DEFAULT_UNITS

    selection = combo.get()
    logger.info("Выбор в комбобоксе: %s", selection)
    if selection == other_label:
        logger.debug("Показ поля ввода для пользовательской величины")
        if not entry.winfo_ismapped():
            entry.place(
                x=ui_const.AXIS_ENTRY_X,
                y=combo.winfo_y(),
                width=ui_const.ENTRY_WIDTH,
            )
            entry.config(state="normal")
        label_size.place_forget()
        size_combo.place_forget()
        size_entry.place_forget()
        size_combo["values"] = []
        size_combo.set("")
    elif selection == none_label:
        logger.debug("Скрытие элементов оси")
        entry.place_forget()
        label_size.place_forget()
        size_combo.place_forget()
        size_entry.place_forget()
        size_combo["values"] = []
        size_combo.set("")
    else:
        logger.debug("Выбрана стандартная величина: %s", selection)
        entry.place_forget()
        size_entry.place_forget()
        label_size.place(
            x=ui_const.AXIS_LABEL_SIZE_X,
            y=combo.winfo_y(),
        )
        values = units_mapping.get(selection, [])
        size_combo["values"] = values
        size_combo.set("")
        if values:
            size_combo.place(
                x=ui_const.AXIS_UNIT_X,
                y=combo.winfo_y(),
                width=ui_const.SIZE_COMBO_WIDTH,
            )
            default_unit = default_units.get(selection)
            if default_unit in values:
                size_combo.current(values.index(default_unit))
        else:
            size_combo.place_forget()


def on_unit_change(size_combo: ttk.Combobox, size_entry: tk.Entry) -> None:
    """Обрабатывает выбор единицы измерения.

    При выборе «Другое» скрывает комбобокс и показывает поле ввода.
    При выборе «Нет» скрывает поле ввода.
    """

    selection = size_combo.get()
    if selection == "Другое":
        size_combo.place_forget()
        size_entry.place(
            x=ui_const.AXIS_UNIT_X,
            y=size_combo.winfo_y(),
            width=ui_const.SIZE_COMBO_WIDTH,
        )
    elif selection == "Нет":
        size_entry.place_forget()
    else:
        size_entry.place_forget()

def create_tab1(notebook: ttk.Notebook) -> None:
    """Создает первую вкладку для построения графика.

    Параметры:
        notebook: виджет, в который добавляется вкладка.

    Возвращает:
        None.
    """

    logger.info("Создание первой вкладки")
    # Создание первой вкладки
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Создание изображения графика")

    input_frame = ttk.Frame(tab1)
    input_frame.place(
        x=ui_const.PADDING,
        y=ui_const.PADDING,
        width=ui_const.INPUT_FRAME_WIDTH,
        height=ui_const.INPUT_FRAME_HEIGHT,
    )

    # Вспомогательная функция для создания элементов управления осями
    def add_axis_control(
        parent: ttk.Frame,
        label_text: str,
        options: List[str],
        y_pos: int,
    ) -> Tuple[ttk.Combobox, tk.Entry, ttk.Label, ttk.Combobox, tk.Entry]:
        logger.debug("Добавление элементов управления для %s", label_text)
        label = ttk.Label(parent, text=label_text)
        label.place(x=ui_const.PADDING, y=y_pos)
        combo = ttk.Combobox(parent, values=options, state="readonly")
        combo.place(
            x=ui_const.AXIS_COMBO_X,
            y=y_pos,
            width=ui_const.COMBO_WIDTH,
        )
        combo.current(0)
        entry = create_text(
            parent, method="entry", height=1, state="disabled", scrollbar=False
        )
        entry.place(
            x=ui_const.AXIS_ENTRY_X,
            y=y_pos,
            width=ui_const.ENTRY_WIDTH,
        )
        entry.place_forget()
        size_label = ttk.Label(parent, text="Выберите размерность:")
        size_label.place(
            x=ui_const.AXIS_LABEL_SIZE_X,
            y=combo.winfo_y(),
        )
        size_label.place_forget()
        size_combo = ttk.Combobox(parent, values=[], state="readonly")
        size_combo.place(
            x=ui_const.AXIS_UNIT_X,
            y=combo.winfo_y(),
            width=ui_const.SIZE_COMBO_WIDTH,
        )
        size_combo.place_forget()
        size_entry = create_text(
            parent, method="entry", height=1, state="normal", scrollbar=False
        )
        size_entry.place(
            x=ui_const.AXIS_UNIT_X,
            y=combo.winfo_y(),
            width=ui_const.SIZE_COMBO_WIDTH,
        )
        size_entry.place_forget()
        combo.bind(
            "<<ComboboxSelected>>",
            lambda e: on_combo_changeX_Y_labels(
                combo, entry, size_label, size_combo, size_entry
            ),
        )
        size_combo.bind(
            "<<ComboboxSelected>>",
            lambda e: on_unit_change(size_combo, size_entry),
        )
        return combo, entry, size_label, size_combo, size_entry

    # Поле для заголовка графика
    label_title = ttk.Label(
        input_frame, text="Выберите или введите название графика:"
    )
    label_title.place(x=ui_const.PADDING, y=0)
    title_var = tk.StringVar()
    combo_title = ttk.Combobox(
        input_frame,
        values=PHYSICAL_QUANTITIES,
        state="readonly",
        textvariable=title_var,
    )
    combo_title.place(
        x=ui_const.PADDING,
        y=ui_const.LINE_HEIGHT,
        width=ui_const.COMBO_WIDTH,
    )
    combo_title.current(0)
    entry_title_custom = create_text(
        input_frame, method="entry", height=1, state="normal", scrollbar=False
    )
    entry_title_custom.place(
        x=ui_const.PADDING,
        y=ui_const.LINE_HEIGHT,
        width=ui_const.ENTRY_WIDTH,
    )
    entry_title_custom.place_forget()

    # Выбор языка
    label_language = ttk.Label(input_frame, text="Выберите язык:")
    label_language.place(x=ui_const.LANGUAGE_X, y=0)
    combo_language = ttk.Combobox(
        input_frame, values=["Русский", "Английский"], state="readonly"
    )
    combo_language.current(0)
    combo_language.place(
        x=ui_const.LANGUAGE_X,
        y=ui_const.LINE_HEIGHT,
        width=ui_const.SMALL_COMBO_WIDTH,
    )

    # Подпись легенды
    legend_title_var = tk.StringVar()
    legend_title_combo = ttk.Combobox(
        input_frame,
        state="readonly",
        textvariable=legend_title_var,
    )
    legend_title_entry = create_text(
        input_frame, method="entry", height=1, state="normal", scrollbar=False
    )
    legend_title_entry.place_forget()
    legend_title_combo.bind(
        "<<ComboboxSelected>>",
        lambda e: on_legend_title_change(
            legend_title_combo,
            legend_title_entry,
            legend_title_var,
            combo_language.get() or "Русский",
        ),
    )

    # Поля для осей X и Y, используя список физических величин
    (
        combo_titleX,
        path_entry_titleX,
        label_titleX_size,
        combo_titleX_size,
        combo_titleX_size_entry,
    ) = add_axis_control(
        input_frame,
        "Выберите величину для оси X:",
        PHYSICAL_QUANTITIES,
        ui_const.LINE_HEIGHT * 2,
    )
    (
        combo_titleY,
        path_entry_titleY,
        label_titleY_size,
        combo_titleY_size,
        combo_titleY_size_entry,
    ) = add_axis_control(
        input_frame,
        "Выберите величину для оси Y:",
        PHYSICAL_QUANTITIES,
        ui_const.LINE_HEIGHT * 3,
    )
    combo_title.bind(
        "<<ComboboxSelected>>",
        lambda e: on_title_combo_change(
            combo_title, entry_title_custom, title_var
        ),
    )

    def on_language_change(event=None) -> None:
        on_title_combo_change(combo_title, entry_title_custom, title_var)
        on_combo_changeX_Y_labels(
            combo_titleX,
            path_entry_titleX,
            label_titleX_size,
            combo_titleX_size,
            combo_titleX_size_entry,
        )
        on_combo_changeX_Y_labels(
            combo_titleY,
            path_entry_titleY,
            label_titleY_size,
            combo_titleY_size,
            combo_titleY_size_entry,
        )
        language = combo_language.get() or "Русский"
        legend_titles = [
            values.get(language, key)
            for key, values in LEGEND_TITLE_TRANSLATIONS.items()
        ]
        legend_title_combo["values"] = legend_titles
        if legend_titles:
            legend_title_combo.current(0)
            legend_title_var.set(legend_title_combo.get())
        legend_title_entry.place_forget()

    combo_language.bind("<<ComboboxSelected>>", on_language_change)
    on_language_change()
    # Фрейм для сохранения файла
    save_frame = ttk.Frame(tab1)
    save_frame.place(
        x=ui_const.PADDING,
        y=ui_const.SAVE_FRAME_Y,
        width=ui_const.SAVE_FRAME_WIDTH,
        height=ui_const.SAVE_FRAME_HEIGHT,
    )

    # Переменная для чекбокса легенды
    checkbox_var = tk.BooleanVar(value=False)

    def toggle_legend_title_visibility() -> None:
        if checkbox_var.get():
            legend_title_combo.place(
                x=ui_const.LEGEND_TITLE_COMBO_X,
                y=ui_const.LEGEND_TITLE_Y,
                width=ui_const.COMBO_WIDTH,
            )
            if not legend_title_var.get() and legend_title_combo["values"]:
                legend_title_combo.current(0)
                legend_title_var.set(legend_title_combo.get())
        else:
            legend_title_combo.place_forget()
            legend_title_entry.place_forget()
            legend_title_var.set("")

    # Управление количеством кривых
    label_curves = ttk.Label(
        input_frame, text="Выберите количество кривых на графике:"
    )
    label_curves.place(x=ui_const.PADDING, y=ui_const.CURVE_LABEL_Y)
    saved_data_curves = []
    curve_options = [str(i) for i in range(1, 6)]
    combo_curves = ttk.Combobox(
        input_frame, values=curve_options, state="readonly"
    )
    combo_curves.place(
        x=ui_const.CURVE_COMBO_X,
        y=ui_const.CURVE_LABEL_Y,
        width=ui_const.SMALL_COMBO_WIDTH,
    )
    combo_curves.current(0)  # select '1'

    # Фрейм для полей ввода кривых
    curves_frame = ttk.Frame(tab1)
    curves_frame.place(
        x=ui_const.PADDING,
        y=ui_const.CURVES_FRAME_Y,
        width=ui_const.CURVES_FRAME_WIDTH,
        height=ui_const.CURVES_FRAME_HEIGHT,
    )
    axis_frame = ttk.LabelFrame(tab1, text="Настройки осей")
    axis_frame.place(
        x=ui_const.PREVIEW_X,
        y=ui_const.AXIS_FRAME_Y,
        width=ui_const.AXIS_FRAME_WIDTH,
        height=ui_const.AXIS_FRAME_HEIGHT,
    )
    axis_frame.linked_to_curves = False
    for column in (2, 4):
        axis_frame.columnconfigure(column, weight=1)

    def _create_auto_entry() -> tk.Entry:
        entry = create_text(
            axis_frame, method="entry", height=1, state="normal", scrollbar=False
        )
        entry.insert(0, "-")
        entry.config(state="readonly", width=12)
        return entry

    def _mark_manual_modified(entry: tk.Entry) -> None:
        entry.user_modified = True

    def _handle_manual_focus_out(entry: tk.Entry) -> None:
        if not entry.get().strip():
            entry.user_modified = False

    def _create_manual_entry() -> tk.Entry:
        entry = create_text(
            axis_frame, method="entry", height=1, state="normal", scrollbar=False
        )
        entry.config(width=12)
        entry.user_modified = False

        entry.bind("<KeyRelease>", lambda _event, e=entry: _mark_manual_modified(e))
        entry.bind("<<Paste>>", lambda _event, e=entry: _mark_manual_modified(e))
        entry.bind("<<Cut>>", lambda _event, e=entry: _mark_manual_modified(e))
        entry.bind("<FocusOut>", lambda _event, e=entry: _handle_manual_focus_out(e))

        return entry

    ttk.Label(axis_frame, text="Ось X (авто):").grid(
        row=0, column=0, padx=5, pady=2, sticky="w"
    )
    ttk.Label(axis_frame, text="от").grid(row=0, column=1, padx=5, pady=2)
    auto_x_min_entry = _create_auto_entry()
    auto_x_min_entry.grid(row=0, column=2, padx=5, pady=2, sticky="ew")
    ttk.Label(axis_frame, text="до").grid(row=0, column=3, padx=5, pady=2)
    auto_x_max_entry = _create_auto_entry()
    auto_x_max_entry.grid(row=0, column=4, padx=5, pady=2, sticky="ew")

    ttk.Label(axis_frame, text="Ось X (вручную):").grid(
        row=1, column=0, padx=5, pady=2, sticky="w"
    )
    ttk.Label(axis_frame, text="от").grid(row=1, column=1, padx=5, pady=2)
    manual_x_min_entry = _create_manual_entry()
    manual_x_min_entry.grid(row=1, column=2, padx=5, pady=2, sticky="ew")
    ttk.Label(axis_frame, text="до").grid(row=1, column=3, padx=5, pady=2)
    manual_x_max_entry = _create_manual_entry()
    manual_x_max_entry.grid(row=1, column=4, padx=5, pady=2, sticky="ew")

    ttk.Label(axis_frame, text="Ось Y (авто):").grid(
        row=2, column=0, padx=5, pady=2, sticky="w"
    )
    ttk.Label(axis_frame, text="от").grid(row=2, column=1, padx=5, pady=2)
    auto_y_min_entry = _create_auto_entry()
    auto_y_min_entry.grid(row=2, column=2, padx=5, pady=2, sticky="ew")
    ttk.Label(axis_frame, text="до").grid(row=2, column=3, padx=5, pady=2)
    auto_y_max_entry = _create_auto_entry()
    auto_y_max_entry.grid(row=2, column=4, padx=5, pady=2, sticky="ew")

    ttk.Label(axis_frame, text="Ось Y (вручную):").grid(
        row=3, column=0, padx=5, pady=2, sticky="w"
    )
    ttk.Label(axis_frame, text="от").grid(row=3, column=1, padx=5, pady=2)
    manual_y_min_entry = _create_manual_entry()
    manual_y_min_entry.grid(row=3, column=2, padx=5, pady=2, sticky="ew")
    ttk.Label(axis_frame, text="до").grid(row=3, column=3, padx=5, pady=2)
    manual_y_max_entry = _create_manual_entry()
    manual_y_max_entry.grid(row=3, column=4, padx=5, pady=2, sticky="ew")

    axis_apply_button = ttk.Button(
        axis_frame,
        text="Применить",
        command=lambda: apply_axis_limits(ax, canvas, axis_manual_entries),
    )
    axis_apply_button.grid(
        row=4, column=0, columnspan=5, padx=5, pady=(4, 8), sticky="e"
    )

    ttk.Separator(axis_frame, orient=tk.HORIZONTAL).grid(
        row=5, column=0, columnspan=5, sticky="ew", pady=(4, 4)
    )

    annotation_frame = ttk.Frame(axis_frame)
    annotation_frame.grid(row=6, column=0, columnspan=5, sticky="ew")
    annotation_frame.columnconfigure(2, weight=1)

    annotation_mode_var = tk.BooleanVar(value=False)
    annotation_type_var = tk.StringVar(value="(X,Y)")

    annotation_mode_check = ttk.Checkbutton(
        annotation_frame, text="Режим отметок", variable=annotation_mode_var
    )
    annotation_mode_check.grid(row=0, column=0, padx=5, pady=2, sticky="w")
    ttk.Label(annotation_frame, text="Подпись:").grid(
        row=0, column=1, padx=5, pady=2, sticky="w"
    )
    annotation_type_combo = ttk.Combobox(
        annotation_frame,
        values=["X", "Y", "(X,Y)", "Свой текст"],
        state="readonly",
        textvariable=annotation_type_var,
        width=12,
    )
    annotation_type_combo.grid(row=0, column=2, padx=5, pady=2, sticky="w")

    ttk.Label(annotation_frame, text="Текст:").grid(
        row=1, column=0, padx=5, pady=2, sticky="w"
    )
    annotation_text_entry = create_text(
        annotation_frame, method="entry", height=1, state="disabled", scrollbar=False
    )
    annotation_text_entry.grid(
        row=1, column=1, columnspan=2, padx=5, pady=2, sticky="ew"
    )
    clear_annotations_button = ttk.Button(
        annotation_frame, text="Очистить отметки"
    )
    clear_annotations_button.grid(row=1, column=3, padx=5, pady=2, sticky="e")

    def update_annotation_entry_state(_event=None) -> None:
        if annotation_type_var.get() == "Свой текст":
            annotation_text_entry.config(state="normal")
        else:
            annotation_text_entry.delete(0, tk.END)
            annotation_text_entry.config(state="disabled")

    annotation_type_combo.bind("<<ComboboxSelected>>", update_annotation_entry_state)
    update_annotation_entry_state()

    axis_auto_entries: Dict[str, tk.Entry] = {
        "x_min": auto_x_min_entry,
        "x_max": auto_x_max_entry,
        "y_min": auto_y_min_entry,
        "y_max": auto_y_max_entry,
    }
    axis_manual_entries: Dict[str, tk.Entry] = {
        "x_min": manual_x_min_entry,
        "x_max": manual_x_max_entry,
        "y_min": manual_y_min_entry,
        "y_max": manual_y_max_entry,
    }

    def reset_manual_entries() -> None:
        for entry in axis_manual_entries.values():
            entry.delete(0, tk.END)
            entry.user_modified = False

    def reset_saved_ranges() -> None:
        for curve_state in saved_data_curves:
            if isinstance(curve_state, dict):
                curve_state["slider_start"] = 0.0
                curve_state["slider_end"] = 100.0

    update_curves(curves_frame, "1", axis_frame, save_frame, checkbox_var, saved_data_curves)
    combo_curves.bind(
        "<<ComboboxSelected>>",
        lambda e: update_curves(
            curves_frame,
            combo_curves.get(),
            axis_frame,
            save_frame,
            checkbox_var,
            saved_data_curves,
        ),
    )

    # Фрейм для предпросмотра графика
    preview_frame = ttk.Frame(tab1)
    preview_frame.place(
        x=ui_const.PREVIEW_X,
        y=ui_const.LINE_HEIGHT,
        width=ui_const.PREVIEW_WIDTH,
        height=ui_const.PREVIEW_HEIGHT,
    )

    def show_usage() -> None:
        logger.info("Отображение инструкции по использованию")
        text = (
            "1. В верхней части вкладки выберите язык интерфейса — он влияет на подписи осей, заголовки и элементы управления.\n"
            "2. Выберите заголовок графика из списка или пункт «Другое» для ввода собственного текста.\n"
            "3. Для осей X и Y выберите величину из списка: вариант «Другое» позволяет ввести своё название, а «Нет» скрывает название и единицы; при необходимости задайте размерность.\n"
            "При выборе «Нет» в комбобоксах заголовка графика и осей подпись не отображается.\n"
            "4. Выберите количество кривых и загрузите данные для каждой; при необходимости активируйте чекбокс «Легенда» и введите подпись кривой. Без включённой легенды подписи не отображаются.\n"
            "5. Поддерживаемые форматы данных: текстовые файлы (*.txt, *.dat) — каждая строка содержит два числа; Excel-файлы (*.xlsx, *.xlsm, *.csv) с двумя столбцами или строками и возможностью указания диапазонов; файлы кривых LS-DYNA; результаты частотного анализа LS-DYNA.\n"
            "6. Дополнительные настройки: для Excel можно менять ориентацию (строки/столбцы), задавать смещения и диапазоны; для частотного анализа выбираются параметр и направление; при чтении LS-DYNA проверяются служебные маркеры и игнорируются строки-комментарии.\n"
            "7. Нажмите «Построить график» для отображения.\n"
            "8. После построения графика откроется редактор, где можно изменять цвет, толщину и стиль линий, "
            "применять цветовые палитры; все изменения сразу видны на графике.\n"
            "9. Для сохранения изображения сначала введите имя файла, затем выберите формат (png, jpg, svg, pdf) и нажмите «Сохранить». "
            "Файл сохраняется в текущей рабочей директории приложения, если не указано иное."
        )
        win = tk.Toplevel(tab1)
        win.withdraw()
        win.title("Как использовать")
        tk.Label(
            win, text=text, justify=tk.LEFT, wraplength=ui_const.WRAP_LENGTH
        ).pack(padx=ui_const.PADDING, pady=ui_const.PADDING)
        ttk.Button(win, text="Ок", command=win.destroy).pack(
            pady=(0, ui_const.PADDING)
        )

        win.update_idletasks()
        width = win.winfo_reqwidth()
        height = win.winfo_reqheight()
        x = (win.winfo_screenwidth() - width) // 2
        y = (win.winfo_screenheight() - height) // 2
        win.geometry(f"{width}x{height}+{x}+{y}")
        win.transient(tab1.winfo_toplevel())
        win.grab_set()
        win.lift()
        win.attributes("-topmost", True)
        win.deiconify()

    info_button = ttk.Button(tab1, text="Как использовать", command=show_usage)
    info_button.place(x=ui_const.PREVIEW_X, y=0)
    fig, ax, canvas = create_plot_canvas(preview_frame)

    annotations: list = []

    def _redraw_canvas() -> None:
        if hasattr(canvas, "draw_idle"):
            canvas.draw_idle()
        else:
            canvas.draw()

    def clear_annotations() -> None:
        while annotations:
            point, label = annotations.pop()
            try:
                point.remove()
            except ValueError:
                pass
            try:
                label.remove()
            except ValueError:
                pass
        _redraw_canvas()

    def _format_annotation_text(x_value: float, y_value: float) -> str:
        mode = annotation_type_var.get()
        if mode == "X":
            return f"{x_value:.3g}"
        if mode == "Y":
            return f"{y_value:.3g}"
        if mode == "(X,Y)":
            return f"({x_value:.3g}, {y_value:.3g})"
        return annotation_text_entry.get().strip()

    def on_canvas_click(event) -> None:
        if not annotation_mode_var.get():
            return
        if event.inaxes != ax or event.xdata is None or event.ydata is None:
            return
        if hasattr(event, "button") and event.button != 1:
            return
        text = _format_annotation_text(event.xdata, event.ydata)
        if annotation_type_var.get() == "Свой текст" and not text:
            messagebox.showwarning(
                "Предупреждение", "Введите текст подписи для отметки."
            )
            return
        point = ax.scatter([event.xdata], [event.ydata], color="red", zorder=5)
        label = ax.annotate(
            text,
            (event.xdata, event.ydata),
            textcoords="offset points",
            xytext=(5, 5),
            color="red",
            fontsize=9,
        )
        annotations.append((point, label))
        _redraw_canvas()

    canvas.mpl_connect("button_press_event", on_canvas_click)
    clear_annotations_button.config(command=clear_annotations)

    editor_visible = {"shown": False}
    plot_editor = PlotEditor(tab1, ax, canvas, saved_data_curves)
    plot_editor.place(
        x=ui_const.EDITOR_X,
        y=ui_const.EDITOR_Y,
        width=ui_const.PREVIEW_WIDTH,
        height=plot_editor.required_height,
    )
    plot_editor.place_forget()

    def reset_auto_entries() -> None:
        for entry in axis_auto_entries.values():
            state = entry.cget("state")
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, "-")
            entry.config(state=state)

    def build_graph() -> None:
        logger.info("Построение графика")
        clear_annotations()
        reset_manual_entries()
        reset_auto_entries()
        reset_saved_ranges()
        if hasattr(ax, "set_xlim") and hasattr(ax, "set_ylim"):
            ax.set_xlim(auto=True)
            ax.set_ylim(auto=True)
        if hasattr(ax, "set_autoscale_on"):
            ax.set_autoscale_on(True)
        plot_editor.reset_axes_lock()
        try:
            generate_graph(
                ax,
                fig,
                canvas,
                combo_title,
                entry_title_custom,
                combo_titleX,
                combo_titleX_size,
                path_entry_titleX,
                combo_titleY,
                combo_titleY_size,
                path_entry_titleY,
                checkbox_var,
                curves_frame,
                combo_curves,
                combo_language,
                legend_title_combo,
                legend_title_entry,
                legend_title_var,
                axis_auto_entries,
                axis_manual_entries,
            )
            plot_editor.refresh()
            plot_editor.reset_ranges()
            editor_height = plot_editor.required_height
            if not editor_visible["shown"]:
                plot_editor.place(
                    x=ui_const.EDITOR_X,
                    y=ui_const.EDITOR_Y,
                    width=ui_const.PREVIEW_WIDTH,
                    height=editor_height,
                )
                editor_visible["shown"] = True
            elif editor_height:
                plot_editor.place_configure(height=editor_height)
            logger.info("График построен успешно")
        except ValueError as exc:
            logger.error("Ошибка построения графика", exc_info=True)
            messagebox.showerror("Ошибка", f"Не удалось построить график:\n{exc}")
        except Exception as exc:
            logger.exception("Ошибка при построении графика")
            messagebox.showerror(
                "Ошибка",
                f"Не удалось построить график:\n{exc}\nПроверьте введённые данные и попробуйте снова.",
            )

    # Кнопка построения графика
    btn_generate_graph = ttk.Button(tab1, text="Построить график", command=build_graph)
    btn_generate_graph.place(x=ui_const.BUTTON_BUILD_X, y=ui_const.BUTTON_BUILD_Y)

    # Элементы для сохранения файла
    label_save = ttk.Label(save_frame, text="Введите имя файла:")
    label_save.place(x=ui_const.PADDING, y=0)
    entry_save = create_text(
        save_frame, method="entry", height=1, state="normal", scrollbar=False
    )
    entry_save.place(
        x=ui_const.PADDING,
        y=ui_const.LINE_HEIGHT,
        width=ui_const.ENTRY_WIDTH,
    )
    label_format = ttk.Label(save_frame, text="Формат:")
    label_format.place(x=ui_const.FORMAT_LABEL_X, y=0)
    combo_format = ttk.Combobox(
        save_frame, values=["png", "jpg", "svg", "pdf"], state="readonly"
    )
    combo_format.place(
        x=ui_const.FORMAT_LABEL_X,
        y=ui_const.LINE_HEIGHT,
        width=ui_const.FORMAT_COMBO_WIDTH,
    )
    combo_format.current(0)
    save_button = ttk.Button(
        save_frame,
        text="Сохранить",
        command=lambda: save_file(entry_save, combo_format, last_graph),
    )
    save_button.place(x=ui_const.SAVE_BUTTON_X, y=ui_const.LINE_HEIGHT)

    # Чекбокс легенды
    def on_legend_checkbox_toggle() -> None:
        update_curves(
            curves_frame,
            combo_curves.get(),
            axis_frame,
            save_frame,
            checkbox_var,
            saved_data_curves,
        )
        toggle_legend_title_visibility()

    checkbox = ttk.Checkbutton(
        input_frame,
        text="Легенда",
        variable=checkbox_var,
        command=on_legend_checkbox_toggle,
    )
    checkbox.place(x=ui_const.CHECKBOX_X, y=ui_const.CURVE_LABEL_Y)
    toggle_legend_title_visibility()
