import math

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
from tabs.function_for_all_tabs.plotting import LABEL_SIZE
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

    # Контейнер с прокруткой для всей вкладки
    scroll_container = ttk.Frame(tab1)
    scroll_container.pack(fill=tk.BOTH, expand=True)

    scroll_canvas = tk.Canvas(scroll_container, highlightthickness=0)
    scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(
        scroll_container, orient=tk.VERTICAL, command=scroll_canvas.yview
    )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar_visible = {"value": True}
    scroll_needed = {"value": False}

    content_frame = ttk.Frame(scroll_canvas)
    content_window = scroll_canvas.create_window((0, 0), window=content_frame, anchor="nw")

    def _refresh_scrollregion() -> None:
        """Обновляет размеры прокручиваемого содержимого."""

        content_frame.update_idletasks()
        children = [child for child in content_frame.winfo_children() if child.winfo_ismapped()]
        if children:
            max_width = max(child.winfo_x() + child.winfo_width() for child in children)
            max_height = max(child.winfo_y() + child.winfo_height() for child in children)
        else:
            max_width = max_height = 0

        required_width = max_width + ui_const.PADDING
        required_height = max_height + ui_const.PADDING
        canvas_width = scroll_canvas.winfo_width()
        canvas_height = scroll_canvas.winfo_height()

        if canvas_width <= 1:
            canvas_width = scroll_canvas.winfo_reqwidth()
        if canvas_height <= 1:
            canvas_height = scroll_canvas.winfo_reqheight()

        content_width = max(canvas_width, required_width)
        content_height = max(required_height, 0)

        needs_scroll = content_height > canvas_height
        scroll_needed["value"] = needs_scroll

        if needs_scroll:
            if not scrollbar_visible["value"]:
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                scrollbar_visible["value"] = True
            scroll_canvas.configure(yscrollcommand=scrollbar.set)
        else:
            if scrollbar_visible["value"]:
                scrollbar.pack_forget()
                scrollbar_visible["value"] = False
            scroll_canvas.configure(yscrollcommand=None)
            scroll_canvas.yview_moveto(0)

        scroll_canvas.itemconfigure(
            content_window, width=content_width, height=content_height
        )
        content_frame.configure(width=content_width, height=content_height)
        scrollregion_height = content_height if needs_scroll else canvas_height
        scroll_canvas.configure(
            scrollregion=(0, 0, content_width, max(scrollregion_height, 0))
        )

    def _schedule_refresh(_event=None) -> None:
        scroll_canvas.after_idle(_refresh_scrollregion)

    def _trigger_scroll_check() -> None:
        """Планирует проверку необходимости прокрутки."""
        _schedule_refresh()

    content_frame.bind("<Configure>", _schedule_refresh)
    scroll_canvas.bind("<Configure>", _schedule_refresh)

    def _on_mousewheel(event) -> None:
        if not scroll_needed["value"]:
            return

        if event.delta:
            scroll_canvas.yview_scroll(int(-event.delta / 120), "units")
        elif event.num == 4:
            scroll_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            scroll_canvas.yview_scroll(1, "units")

        first, last = scroll_canvas.yview()
        if first < 0:
            scroll_canvas.yview_moveto(0)
        elif last > 1:
            scroll_canvas.yview_moveto(max(0, 1 - (last - first)))

    def _bind_mousewheel(_event) -> None:
        scroll_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        scroll_canvas.bind_all("<Button-4>", _on_mousewheel)
        scroll_canvas.bind_all("<Button-5>", _on_mousewheel)

    def _unbind_mousewheel(_event) -> None:
        scroll_canvas.unbind_all("<MouseWheel>")
        scroll_canvas.unbind_all("<Button-4>")
        scroll_canvas.unbind_all("<Button-5>")

    scroll_canvas.bind("<Enter>", _bind_mousewheel)
    scroll_canvas.bind("<Leave>", _unbind_mousewheel)
    tab1.bind("<Destroy>", lambda _event: _unbind_mousewheel(None))

    input_frame = ttk.Frame(content_frame)
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
    save_frame = ttk.Frame(content_frame)
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
    curves_frame = ttk.Frame(content_frame)
    curves_frame.place(
        x=ui_const.PADDING,
        y=ui_const.CURVES_FRAME_Y,
        width=ui_const.CURVES_FRAME_WIDTH,
        height=ui_const.CURVES_FRAME_HEIGHT,
    )
    axis_frame = ttk.LabelFrame(content_frame, text="Настройки осей")
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
    annotation_snap_var = tk.StringVar(value="нет")
    annotation_marker_shape_var = tk.StringVar(value="Круг")
    annotation_marker_size_var = tk.StringVar(value="40")
    annotation_color_var = tk.StringVar(value="Красный")

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

    ttk.Label(annotation_frame, text="Привязка:").grid(
        row=0, column=3, padx=5, pady=2, sticky="w"
    )
    annotation_snap_combo = ttk.Combobox(
        annotation_frame,
        values=["нет"],
        state="readonly",
        textvariable=annotation_snap_var,
        width=12,
    )
    annotation_snap_combo.grid(row=0, column=4, padx=5, pady=2, sticky="w")

    marker_shape_options = {
        "Круг": "o",
        "Квадрат": "s",
        "Ромб": "D",
        "Крестик": "x",
    }
    marker_color_options = {
        "Красный": "red",
        "Синий": "blue",
        "Зеленый": "green",
        "Оранжевый": "orange",
        "Фиолетовый": "purple",
        "Черный": "black",
    }

    ttk.Label(annotation_frame, text="Форма:").grid(
        row=2, column=0, padx=5, pady=2, sticky="w"
    )
    annotation_shape_combo = ttk.Combobox(
        annotation_frame,
        values=list(marker_shape_options.keys()),
        state="readonly",
        textvariable=annotation_marker_shape_var,
        width=12,
    )
    annotation_shape_combo.grid(row=2, column=1, padx=5, pady=2, sticky="w")
    ttk.Label(annotation_frame, text="Размер:").grid(
        row=2, column=2, padx=5, pady=2, sticky="w"
    )
    annotation_size_spinbox = ttk.Spinbox(
        annotation_frame,
        from_=5,
        to=200,
        increment=5,
        textvariable=annotation_marker_size_var,
        width=6,
    )
    annotation_size_spinbox.grid(row=2, column=3, padx=5, pady=2, sticky="w")
    ttk.Label(annotation_frame, text="Цвет:").grid(
        row=2, column=4, padx=5, pady=2, sticky="w"
    )
    annotation_color_combo = ttk.Combobox(
        annotation_frame,
        values=list(marker_color_options.keys()),
        state="readonly",
        textvariable=annotation_color_var,
        width=12,
    )
    annotation_color_combo.grid(row=2, column=5, padx=5, pady=2, sticky="w")

    ttk.Label(annotation_frame, text="Текст:").grid(
        row=1, column=0, padx=5, pady=2, sticky="w"
    )
    annotation_text_entry = create_text(
        annotation_frame, method="entry", height=1, state="disabled", scrollbar=False
    )
    annotation_text_entry.grid(
        row=1, column=1, columnspan=3, padx=5, pady=2, sticky="ew"
    )
    undo_annotation_button = ttk.Button(annotation_frame, text="←", width=3)
    undo_annotation_button.grid(row=1, column=4, padx=2, pady=2, sticky="e")
    redo_annotation_button = ttk.Button(annotation_frame, text="→", width=3)
    redo_annotation_button.grid(row=1, column=5, padx=2, pady=2, sticky="w")
    clear_annotations_button = ttk.Button(
        annotation_frame, text="Очистить отметки"
    )
    clear_annotations_button.grid(row=1, column=6, padx=5, pady=2, sticky="e")

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
    _trigger_scroll_check()

    def _on_curve_count_change(_event=None) -> None:
        update_curves(
            curves_frame,
            combo_curves.get(),
            axis_frame,
            save_frame,
            checkbox_var,
            saved_data_curves,
        )
        _trigger_scroll_check()

    combo_curves.bind("<<ComboboxSelected>>", _on_curve_count_change)

    # Фрейм для предпросмотра графика
    preview_frame = ttk.Frame(content_frame)
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

    info_button = ttk.Button(content_frame, text="Как использовать", command=show_usage)
    info_button.place(x=ui_const.PREVIEW_X, y=0)
    fig, ax, canvas = create_plot_canvas(preview_frame)

    annotations: List[Tuple] = []
    undone_annotations: List[Tuple] = []

    def _redraw_canvas() -> None:
        if hasattr(canvas, "draw_idle"):
            canvas.draw_idle()
        else:
            canvas.draw()

    def _remove_annotation_artists(items: List[Tuple]) -> None:
        for point, label in items:
            try:
                point.remove()
            except ValueError:
                pass
            try:
                label.remove()
            except ValueError:
                pass

    def _update_annotation_buttons_state() -> None:
        has_annotations = bool(annotations)
        has_undone = bool(undone_annotations)
        undo_annotation_button.config(
            state="normal" if has_annotations else "disabled"
        )
        redo_annotation_button.config(
            state="normal" if has_undone else "disabled"
        )
        clear_annotations_button.config(
            state="normal" if has_annotations or has_undone else "disabled"
        )

    def clear_annotations() -> None:
        if annotations:
            _remove_annotation_artists(annotations)
            annotations.clear()
        if undone_annotations:
            _remove_annotation_artists(undone_annotations)
            undone_annotations.clear()
        _update_annotation_buttons_state()
        _redraw_canvas()

    def undo_last_annotation() -> None:
        if not annotations:
            return
        point, label = annotations.pop()
        point.set_visible(False)
        label.set_visible(False)
        undone_annotations.append((point, label))
        _update_annotation_buttons_state()
        _redraw_canvas()

    def redo_last_annotation() -> None:
        if not undone_annotations:
            return
        point, label = undone_annotations.pop()
        point.set_visible(True)
        label.set_visible(True)
        annotations.append((point, label))
        _update_annotation_buttons_state()
        _redraw_canvas()

    def _get_marker_properties() -> Tuple[str, float, str]:
        marker = marker_shape_options.get(
            annotation_marker_shape_var.get(), "o"
        )
        try:
            size_value = float(annotation_marker_size_var.get())
        except (tk.TclError, ValueError):
            size_value = 40.0
        size_value = max(size_value, 1.0)
        color = marker_color_options.get(annotation_color_var.get(), "red")
        return marker, size_value, color

    def _format_annotation_text(x_value: float, y_value: float) -> str:
        mode = annotation_type_var.get()
        if mode == "X":
            return f"{x_value:.3g}"
        if mode == "Y":
            return f"{y_value:.3g}"
        if mode == "(X,Y)":
            return f"({x_value:.3g}, {y_value:.3g})"
        return annotation_text_entry.get().strip()

    def _get_selected_line_index() -> int | None:
        value = annotation_snap_var.get().strip().lower()
        if value == "нет":
            return None
        original = annotation_snap_var.get().strip()
        try:
            index = int(original.split()[-1]) - 1
        except (ValueError, IndexError):
            return None
        return index

    def _find_nearest_point(line, x_value: float, y_value: float) -> Tuple[float, float] | None:
        try:
            x_data = line.get_xdata()
            y_data = line.get_ydata()
        except AttributeError:
            return None

        if len(x_data) != len(y_data):
            return None

        axes = getattr(line, "axes", None)
        if axes is None:
            return None

        transform = getattr(axes, "transData", None)
        if transform is None:
            return None

        try:
            click_x, click_y = transform.transform((x_value, y_value))
        except (TypeError, ValueError):
            return None
        if not (math.isfinite(click_x) and math.isfinite(click_y)):
            return None

        use_scaled_distance = False
        x_scale = y_scale = None
        try:
            x_min, x_max = axes.get_xlim()
            y_min, y_max = axes.get_ylim()
            bbox = axes.get_window_extent()
        except (TypeError, ValueError):
            bbox = None
        else:
            if bbox is not None:
                width = bbox.width
                height = bbox.height
                if width > 0 and height > 0:
                    x_range = x_max - x_min
                    y_range = y_max - y_min
                    if (
                        math.isfinite(x_range)
                        and x_range != 0
                        and math.isfinite(y_range)
                        and y_range != 0
                    ):
                        x_scale = abs(width / x_range)
                        y_scale = abs(height / y_range)
                        if math.isfinite(x_scale) and math.isfinite(y_scale):
                            use_scaled_distance = True

        nearest_point: Tuple[float, float] | None = None
        min_distance: float | None = None

        for x_item, y_item in zip(x_data, y_data):
            try:
                x_val = float(x_item)
                y_val = float(y_item)
            except (TypeError, ValueError):
                continue

            if not (math.isfinite(x_val) and math.isfinite(y_val)):
                continue

            if use_scaled_distance:
                dx = (x_val - x_value) * x_scale
                dy = (y_val - y_value) * y_scale
            else:
                try:
                    point_x, point_y = transform.transform((x_val, y_val))
                except (TypeError, ValueError):
                    continue
                if not (math.isfinite(point_x) and math.isfinite(point_y)):
                    continue
                dx = point_x - click_x
                dy = point_y - click_y

            distance = dx * dx + dy * dy

            if min_distance is None or distance < min_distance:
                min_distance = distance
                nearest_point = (x_val, y_val)

        return nearest_point

    def _apply_annotation_snap(x_value: float, y_value: float) -> Tuple[float, float]:
        index = _get_selected_line_index()
        if index is None:
            return x_value, y_value

        lines = list(ax.lines)
        if not (0 <= index < len(lines)):
            return x_value, y_value

        snapped = _find_nearest_point(lines[index], x_value, y_value)
        if snapped is None:
            return x_value, y_value
        return snapped

    def _update_annotation_snap_options() -> None:
        lines = list(ax.lines)
        options = ["нет"] + [f"кривая {i}" for i in range(1, len(lines) + 1)]
        annotation_snap_combo["values"] = options
        if annotation_snap_var.get() not in options:
            annotation_snap_var.set("нет")

    def on_canvas_click(event) -> None:
        if not annotation_mode_var.get():
            return
        if event.inaxes != ax or event.xdata is None or event.ydata is None:
            return
        if hasattr(event, "button") and event.button != 1:
            return
        x_value, y_value = _apply_annotation_snap(event.xdata, event.ydata)
        text = _format_annotation_text(x_value, y_value)
        if annotation_type_var.get() == "Свой текст" and not text:
            messagebox.showwarning(
                "Предупреждение", "Введите текст подписи для отметки."
            )
            return
        if undone_annotations:
            _remove_annotation_artists(undone_annotations)
            undone_annotations.clear()
        marker, marker_size, marker_color = _get_marker_properties()
        point = ax.scatter(
            [x_value],
            [y_value],
            color=marker_color,
            s=marker_size,
            marker=marker,
            zorder=5,
        )
        label = ax.annotate(
            text,
            (x_value, y_value),
            textcoords="offset points",
            xytext=(5, 5),
            color=marker_color,
            fontsize=LABEL_SIZE,
            fontstyle="normal",
            fontweight="normal",
        )
        annotations.append((point, label))
        _update_annotation_buttons_state()
        _redraw_canvas()

    canvas.mpl_connect("button_press_event", on_canvas_click)
    _update_annotation_snap_options()
    undo_annotation_button.config(command=undo_last_annotation)
    redo_annotation_button.config(command=redo_last_annotation)
    clear_annotations_button.config(command=clear_annotations)
    _update_annotation_buttons_state()

    editor_visible = {"shown": False}
    plot_editor = PlotEditor(content_frame, ax, canvas, saved_data_curves)
    plot_editor.place(
        x=ui_const.EDITOR_X,
        y=ui_const.EDITOR_Y,
        width=ui_const.PREVIEW_WIDTH,
        height=plot_editor.required_height,
    )
    plot_editor.place_forget()

    def _refresh_editor_state() -> None:
        plot_editor.refresh()
        _update_annotation_snap_options()

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
            _refresh_editor_state()
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
            _refresh_editor_state()
            messagebox.showerror("Ошибка", f"Не удалось построить график:\n{exc}")
        except Exception as exc:
            logger.exception("Ошибка при построении графика")
            _refresh_editor_state()
            messagebox.showerror(
                "Ошибка",
                f"Не удалось построить график:\n{exc}\nПроверьте введённые данные и попробуйте снова.",
            )
        finally:
            _trigger_scroll_check()

    # Кнопка построения графика
    btn_generate_graph = ttk.Button(content_frame, text="Построить график", command=build_graph)
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
        _trigger_scroll_check()

    checkbox = ttk.Checkbutton(
        input_frame,
        text="Легенда",
        variable=checkbox_var,
        command=on_legend_checkbox_toggle,
    )
    checkbox.place(x=ui_const.CHECKBOX_X, y=ui_const.CURVE_LABEL_Y)
    toggle_legend_title_visibility()

    scroll_canvas.after_idle(_refresh_scrollregion)
