import json
import math
from copy import deepcopy

from logging_utils import get_logger
import tkinter as tk  # Alias for Tk functionality
from tkinter import ttk, messagebox, colorchooser, filedialog
from typing import Dict, List, Optional, Tuple
from matplotlib import colors as mcolors
from .functions_for_tab1 import (
    update_curves,
    generate_graph,
    save_file,
    apply_axis_limits,
)
from .functions_for_tab1.plotting import last_graph
from widgets import PlotEditor, create_text
from color_palettes import PALETTES
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
    layout_state = {
        "editor_y": ui_const.EDITOR_Y,
        "update_editor": lambda: None,
    }

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
        layout_state["update_editor"]()
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

    default_palette = next(iter(PALETTES), "")
    default_color = "#ff0000"
    if default_palette:
        palette_colors = PALETTES.get(default_palette, [])
        if palette_colors:
            default_color = palette_colors[0]
    annotation_color_var = tk.StringVar(value=default_color)

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
        width=18,
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
        width=14,
    )
    annotation_snap_combo.grid(row=0, column=4, padx=5, pady=2, sticky="w")

    marker_shape_options = {
        "Круг": "o",
        "Квадрат": "s",
        "Ромб": "D",
        "Крестик": "x",
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
    color_panel = ttk.Frame(annotation_frame)
    color_panel.grid(row=2, column=4, columnspan=3, padx=5, pady=2, sticky="w")
    ttk.Label(color_panel, text="Цвет:").grid(row=0, column=0, padx=(0, 6), pady=0, sticky="w")

    annotation_color_preview = tk.Label(
        color_panel,
        bg=annotation_color_var.get(),
        width=6,
        relief="groove",
        borderwidth=1,
        cursor="hand2",
    )
    annotation_color_preview.grid(row=0, column=1, padx=(0, 6), pady=0, sticky="w")

    palette_label = ttk.Label(color_panel, text="Палитра:")
    annotation_palette_var = tk.StringVar(value=default_palette)
    annotation_palette_combo = ttk.Combobox(
        color_panel,
        values=list(PALETTES.keys()),
        state="readonly",
        textvariable=annotation_palette_var,
        width=14,
    )

    palette_colors_frame = ttk.Frame(color_panel)

    def _set_annotation_color(color: str) -> None:
        annotation_color_var.set(color)
        annotation_color_preview.config(bg=color)

    def _choose_custom_annotation_color(_event=None) -> None:
        initial = annotation_color_var.get()
        color_code = colorchooser.askcolor(color=initial)[1]
        if color_code:
            _set_annotation_color(color_code)

    def _refresh_palette_colors(_event=None) -> None:
        for child in palette_colors_frame.winfo_children():
            child.destroy()
        palette_name = annotation_palette_var.get()
        colors = PALETTES.get(palette_name, [])
        for color in colors:
            swatch = tk.Label(
                palette_colors_frame,
                bg=color,
                width=2,
                relief="groove",
                borderwidth=1,
                cursor="hand2",
            )
            swatch.pack(side=tk.LEFT, padx=(0, 4))
            swatch.bind("<Button-1>", lambda _e, c=color: _set_annotation_color(c))

    annotation_color_preview.bind("<Button-1>", _choose_custom_annotation_color)

    if PALETTES:
        palette_label.grid(row=1, column=0, padx=(0, 6), pady=(6, 0), sticky="w")
        annotation_palette_combo.grid(
            row=1, column=1, padx=(0, 6), pady=(6, 0), sticky="w"
        )
        palette_colors_frame.grid(
            row=2, column=0, columnspan=2, pady=(6, 0), sticky="w"
        )
        annotation_palette_combo.bind("<<ComboboxSelected>>", _refresh_palette_colors)
        _refresh_palette_colors()

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

    def _create_annotation_artist(
        x_value: float,
        y_value: float,
        text: str,
        marker: str,
        marker_size: float,
        marker_color: str,
    ) -> Tuple:
        point = ax.scatter(
            [x_value],
            [y_value],
            color=marker_color,
            s=marker_size,
            marker=marker,
            zorder=5,
        )
        setattr(point, "_marker_style", marker)
        setattr(point, "_marker_size", marker_size)
        setattr(point, "_marker_color", marker_color)
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
        return point, label

    def _serialize_annotations() -> List[dict]:
        serialized: List[dict] = []
        for point, label in annotations:
            try:
                offsets = point.get_offsets()
            except AttributeError:
                continue
            if offsets is None or len(offsets) == 0:
                continue
            x_value, y_value = offsets[0]
            try:
                x_float = float(x_value)
                y_float = float(y_value)
            except (TypeError, ValueError):
                continue
            marker = getattr(point, "_marker_style", "o")
            size_attr = getattr(point, "_marker_size", None)
            if size_attr is None:
                sizes = point.get_sizes()
                if sizes is not None and len(sizes) > 0:
                    marker_size = float(sizes[0])
                else:
                    marker_size = 40.0
            else:
                marker_size = float(size_attr)
            color_value = getattr(point, "_marker_color", "") or label.get_color()
            if not color_value:
                facecolors = getattr(point, "get_facecolors", lambda: [])()
                edgecolors = getattr(point, "get_edgecolors", lambda: [])()
                color_source = None
                if facecolors is not None and len(facecolors) > 0:
                    color_source = facecolors[0]
                elif edgecolors is not None and len(edgecolors) > 0:
                    color_source = edgecolors[0]
                if color_source is not None and len(color_source) >= 3:
                    try:
                        color_value = mcolors.to_hex(color_source, keep_alpha=len(color_source) == 4)
                    except ValueError:
                        color_value = label.get_color()
                else:
                    color_value = label.get_color()
            serialized.append(
                {
                    "x": x_float,
                    "y": y_float,
                    "text": label.get_text(),
                    "marker": marker,
                    "size": marker_size,
                    "color": color_value,
                }
            )
        return serialized

    def _restore_annotations(serialized: List[dict]) -> None:
        clear_annotations()
        undone_annotations.clear()
        for item in serialized:
            try:
                x_value = float(item.get("x"))
                y_value = float(item.get("y"))
            except (TypeError, ValueError):
                continue
            text = item.get("text", "")
            marker = item.get("marker", "o") or "o"
            try:
                marker_size = float(item.get("size", 40.0))
            except (TypeError, ValueError):
                marker_size = 40.0
            color_value = item.get("color") or "#ff0000"
            _create_annotation_artist(
                x_value,
                y_value,
                text,
                marker,
                marker_size,
                color_value,
            )

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
        color_value = annotation_color_var.get().strip()
        color = color_value if color_value else "#ff0000"
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
        _create_annotation_artist(
            x_value,
            y_value,
            text,
            marker,
            marker_size,
            marker_color,
        )

    canvas.mpl_connect("button_press_event", on_canvas_click)
    _update_annotation_snap_options()
    undo_annotation_button.config(command=undo_last_annotation)
    redo_annotation_button.config(command=redo_last_annotation)
    clear_annotations_button.config(command=clear_annotations)
    _update_annotation_buttons_state()

    editor_visible = {"shown": False}
    plot_editor = PlotEditor(content_frame, ax, canvas, saved_data_curves)

    def _recalculate_editor_position() -> None:
        axis_frame.update_idletasks()
        annotation_frame.update_idletasks()
        axis_height = max(
            axis_frame.winfo_height(),
            axis_frame.winfo_reqheight(),
            ui_const.AXIS_FRAME_HEIGHT,
        )
        axis_frame.place_configure(height=axis_height)
        annotation_bottom = (
            axis_frame.winfo_y()
            + annotation_frame.winfo_y()
            + annotation_frame.winfo_height()
        )
        target_y = annotation_bottom + ui_const.PADDING
        layout_state["editor_y"] = target_y
        if editor_visible["shown"]:
            plot_editor.place_configure(
                x=ui_const.EDITOR_X,
                y=target_y,
                width=ui_const.PREVIEW_WIDTH,
            )

    layout_state["update_editor"] = _recalculate_editor_position
    _recalculate_editor_position()

    plot_editor.place(
        x=ui_const.EDITOR_X,
        y=layout_state["editor_y"],
        width=ui_const.PREVIEW_WIDTH,
        height=plot_editor.required_height,
    )
    plot_editor.place_forget()

    def _refresh_editor_state() -> None:
        plot_editor.refresh()
        _update_annotation_snap_options()
        layout_state["update_editor"]()

    def reset_auto_entries() -> None:
        for entry in axis_auto_entries.values():
            state = entry.cget("state")
            entry.config(state="normal")
            entry.delete(0, tk.END)
            entry.insert(0, "-")
            entry.config(state=state)

    def _perform_plot(reset_entries: bool, reset_ranges: bool) -> Tuple[bool, Optional[str]]:
        logger.info("Построение графика")
        clear_annotations()
        if reset_entries:
            reset_manual_entries()
            reset_auto_entries()
            reset_saved_ranges()
        if hasattr(ax, "set_xlim") and hasattr(ax, "set_ylim"):
            ax.set_xlim(auto=True)
            ax.set_ylim(auto=True)
        if hasattr(ax, "set_autoscale_on"):
            ax.set_autoscale_on(True)
        plot_editor.reset_axes_lock()
        success = True
        error_message: Optional[str] = None
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
            if reset_ranges:
                plot_editor.reset_ranges()
            layout_state["update_editor"]()
            editor_height = plot_editor.required_height
            if not editor_visible["shown"]:
                plot_editor.place(
                    x=ui_const.EDITOR_X,
                    y=layout_state["editor_y"],
                    width=ui_const.PREVIEW_WIDTH,
                    height=editor_height,
                )
                editor_visible["shown"] = True
            elif editor_height:
                plot_editor.place_configure(
                    x=ui_const.EDITOR_X,
                    y=layout_state["editor_y"],
                    width=ui_const.PREVIEW_WIDTH,
                    height=editor_height,
                )
            logger.info("График построен успешно")
        except ValueError as exc:
            logger.error("Ошибка построения графика", exc_info=True)
            _refresh_editor_state()
            messagebox.showerror("Ошибка", f"Не удалось построить график:\n{exc}")
            success = False
            error_message = str(exc)
        except Exception as exc:
            logger.exception("Ошибка при построении графика")
            _refresh_editor_state()
            messagebox.showerror(
                "Ошибка",
                f"Не удалось построить график:\n{exc}\nПроверьте введённые данные и попробуйте снова.",
            )
            success = False
            error_message = str(exc)
        finally:
            _trigger_scroll_check()
        return success, error_message

    def build_graph() -> None:
        _perform_plot(reset_entries=True, reset_ranges=True)

    def _collect_project_state() -> dict:
        language = combo_language.get() or "Русский"

        def _entry_text(entry: Optional[tk.Entry]) -> str:
            if entry is None or not hasattr(entry, "get"):
                return ""
            return entry.get()

        axis_manual_state: Dict[str, Dict[str, object]] = {}
        for key, entry in axis_manual_entries.items():
            if entry is None:
                continue
            axis_manual_state[key] = {
                "value": entry.get(),
                "user_modified": bool(getattr(entry, "user_modified", False)),
            }

        axis_auto_state: Dict[str, str] = {}
        for key, entry in axis_auto_entries.items():
            if entry is None:
                continue
            axis_auto_state[key] = entry.get()

        legend_enabled = bool(checkbox_var.get())
        legend_value = legend_title_var.get()
        legend_custom_visible = bool(
            legend_title_entry.winfo_ismapped()
            if hasattr(legend_title_entry, "winfo_ismapped")
            else False
        )
        legend_key: Optional[str] = None
        if legend_custom_visible:
            legend_key = "Другое"
        elif legend_value:
            for key, translations in LEGEND_TITLE_TRANSLATIONS.items():
                if translations.get(language, key) == legend_value:
                    legend_key = key
                    break

        line_styles: List[Dict[str, object]] = []
        for line in getattr(ax, "lines", []):
            colour = line.get_color()
            colour_hex = None
            try:
                colour_hex = mcolors.to_hex(colour)
            except ValueError:
                try:
                    colour_hex = mcolors.to_hex(mcolors.to_rgba(colour))
                except ValueError:
                    colour_hex = str(colour)
            line_styles.append(
                {
                    "color": colour_hex,
                    "style": line.get_linestyle(),
                    "width": float(line.get_linewidth()),
                }
            )

        axes_limits: Optional[Dict[str, List[float]]] = None
        if hasattr(ax, "has_data") and ax.has_data():
            try:
                x_lim = list(map(float, ax.get_xlim()))
                y_lim = list(map(float, ax.get_ylim()))
            except (TypeError, ValueError):
                axes_limits = None
            else:
                axes_limits = {"x": x_lim, "y": y_lim}

        fixed_limits: Optional[Dict[str, List[float]]] = None
        if getattr(plot_editor, "_fixed_limits", None):
            try:
                x_fix, y_fix = plot_editor._fixed_limits
                fixed_limits = {
                    "x": [float(x_fix[0]), float(x_fix[1])],
                    "y": [float(y_fix[0]), float(y_fix[1])],
                }
            except (TypeError, ValueError, IndexError):
                fixed_limits = None

        state = {
            "language": language,
            "title": {
                "selection": combo_title.get(),
                "custom": entry_title_custom.get(),
                "custom_visible": bool(
                    entry_title_custom.winfo_ismapped()
                    if hasattr(entry_title_custom, "winfo_ismapped")
                    else False
                ),
            },
            "axes": {
                "x": {
                    "selection": combo_titleX.get(),
                    "custom": _entry_text(path_entry_titleX),
                    "unit_selection": combo_titleX_size.get(),
                    "unit_custom": _entry_text(combo_titleX_size_entry),
                },
                "y": {
                    "selection": combo_titleY.get(),
                    "custom": _entry_text(path_entry_titleY),
                    "unit_selection": combo_titleY_size.get(),
                    "unit_custom": _entry_text(combo_titleY_size_entry),
                },
                "auto": axis_auto_state,
                "manual": axis_manual_state,
            },
            "legend": {
                "enabled": legend_enabled,
                "selected_key": legend_key,
                "display_value": legend_value,
                "custom_text": legend_title_entry.get(),
                "custom_visible": legend_custom_visible,
            },
            "curves": deepcopy(saved_data_curves),
            "num_curves": combo_curves.get(),
            "annotations": _serialize_annotations(),
            "annotation_settings": {
                "mode": bool(annotation_mode_var.get()),
                "type": annotation_type_var.get(),
                "snap": annotation_snap_var.get(),
                "marker_shape": annotation_marker_shape_var.get(),
                "marker_size": annotation_marker_size_var.get(),
                "color": annotation_color_var.get(),
                "palette": annotation_palette_var.get(),
                "text": annotation_text_entry.get(),
            },
            "plot": {
                "palette": plot_editor.palette_combo.get(),
                "line_styles": line_styles,
                "fix_axes": bool(plot_editor.fix_axes_var.get()),
                "fixed_limits": fixed_limits,
                "axes_limits": axes_limits,
                "editor_visible": bool(editor_visible["shown"]),
                "has_graph": bool(getattr(ax, "lines", [])),
            },
            "save": {
                "name": entry_save.get(),
                "format": combo_format.get(),
            },
        }
        return state

    def _apply_project_state(state: dict) -> Tuple[bool, Optional[str]]:
        try:
            language = state.get("language") or "Русский"
            combo_language.set(language)
            on_language_change()

            title_state = state.get("title", {})
            combo_title.set(title_state.get("selection", combo_title.get()))
            on_title_combo_change(combo_title, entry_title_custom, title_var)
            entry_title_custom.delete(0, tk.END)
            entry_title_custom.insert(0, title_state.get("custom", ""))

            axes_state = state.get("axes", {})
            x_state = axes_state.get("x", {})
            combo_titleX.set(x_state.get("selection", combo_titleX.get()))
            on_combo_changeX_Y_labels(
                combo_titleX,
                path_entry_titleX,
                label_titleX_size,
                combo_titleX_size,
                combo_titleX_size_entry,
            )
            path_entry_titleX.delete(0, tk.END)
            path_entry_titleX.insert(0, x_state.get("custom", ""))
            unit_selection_x = x_state.get("unit_selection", "")
            combo_titleX_size.set(unit_selection_x)
            on_unit_change(combo_titleX_size, combo_titleX_size_entry)
            combo_titleX_size_entry.delete(0, tk.END)
            combo_titleX_size_entry.insert(0, x_state.get("unit_custom", ""))

            y_state = axes_state.get("y", {})
            combo_titleY.set(y_state.get("selection", combo_titleY.get()))
            on_combo_changeX_Y_labels(
                combo_titleY,
                path_entry_titleY,
                label_titleY_size,
                combo_titleY_size,
                combo_titleY_size_entry,
            )
            path_entry_titleY.delete(0, tk.END)
            path_entry_titleY.insert(0, y_state.get("custom", ""))
            unit_selection_y = y_state.get("unit_selection", "")
            combo_titleY_size.set(unit_selection_y)
            on_unit_change(combo_titleY_size, combo_titleY_size_entry)
            combo_titleY_size_entry.delete(0, tk.END)
            combo_titleY_size_entry.insert(0, y_state.get("unit_custom", ""))

            auto_state = axes_state.get("auto", {})
            for key, entry in axis_auto_entries.items():
                if entry is None:
                    continue
                state_attr = entry.cget("state") if hasattr(entry, "cget") else None
                if state_attr is not None:
                    entry.config(state="normal")
                entry.delete(0, tk.END)
                value = auto_state.get(key, "")
                if value is not None:
                    entry.insert(0, str(value))
                if state_attr is not None:
                    entry.config(state=state_attr)

            manual_state = axes_state.get("manual", {})
            for key, entry in axis_manual_entries.items():
                if entry is None:
                    continue
                info = manual_state.get(key, {})
                entry.delete(0, tk.END)
                value = info.get("value", "")
                if value is not None:
                    entry.insert(0, str(value))
                entry.user_modified = bool(info.get("user_modified", False))

            legend_state = state.get("legend", {})
            checkbox_var.set(bool(legend_state.get("enabled", False)))
            toggle_legend_title_visibility()
            legend_custom_text = legend_state.get("custom_text", "")
            legend_key = legend_state.get("selected_key")
            legend_display = legend_state.get("display_value", "")
            custom_visible = bool(legend_state.get("custom_visible", False))
            language_now = combo_language.get() or "Русский"
            other_label = LEGEND_TITLE_TRANSLATIONS["Другое"].get(language_now, "Другое")
            if checkbox_var.get():
                if custom_visible:
                    legend_title_combo.set(other_label)
                    legend_title_var.set(other_label)
                    on_legend_title_change(
                        legend_title_combo,
                        legend_title_entry,
                        legend_title_var,
                        language_now,
                    )
                    legend_title_entry.delete(0, tk.END)
                    legend_title_entry.insert(0, legend_custom_text)
                else:
                    if legend_key and legend_key in LEGEND_TITLE_TRANSLATIONS:
                        translated = LEGEND_TITLE_TRANSLATIONS[legend_key].get(
                            language_now, legend_key
                        )
                    else:
                        translated = legend_display
                    if translated:
                        legend_title_combo.set(translated)
                        legend_title_var.set(translated)
                    legend_title_entry.place_forget()
                    legend_title_entry.delete(0, tk.END)
                    legend_title_entry.insert(0, legend_custom_text)
            else:
                legend_title_entry.place_forget()
                legend_title_entry.delete(0, tk.END)
                legend_title_entry.insert(0, legend_custom_text)
                legend_title_var.set("")

            curves_data = state.get("curves", [])
            saved_data_curves.clear()
            if isinstance(curves_data, list) and curves_data:
                for item in curves_data:
                    saved_data_curves.append(deepcopy(item) if isinstance(item, dict) else {})
            else:
                saved_data_curves.append({})

            saved_count = state.get("num_curves")
            if isinstance(saved_count, str):
                try:
                    count_int = int(saved_count)
                except ValueError:
                    count_int = len(saved_data_curves) or 1
            elif isinstance(saved_count, int):
                count_int = saved_count
            else:
                count_int = len(saved_data_curves) or 1
            count_int = max(1, min(count_int, len(curve_options)))
            curve_value = str(count_int)
            combo_curves.set(curve_value)
            combo_curves.current(count_int - 1)
            update_curves(
                curves_frame,
                curve_value,
                axis_frame,
                save_frame,
                checkbox_var,
                saved_data_curves,
            )

            save_state = state.get("save", {})
            entry_save.delete(0, tk.END)
            entry_save.insert(0, str(save_state.get("name", "")))
            format_value = str(save_state.get("format", ""))
            if format_value:
                combo_format.set(format_value)

            annotation_state = state.get("annotation_settings", {})
            annotation_mode_var.set(bool(annotation_state.get("mode", False)))
            annotation_type_var.set(annotation_state.get("type", annotation_type_var.get()))
            annotation_marker_shape_var.set(
                annotation_state.get("marker_shape", annotation_marker_shape_var.get())
            )
            annotation_marker_size_var.set(
                str(annotation_state.get("marker_size", annotation_marker_size_var.get()))
            )
            color_value = annotation_state.get("color", annotation_color_var.get())
            annotation_color_var.set(color_value)
            annotation_color_preview.config(bg=color_value)
            palette_value = annotation_state.get("palette")
            if palette_value and palette_value in PALETTES:
                annotation_palette_var.set(palette_value)
            elif annotation_palette_var.get() not in PALETTES:
                annotation_palette_var.set(next(iter(PALETTES), ""))
            _refresh_palette_colors()
            if annotation_type_var.get() == "Свой текст":
                annotation_text_entry.config(state="normal")
                annotation_text_entry.delete(0, tk.END)
                annotation_text_entry.insert(
                    0, annotation_state.get("text", annotation_text_entry.get())
                )
            else:
                annotation_text_entry.delete(0, tk.END)
                annotation_text_entry.config(state="disabled")

            plot_state = state.get("plot", {})
            palette_selection = plot_state.get("palette")
            if palette_selection and palette_selection in plot_editor.palette_combo["values"]:
                plot_editor.palette_combo.set(palette_selection)

            success, error_message = _perform_plot(
                reset_entries=False, reset_ranges=False
            )

            if not success:
                return success, error_message

            # Повторно применяем значения осей после построения
            for key, entry in axis_auto_entries.items():
                if entry is None:
                    continue
                state_attr = entry.cget("state") if hasattr(entry, "cget") else None
                if state_attr is not None:
                    entry.config(state="normal")
                entry.delete(0, tk.END)
                value = auto_state.get(key, "")
                if value is not None:
                    entry.insert(0, str(value))
                if state_attr is not None:
                    entry.config(state=state_attr)

            for key, entry in axis_manual_entries.items():
                if entry is None:
                    continue
                info = manual_state.get(key, {})
                entry.delete(0, tk.END)
                value = info.get("value", "")
                if value is not None:
                    entry.insert(0, str(value))
                entry.user_modified = bool(info.get("user_modified", False))
            apply_axis_limits(ax, canvas, axis_manual_entries)

            line_styles = plot_state.get("line_styles", [])
            for line, style_info in zip(getattr(ax, "lines", []), line_styles):
                color = style_info.get("color")
                if color:
                    try:
                        line.set_color(color)
                    except ValueError:
                        try:
                            line.set_color(mcolors.to_rgba(color))
                        except ValueError:
                            pass
                linestyle = style_info.get("style")
                if linestyle:
                    line.set_linestyle(linestyle)
                width = style_info.get("width")
                if width is not None:
                    try:
                        line.set_linewidth(float(width))
                    except (TypeError, ValueError):
                        pass

            for row, style_info in zip(getattr(plot_editor, "_rows", []), line_styles):
                color = style_info.get("color")
                if color:
                    row.colour.config(bg=color)
                linestyle = style_info.get("style")
                if linestyle:
                    row.style.set(linestyle)
                width = style_info.get("width")
                if width is not None:
                    try:
                        row.width.set(float(width))
                    except (TypeError, ValueError):
                        pass

            axes_limits = plot_state.get("axes_limits") or {}
            x_limits = axes_limits.get("x")
            y_limits = axes_limits.get("y")
            try:
                if x_limits:
                    ax.set_xlim(float(x_limits[0]), float(x_limits[1]))
                if y_limits:
                    ax.set_ylim(float(y_limits[0]), float(y_limits[1]))
            except (TypeError, ValueError, IndexError):
                pass

            fixed_limits = plot_state.get("fixed_limits")
            if fixed_limits and "x" in fixed_limits and "y" in fixed_limits:
                try:
                    plot_editor._fixed_limits = (
                        tuple(map(float, fixed_limits["x"])),
                        tuple(map(float, fixed_limits["y"])),
                    )
                except (TypeError, ValueError):
                    plot_editor._fixed_limits = None
            else:
                plot_editor._fixed_limits = None
            plot_editor.fix_axes_var.set(bool(plot_state.get("fix_axes", False)))
            plot_editor._apply_axes_fix_state()

            _update_annotation_snap_options()
            saved_snap = annotation_state.get("snap", annotation_snap_var.get())
            snap_options = annotation_snap_combo["values"]
            if saved_snap in snap_options:
                annotation_snap_var.set(saved_snap)
            elif snap_options:
                annotation_snap_var.set(snap_options[0])

            _restore_annotations(state.get("annotations", []))
            update_annotation_entry_state()

            editor_should_show = plot_state.get("editor_visible", True)
            if not editor_should_show:
                plot_editor.place_forget()
                editor_visible["shown"] = False
            else:
                editor_visible["shown"] = True

            _redraw_canvas()
            plot_editor._refresh_legend()
            plot_editor._redraw_canvas()
            _trigger_scroll_check()
            return True, None
        except Exception as exc:  # noqa: BLE001
            logger.exception("Ошибка восстановления проекта")
            raise ValueError(f"Некорректный файл проекта: {exc}") from exc

    def save_project() -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("All files", "*.*")],
        )
        if not path:
            return
        data = _collect_project_state()
        try:
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(data, fh, ensure_ascii=False, indent=2)
            messagebox.showinfo("Успех", f"Проект сохранён: {path}")
        except Exception as exc:  # noqa: BLE001
            logger.exception("Ошибка сохранения проекта")
            messagebox.showerror(
                "Ошибка сохранения",
                f"{exc}\nНе удалось сохранить проект.",
            )

    def load_project() -> None:
        path = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Ошибка чтения проекта")
            messagebox.showerror(
                "Ошибка загрузки",
                f"{exc}\nНе удалось прочитать файл проекта.",
            )
            return
        try:
            success, error_message = _apply_project_state(data)
        except ValueError as exc:
            messagebox.showerror("Ошибка загрузки", str(exc))
            return
        if success:
            messagebox.showinfo("Успех", f"Проект загружен: {path}")
        else:
            details = (
                f"\n{error_message}"
                if error_message
                else ""
            )
            messagebox.showwarning(
                "Загрузка завершена",
                "Данные формы восстановлены, но построить график не удалось." + details,
            )

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

    project_buttons = ttk.Frame(save_frame)
    project_buttons.place(
        x=ui_const.PADDING,
        y=ui_const.LINE_HEIGHT * 2 + 10,
    )
    ttk.Button(
        project_buttons,
        text="Сохранить проект",
        command=save_project,
    ).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(
        project_buttons,
        text="Загрузить проект",
        command=load_project,
    ).pack(side=tk.LEFT)

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
