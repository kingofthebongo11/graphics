import logging
import tkinter as tk  # Alias for Tk functionality
from tkinter import ttk
from typing import List, Tuple
from .functions_for_tab1 import update_curves, generate_graph, save_file, last_graph
from widgets import PlotEditor, create_text
from tabs.function_for_all_tabs import create_plot_canvas
from .constants import DEFAULT_UNITS, PHYSICAL_QUANTITIES, UNITS_MAPPING
from ui import constants as ui_const


logger = logging.getLogger(__name__)


def on_title_combo_change(
    combo: ttk.Combobox, entry: tk.Entry, title_var: tk.StringVar
) -> None:
    """Обновляет выбор заголовка графика.

    При выборе "Другое" отображает поле ввода и очищает комбобокс.
    При выборе готового варианта скрывает поле ввода и устанавливает
    выбранный текст в переменную заголовка.
    """

    selection = combo.get()
    if selection == "Другое":
        entry.place(
            x=combo.winfo_x(),
            y=combo.winfo_y(),
            width=combo.winfo_width(),
        )
        combo.set("")
        title_var.set("")
    else:
        entry.place_forget()
        title_var.set(selection)


def on_combo_changeX_Y_labels(
    combo: ttk.Combobox,
    entry: tk.Entry,
    label_size: ttk.Label,
    size_combo: ttk.Combobox,
) -> None:
    """
    Обрабатывает выбор в комбобоксе для осей:
    - Если выбрано "Другое", отображает текстовое поле для ввода и скрывает выбор размерности.
    - Иначе скрывает текстовое поле, показывает метку и комбобокс размерности с нужными единицами.
    """

    selection = combo.get()
    logger.info("Выбор в комбобоксе: %s", selection)
    if selection == "Другое":
        logger.debug("Показ поля ввода для пользовательской величины")
        if not entry.winfo_ismapped():
            entry.place(
                x=combo.winfo_x() + ui_const.LABEL_SIZE_OFFSET,
                y=combo.winfo_y(),
                width=ui_const.ENTRY_WIDTH,
            )
            entry.config(state="normal")
        label_size.place_forget()
        size_combo.place_forget()
        size_combo["values"] = []
        size_combo.set("")
    elif selection == "Нет":
        logger.debug("Скрытие элементов оси")
        entry.place_forget()
        label_size.place_forget()
        size_combo.place_forget()
        size_combo["values"] = []
        size_combo.set("")
    else:
        logger.debug("Выбрана стандартная величина: %s", selection)
        entry.place_forget()
        label_size.place(
            x=combo.winfo_x() + ui_const.LABEL_SIZE_OFFSET,
            y=combo.winfo_y(),
        )
        values = UNITS_MAPPING.get(selection, [])
        size_combo["values"] = values
        size_combo.set("")
        if values:
            size_combo.place(
                x=combo.winfo_x() + ui_const.SIZE_COMBO_OFFSET,
                y=combo.winfo_y(),
                width=ui_const.SIZE_COMBO_WIDTH,
            )
            default_unit = DEFAULT_UNITS.get(selection)
            if default_unit in values:
                size_combo.current(values.index(default_unit))
        else:
            size_combo.place_forget()


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
    ) -> Tuple[ttk.Combobox, tk.Entry, ttk.Label, ttk.Combobox]:
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
            x=combo.winfo_x() + ui_const.LABEL_SIZE_OFFSET,
            y=combo.winfo_y(),
        )
        size_label.place_forget()
        size_combo = ttk.Combobox(parent, values=[], state="readonly")
        size_combo.place(
            x=combo.winfo_x() + ui_const.SIZE_COMBO_OFFSET,
            y=combo.winfo_y(),
            width=ui_const.SIZE_COMBO_WIDTH,
        )
        size_combo.place_forget()
        combo.bind(
            "<<ComboboxSelected>>",
            lambda e: on_combo_changeX_Y_labels(combo, entry, size_label, size_combo),
        )
        return combo, entry, size_label, size_combo

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
        width=ui_const.ENTRY_WIDTH,
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
    combo_title.bind(
        "<<ComboboxSelected>>",
        lambda e: on_title_combo_change(combo_title, entry_title_custom, title_var),
    )

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

    # Поля для осей X и Y, используя список физических величин
    combo_titleX, path_entry_titleX, label_titleX_size, combo_titleX_size = (
        add_axis_control(
            input_frame,
            "Выберите величину для оси X:",
            PHYSICAL_QUANTITIES,
            ui_const.LINE_HEIGHT * 2,
        )
    )
    combo_titleY, path_entry_titleY, label_titleY_size, combo_titleY_size = (
        add_axis_control(
            input_frame,
            "Выберите величину для оси Y:",
            PHYSICAL_QUANTITIES,
            ui_const.LINE_HEIGHT * 3,
        )
    )
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
    update_curves(curves_frame, "1", save_frame, checkbox_var, saved_data_curves)
    combo_curves.bind(
        "<<ComboboxSelected>>",
        lambda e: update_curves(
            curves_frame,
            combo_curves.get(),
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
            "1. Выберите название графика из списка или пункт «Другое» и введите своё.\n"
            "2. Выберите размерности осей при необходимости.\n"
            "3. Выберите количество кривых и загрузите данные для каждой.\n"
            "4. Нажмите «Построить график» для отображения.\n"
            "5. Для сохранения изображения укажите имя файла и формат, затем нажмите «Сохранить»."
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

    editor_visible = {"shown": False}
    plot_editor = PlotEditor(tab1, ax, canvas)
    plot_editor.place(
        x=ui_const.EDITOR_X,
        y=ui_const.EDITOR_Y,
        width=ui_const.PREVIEW_WIDTH,
        height=ui_const.EDITOR_HEIGHT,
    )
    plot_editor.place_forget()

    def build_graph() -> None:
        logger.info("Построение графика")
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
            )
            plot_editor.refresh()
            if not editor_visible["shown"]:
                plot_editor.place(
                    x=ui_const.EDITOR_X,
                    y=ui_const.EDITOR_Y,
                    width=ui_const.PREVIEW_WIDTH,
                    height=ui_const.EDITOR_HEIGHT,
                )
                editor_visible["shown"] = True
            logger.info("График построен успешно")
        except Exception as exc:
            logger.error("Ошибка при построении графика: %s", exc)
            raise

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
    checkbox = ttk.Checkbutton(
        input_frame,
        text="Легенда",
        variable=checkbox_var,
        command=lambda: update_curves(
            curves_frame,
            combo_curves.get(),
            save_frame,
            checkbox_var,
            saved_data_curves,
        ),
    )
    checkbox.place(x=ui_const.CHECKBOX_X, y=ui_const.CURVE_LABEL_Y)
