import tkinter as tk
from tkinter import ttk
from typing import Any, Dict

from widgets import create_text, select_path

from .events import on_combobox_event, on_combo_change_curve_type
from ui import constants as ui_const
from analysis_types import ANALYSIS_TYPES


def _build_source_section(axis: str, input_frame: tk.Widget, i: int, saved_data: list[dict]) -> Dict[str, Any]:
    """Создает элементы выбора источника данных для оси.

    Parameters
    ----------
    axis:
        Ось, для которой создаются элементы ("X" или "Y").
    input_frame:
        Родительский фрейм.
    i:
        Номер кривой.
    saved_data:
        Список сохраненных параметров.

    Returns
    -------
    dict
        Словарь с созданными виджетами.
    """
    label_source = ttk.Label(
        input_frame,
        text="Выберите тип для X:" if axis == "X" else "Выберите тип для данных Y:",
    )
    combo_source = ttk.Combobox(
        input_frame,
        values=["Частотный анализ", "Текстовой файл", "Файл кривой LS-Dyna", "Excel файл"],
        state="readonly",
    )
    combo_source._name = f"curve_{i}_{axis}_source"
    saved_source = saved_data[i - 1].get(f"{axis}_source", {}).get("source")
    if saved_source:
        combo_source.set(saved_source)

    label_param = ttk.Label(input_frame, text="Параметр:")
    combo_param = ttk.Combobox(
        input_frame,
        values=[
            "Время",
            "Номер доминантной частота",
            "Частота",
            "Масса",
            "Процент от общей массы",
            "Процент общей массы",
        ],
        state="readonly",
    )
    combo_param._name = f"curve_{i}_{axis}_parameter"
    combo_param.bind(
        "<<ComboboxSelected>>",
        lambda e: saved_data[i - 1].setdefault(f"{axis}_source", {}).update({"parameter": combo_param.get()}),
    )
    if saved_source == "Частотный анализ":
        saved_param = saved_data[i - 1].get(f"{axis}_source", {}).get("parameter")
        if saved_param:
            combo_param.set(saved_param)

    label_axis = ttk.Label(input_frame, text="По какой оси:")
    combo_axis = ttk.Combobox(
        input_frame,
        values=["X", "Y", "Z", "XR", "YR", "ZR"],
        state="readonly",
    )
    combo_axis._name = f"curve_{i}_{axis}_direction"
    combo_axis.bind(
        "<<ComboboxSelected>>",
        lambda e: saved_data[i - 1].setdefault(f"{axis}_source", {}).update({"direction": combo_axis.get()}),
    )
    if saved_source == "Частотный анализ":
        saved_dir = saved_data[i - 1].get(f"{axis}_source", {}).get("direction")
        if saved_dir:
            combo_axis.set(saved_dir)

    label_column = ttk.Label(input_frame, text="Столбец:")
    combo_column = ttk.Combobox(
        input_frame,
        values=["X", "Y"],
        state="readonly",
    )
    combo_column._name = f"curve_{i}_{axis}_column"
    saved_column = saved_data[i - 1].get(f"{axis}_source", {}).get("column")
    if saved_column in (0, 1):
        combo_column.set("X" if saved_column == 0 else "Y")
    combo_column.bind(
        "<<ComboboxSelected>>",
        lambda e: saved_data[i - 1]
        .setdefault(f"{axis}_source", {})
        .update({"column": 0 if combo_column.get() == "X" else 1}),
    )

    label_range_c = ttk.Label(input_frame, text="Диапазон:")
    entry_range_c = ttk.Entry(input_frame, width=ui_const.ENTRY_CHAR_WIDTH)
    entry_range_c.insert(
        0, saved_data[i - 1].get(f"{axis}_source", {}).get(f"range_{axis.lower()}", "")
    )
    entry_range_c._name = f"curve_{i}_{axis}_range"
    entry_range_c.bind(
        "<KeyRelease>",
        lambda e: saved_data[i - 1]
        .setdefault(f"{axis}_source", {})
        .update(
            {
                "use_ranges": True,
                f"range_{axis.lower()}": entry_range_c.get(),
                "column": 0 if axis == "X" else 1,
            }
        ),
    )

    return {
        "label_source": label_source,
        "combo_source": combo_source,
        "label_param": label_param,
        "combo_param": combo_param,
        "label_axis": label_axis,
        "combo_axis": combo_axis,
        "label_column": label_column,
        "combo_column": combo_column,
        "label_range_c": label_range_c,
        "entry_range_c": entry_range_c,
    }


def _create_excel_options(
    input_frame: tk.Widget,
    i: int,
    dy: int,
    saved_data: list[dict],
    combo_curve_type: ttk.Combobox,
) -> Dict[str, Any]:
    """Создает элементы управления, специфичные для Excel-файлов."""

    horizontal_var = tk.BooleanVar(value=saved_data[i - 1].get("horizontal", False))
    checkbox_horizontal = ttk.Checkbutton(
        input_frame,
        text="По-горизонтали",
        variable=horizontal_var,
        command=lambda: saved_data[i - 1].update({"horizontal": horizontal_var.get()}),
    )
    checkbox_horizontal._name = f"curve_{i}_horizontal"
    checkbox_horizontal.var = horizontal_var

    offset_var = tk.BooleanVar(value=saved_data[i - 1].get("use_offset", False))
    checkbox_offset = ttk.Checkbutton(
        input_frame,
        text="Смещение",
        variable=offset_var,
        command=lambda: (
            saved_data[i - 1].update({"use_offset": offset_var.get()}),
            toggle_excel_options(),
        ),
    )
    checkbox_offset._name = f"curve_{i}_use_offset"
    checkbox_offset.var = offset_var

    label_offset_h = ttk.Label(input_frame, text="Гор:")
    entry_offset_h = ttk.Entry(input_frame, width=ui_const.OFFSET_CHAR_WIDTH)
    entry_offset_h.insert(0, str(saved_data[i - 1].get("offset_horizontal", 0)))
    entry_offset_h._name = f"curve_{i}_offset_h"
    entry_offset_h.bind(
        "<KeyRelease>",
        lambda e: saved_data[i - 1].update(
            {
                "offset_horizontal": int(entry_offset_h.get() or 0)
                if entry_offset_h.get().isdigit()
                else 0
            }
        ),
    )

    label_offset_v = ttk.Label(input_frame, text="Верт:")
    entry_offset_v = ttk.Entry(input_frame, width=ui_const.OFFSET_CHAR_WIDTH)
    entry_offset_v.insert(0, str(saved_data[i - 1].get("offset_vertical", 0)))
    entry_offset_v._name = f"curve_{i}_offset_v"
    entry_offset_v.bind(
        "<KeyRelease>",
        lambda e: saved_data[i - 1].update(
            {
                "offset_vertical": int(entry_offset_v.get() or 0)
                if entry_offset_v.get().isdigit()
                else 0
            }
        ),
    )

    ranges_var = tk.BooleanVar(value=saved_data[i - 1].get("use_ranges", False))
    checkbox_ranges = ttk.Checkbutton(
        input_frame,
        text="Диапазоны",
        variable=ranges_var,
        command=lambda: (
            saved_data[i - 1].update({"use_ranges": ranges_var.get()}),
            toggle_excel_options(),
        ),
    )
    checkbox_ranges._name = f"curve_{i}_use_ranges"
    checkbox_ranges.var = ranges_var

    label_range_x = ttk.Label(input_frame, text="X:")
    entry_range_x = ttk.Entry(input_frame, width=ui_const.ENTRY_CHAR_WIDTH)
    entry_range_x.insert(0, saved_data[i - 1].get("range_x", ""))
    entry_range_x._name = f"curve_{i}_range_x"
    entry_range_x.bind(
        "<KeyRelease>",
        lambda e: saved_data[i - 1].update({"range_x": entry_range_x.get()}),
    )

    label_range_y = ttk.Label(input_frame, text="Y:")
    entry_range_y = ttk.Entry(input_frame, width=ui_const.ENTRY_CHAR_WIDTH)
    entry_range_y.insert(0, saved_data[i - 1].get("range_y", ""))
    entry_range_y._name = f"curve_{i}_range_y"
    entry_range_y.bind(
        "<KeyRelease>",
        lambda e: saved_data[i - 1].update({"range_y": entry_range_y.get()}),
    )

    def toggle_excel_options() -> None:
        if combo_curve_type.get() == "Excel файл":
            checkbox_horizontal.place(
                x=ui_const.PADDING,
                y=ui_const.CONTROL_Y + dy * (i - 1),
            )
            checkbox_offset.place(
                x=ui_const.OFFSET_CHECKBOX_X,
                y=ui_const.CONTROL_Y + dy * (i - 1),
            )
            checkbox_ranges.place(
                x=ui_const.RANGES_CHECKBOX_X,
                y=ui_const.CONTROL_Y + dy * (i - 1),
            )
            if ranges_var.get():
                checkbox_horizontal.var.set(False)
                checkbox_offset.var.set(False)
                saved_data[i - 1].update({"horizontal": False, "use_offset": False})
                checkbox_horizontal.config(state="disabled")
                checkbox_offset.config(state="disabled")
                label_offset_h.place_forget()
                entry_offset_h.place_forget()
                label_offset_v.place_forget()
                entry_offset_v.place_forget()
                label_range_x.place(
                    x=ui_const.RANGE_LABEL_X,
                    y=ui_const.CONTROL_Y + dy * (i - 1),
                )
                entry_range_x.place(
                    x=ui_const.RANGE_ENTRY_X,
                    y=ui_const.CONTROL_Y + dy * (i - 1),
                    width=ui_const.RANGE_ENTRY_WIDTH,
                )
                label_range_y.place(
                    x=ui_const.RANGE_Y_LABEL_X,
                    y=ui_const.CONTROL_Y + dy * (i - 1),
                )
                entry_range_y.place(
                    x=ui_const.RANGE_Y_ENTRY_X,
                    y=ui_const.CONTROL_Y + dy * (i - 1),
                    width=ui_const.RANGE_ENTRY_WIDTH,
                )
            else:
                checkbox_horizontal.config(state="normal")
                checkbox_offset.config(state="normal")
                label_range_x.place_forget()
                entry_range_x.place_forget()
                label_range_y.place_forget()
                entry_range_y.place_forget()
                if offset_var.get():
                    label_offset_h.place(
                        x=ui_const.OFFSET_H_LABEL_X,
                        y=ui_const.CONTROL_Y + dy * (i - 1),
                    )
                    entry_offset_h.place(
                        x=ui_const.OFFSET_H_ENTRY_X,
                        y=ui_const.CONTROL_Y + dy * (i - 1),
                        width=ui_const.OFFSET_ENTRY_WIDTH,
                    )
                    label_offset_v.place(
                        x=ui_const.OFFSET_V_LABEL_X,
                        y=ui_const.CONTROL_Y + dy * (i - 1),
                    )
                    entry_offset_v.place(
                        x=ui_const.OFFSET_V_ENTRY_X,
                        y=ui_const.CONTROL_Y + dy * (i - 1),
                        width=ui_const.OFFSET_ENTRY_WIDTH,
                    )
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

    return {
        "checkbox_horizontal": checkbox_horizontal,
        "checkbox_offset": checkbox_offset,
        "checkbox_ranges": checkbox_ranges,
        "label_offset_h": label_offset_h,
        "entry_offset_h": entry_offset_h,
        "label_offset_v": label_offset_v,
        "entry_offset_v": entry_offset_v,
        "label_range_x": label_range_x,
        "entry_range_x": entry_range_x,
        "label_range_y": label_range_y,
        "entry_range_y": entry_range_y,
        "toggle": toggle_excel_options,
        "ranges_var": ranges_var,
        "offset_var": offset_var,
    }


def _create_path_widgets(
    input_frame: tk.Widget, i: int, dy: int, saved_data: list[dict]
) -> Dict[str, Any]:
    """Создает элементы для выбора путей к файлам."""

    label_path = ttk.Label(input_frame, text="Выберите файл с кривой:")
    label_path.place(
        x=ui_const.PADDING,
        y=ui_const.PATH_LABEL_Y + dy * (i - 1),
    )

    path_entry = create_text(
        input_frame, method="entry", height=1, state="normal", scrollbar=False
    )
    path_entry.place(
        x=ui_const.PADDING,
        y=ui_const.PATH_ENTRY_Y + dy * (i - 1),
        width=ui_const.PATH_ENTRY_WIDTH,
    )
    path_entry._name = f"curve_{i}_filename"
    path_entry.insert(0, saved_data[i - 1].get("path", ""))

    select_button = ttk.Button(
        input_frame,
        text="Выбор файла",
        command=lambda: select_path(path_entry, path_type="file", saved_data=saved_data[i - 1]),
    )
    select_button.place(
        x=ui_const.SELECT_BUTTON_X,
        y=ui_const.SELECT_BUTTON_Y + dy * (i - 1),
    )

    label_path_X = ttk.Label(input_frame, text="Файл для X:")
    label_path_X.place(
        x=ui_const.PADDING,
        y=ui_const.PATH_LABEL_Y + dy * (i - 1),
    )
    path_entry_X = create_text(
        input_frame, method="entry", height=1, state="normal", scrollbar=False
    )
    path_entry_X.place(
        x=ui_const.PADDING,
        y=ui_const.PATH_ENTRY_Y + dy * (i - 1),
        width=ui_const.PATH_ENTRY_WIDTH,
    )
    path_entry_X._name = f"curve_{i}_filename_X"
    path_entry_X.insert(0, saved_data[i - 1].get("X_source", {}).get("curve_file", ""))
    path_entry_X.bind(
        "<KeyRelease>",
        lambda e: saved_data[i - 1]
        .setdefault("X_source", {})
        .update({"curve_file": path_entry_X.get()}),
    )
    select_button_X = ttk.Button(
        input_frame,
        text="Выбор файла",
        command=lambda: (
            select_path(path_entry_X, path_type="file"),
            saved_data[i - 1]
            .setdefault("X_source", {})
            .update({"curve_file": path_entry_X.get()}),
        ),
    )
    select_button_X.place(
        x=ui_const.SELECT_BUTTON_X,
        y=ui_const.SELECT_BUTTON_Y + dy * (i - 1),
    )

    label_path_Y = ttk.Label(input_frame, text="Файл для Y:")
    label_path_Y.place(
        x=ui_const.PADDING,
        y=ui_const.PATH_LABEL_Y_2 + dy * (i - 1),
    )
    path_entry_Y = create_text(
        input_frame, method="entry", height=1, state="normal", scrollbar=False
    )
    path_entry_Y.place(
        x=ui_const.PADDING,
        y=ui_const.PATH_ENTRY_Y_2 + dy * (i - 1),
        width=ui_const.PATH_ENTRY_WIDTH,
    )
    path_entry_Y._name = f"curve_{i}_filename_Y"
    path_entry_Y.insert(0, saved_data[i - 1].get("Y_source", {}).get("curve_file", ""))
    path_entry_Y.bind(
        "<KeyRelease>",
        lambda e: saved_data[i - 1]
        .setdefault("Y_source", {})
        .update({"curve_file": path_entry_Y.get()}),
    )
    select_button_Y = ttk.Button(
        input_frame,
        text="Выбор файла",
        command=lambda: (
            select_path(path_entry_Y, path_type="file"),
            saved_data[i - 1]
            .setdefault("Y_source", {})
            .update({"curve_file": path_entry_Y.get()}),
        ),
    )
    select_button_Y.place(
        x=ui_const.SELECT_BUTTON_X,
        y=ui_const.SELECT_BUTTON_Y_2 + dy * (i - 1),
    )

    label_path_X.place_forget()
    path_entry_X.place_forget()
    select_button_X.place_forget()
    label_path_Y.place_forget()
    path_entry_Y.place_forget()
    select_button_Y.place_forget()

    return {
        "label_path": label_path,
        "path_entry": path_entry,
        "select_button": select_button,
        "label_path_X": label_path_X,
        "path_entry_X": path_entry_X,
        "select_button_X": select_button_X,
        "label_path_Y": label_path_Y,
        "path_entry_Y": path_entry_Y,
        "select_button_Y": select_button_Y,
    }


def create_curve_box(input_frame, i, checkbox_var, saved_data):
    """Создает ячейку для настройки параметров кривой."""

    dy = (
        ui_const.CURVE_HEIGHT_WITH_LEGEND
        if checkbox_var.get()
        else ui_const.CURVE_HEIGHT
    )

    label_curve_box = ttk.Label(
        input_frame, text=f"Настройка параметров кривой {i}:"
    )
    label_curve_box.place(x=ui_const.PADDING, y=dy * (i - 1))

    label_curve_type = ttk.Label(
        input_frame, text=f"Выберите тип кривой {i}:"
    )
    label_curve_type.place(
        x=ui_const.PADDING,
        y=ui_const.LINE_HEIGHT + dy * (i - 1),
    )

    combo_curve_type = ttk.Combobox(
        input_frame,
        values=[
            "Частотный анализ",
            "Текстовой файл",
            "Файл кривой LS-Dyna",
            "Excel файл",
            "Комбинированный",
        ],
        state="readonly",
    )
    combo_curve_type.place(
        x=ui_const.CURVE_COMBO_X,
        y=ui_const.LINE_HEIGHT + dy * (i - 1),
        width=ui_const.SMALL_COMBO_WIDTH,
    )
    combo_curve_type._name = f"curve_{i}_type"
    saved_type = saved_data[i - 1].get("curve_type")
    if saved_type:
        combo_curve_type.set(saved_type)
    else:
        combo_curve_type.set("Текстовой файл")
        saved_data[i - 1]["curve_type"] = "Текстовой файл"

    label_curve_typeX = ttk.Label(input_frame, text="Выберите параметр для Х:")
    combo_curve_typeX = ttk.Combobox(
        input_frame,
        values=[
            "Время",
            "Номер доминантной частота",
            "Частота",
            "Масса",
            "Процент от общей массы",
            "Процент общей массы",
        ],
        state="readonly",
    )
    combo_curve_typeX._name = f"curve_{i}_typeXF"

    label_curve_typeY = ttk.Label(input_frame, text="Выберите параметр для Y:")
    combo_curve_typeY = ttk.Combobox(
        input_frame,
        values=[
            "Время",
            "Номер доминантной частота",
            "Частота",
            "Масса",
            "Процет от общей массы",
            "Процент общей массы",
        ],
        state="readonly",
    )
    combo_curve_typeY._name = f"curve_{i}_typeYF"

    label_curve_typeX_type = ttk.Label(input_frame, text="По какой оси:")
    combo_curve_typeX_type = ttk.Combobox(
        input_frame, values=["X", "Y", "Z", "XR", "YR", "ZR"], state="readonly"
    )
    combo_curve_typeX_type._name = f"curve_{i}_typeXFtype"

    label_curve_typeY_type = ttk.Label(input_frame, text="По какой оси:")
    combo_curve_typeY_type = ttk.Combobox(
        input_frame, values=["X", "Y", "Z", "XR", "YR", "ZR"], state="readonly"
    )
    combo_curve_typeY_type._name = f"curve_{i}_typeYFtype"

    label_analysis_type = ttk.Label(input_frame, text="Тип анализа:")
    combo_analysis_type = ttk.Combobox(
        input_frame, values=ANALYSIS_TYPES, state="readonly"
    )
    combo_analysis_type._name = f"curve_{i}_analysis_type"
    saved_at = saved_data[i - 1].get("analysis_type")
    if saved_at:
        combo_analysis_type.set(saved_at)
    combo_analysis_type.bind(
        "<<ComboboxSelected>>",
        lambda e: saved_data[i - 1].update({"analysis_type": combo_analysis_type.get()}),
    )

    x_source = _build_source_section("X", input_frame, i, saved_data)
    y_source = _build_source_section("Y", input_frame, i, saved_data)

    excel_widgets = _create_excel_options(input_frame, i, dy, saved_data, combo_curve_type)
    toggle_excel_options = excel_widgets["toggle"]

    paths = _create_path_widgets(input_frame, i, dy, saved_data)

    def toggle_source(options: Dict[str, Any]) -> None:
        if not options["combo_source"].winfo_viewable():
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
                x_source["label_source"],
                x_source["combo_source"],
                y_source["label_source"],
                y_source["combo_source"],
                paths["label_path"],
                paths["path_entry"],
                paths["select_button"],
                paths["label_path_X"],
                paths["path_entry_X"],
                paths["select_button_X"],
                paths["label_path_Y"],
                paths["path_entry_Y"],
                paths["select_button_Y"],
                label_analysis_type,
                combo_analysis_type,
            )
        for w in [
            options["label_param"],
            options["combo_param"],
            options["label_axis"],
            options["combo_axis"],
            options["label_column"],
            options["combo_column"],
            options["label_range_c"],
            options["entry_range_c"],
        ]:
            w.place_forget()
        if combo_curve_type.get() != "Комбинированный":
            return
        source = options["combo_source"].get()
        if source == "Частотный анализ":
            input_frame.update_idletasks()
            options["label_param"].place(
                x=options["combo_source"].winfo_x(),
                y=options["combo_source"].winfo_y() + ui_const.SOURCE_LABEL_OFFSET,
            )
            options["combo_param"].place(
                x=options["combo_source"].winfo_x(),
                y=options["combo_source"].winfo_y() + ui_const.SOURCE_COMBO_OFFSET,
                width=ui_const.SMALL_COMBO_WIDTH,
            )
            options["label_axis"].place(
                x=options["combo_source"].winfo_x(),
                y=options["combo_source"].winfo_y() + ui_const.SOURCE_AXIS_LABEL_OFFSET,
            )
            options["combo_axis"].place(
                x=options["combo_source"].winfo_x(),
                y=options["combo_source"].winfo_y() + ui_const.SOURCE_AXIS_COMBO_OFFSET,
                width=ui_const.SMALL_COMBO_WIDTH,
            )
        elif source in ("Текстовой файл", "Файл кривой LS-Dyna"):
            input_frame.update_idletasks()
            options["label_column"].place(
                x=options["combo_source"].winfo_x(),
                y=options["combo_source"].winfo_y() + ui_const.SOURCE_LABEL_OFFSET,
            )
            options["combo_column"].place(
                x=options["combo_source"].winfo_x(),
                y=options["combo_source"].winfo_y() + ui_const.SOURCE_COMBO_OFFSET,
                width=ui_const.SMALL_COMBO_WIDTH,
            )
            saved_data[i - 1].setdefault(
                f"{'X' if options is x_source else 'Y'}_source", {}
            ).setdefault("column", 0 if options is x_source else 1)
        elif source == "Excel файл":
            input_frame.update_idletasks()
            options["label_range_c"].place(
                x=options["combo_source"].winfo_x(),
                y=options["combo_source"].winfo_y() + ui_const.SOURCE_LABEL_OFFSET,
            )
            options["entry_range_c"].place(
                x=options["combo_source"].winfo_x(),
                y=options["combo_source"].winfo_y() + ui_const.SOURCE_COMBO_OFFSET,
                width=ui_const.SMALL_COMBO_WIDTH,
            )
            saved_data[i - 1].setdefault(
                f"{'X' if options is x_source else 'Y'}_source", {}
            ).update({"column": 0 if options is x_source else 1})

    def toggle_X_source_options() -> None:
        toggle_source(x_source)

    def toggle_Y_source_options() -> None:
        toggle_source(y_source)

    x_source["combo_source"].bind(
        "<<ComboboxSelected>>",
        lambda e: on_combobox_event(
            e,
            lambda e: saved_data[i - 1]
            .setdefault("X_source", {})
            .update({"source": x_source["combo_source"].get()}),
            lambda e: toggle_X_source_options(),
        ),
    )
    y_source["combo_source"].bind(
        "<<ComboboxSelected>>",
        lambda e: on_combobox_event(
            e,
            lambda e: saved_data[i - 1]
            .setdefault("Y_source", {})
            .update({"source": y_source["combo_source"].get()}),
            lambda e: toggle_Y_source_options(),
        ),
    )

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
                x_source["label_source"],
                x_source["combo_source"],
                y_source["label_source"],
                y_source["combo_source"],
                paths["label_path"],
                paths["path_entry"],
                paths["select_button"],
                paths["label_path_X"],
                paths["path_entry_X"],
                paths["select_button_X"],
                paths["label_path_Y"],
                paths["path_entry_Y"],
                paths["select_button_Y"],
                label_analysis_type,
                combo_analysis_type,
            ),
            lambda e: saved_data[i - 1].update({"curve_type": combo_curve_type.get()}),
            lambda e: toggle_excel_options(),
            lambda e: (toggle_X_source_options(), toggle_Y_source_options()),
        ),
    )

    if checkbox_var.get():
        label_legend = ttk.Label(input_frame, text="Подпись легенды:")
        label_legend.place(
            x=ui_const.PADDING,
            y=ui_const.LEGEND_LABEL_Y + dy * (i - 1),
        )
        legend_entry = create_text(
            input_frame, method="entry", height=1, state="normal", scrollbar=False
        )
        legend_entry.place(
            x=ui_const.PADDING,
            y=ui_const.LEGEND_ENTRY_Y + dy * (i - 1),
            width=ui_const.ENTRY_WIDTH,
        )
        legend_entry._name = f"curve_{i}_legend"
        legend_entry.insert(0, saved_data[i - 1].get("legend", ""))
        legend_entry.bind(
            "<KeyRelease>",
            lambda e: saved_data[i - 1].update({"legend": legend_entry.get()}),
        )

    toggle_excel_options()
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
        x_source["label_source"],
        x_source["combo_source"],
        y_source["label_source"],
        y_source["combo_source"],
        paths["label_path"],
        paths["path_entry"],
        paths["select_button"],
        paths["label_path_X"],
        paths["path_entry_X"],
        paths["select_button_X"],
        paths["label_path_Y"],
        paths["path_entry_Y"],
        paths["select_button_Y"],
        label_analysis_type,
        combo_analysis_type,
    )
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
    frame_height = (
        ui_const.CURVE_HEIGHT_WITH_LEGEND * num_curves_int
        if checkbox_var.get()
        else ui_const.CURVE_HEIGHT * num_curves_int
    )
    frame.place_configure(height=frame_height)

    # Восстанавливаем данные, если они есть
    for i in range(len(saved_data), num_curves_int):
        saved_data.append({'curve_type': "", 'path': "", 'legend': "", 'curve_typeX': "", 'curve_typeY': "",
                           'curve_typeX_type': "", 'curve_typeY_type': "", 'analysis_type': "", 'horizontal': False,
                           'use_offset': False, 'offset_horizontal': 0, 'offset_vertical': 0,
                           'use_ranges': False, 'range_x': '', 'range_y': '',
                           'X_source': {}, 'Y_source': {}})

    for i in range(1, num_curves_int + 1):
        create_curve_box(frame, i, checkbox_var, saved_data)

    next_frame.place(
        x=ui_const.PADDING,
        y=frame.winfo_y() + frame_height + ui_const.PADDING,
    )  # Обновляем координаты следующего фрейма
