from tkinter import ttk


def on_combobox_event(event, *callbacks):
    """Вызывает все переданные функции-обработчики последовательно."""
    for callback in callbacks:
        if callable(callback):
            try:
                callback(event)
            except TypeError:
                callback()


def on_combo_change_curve_type(
    frame,
    combo,
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
):
    def _init_geom(widget):
        if not hasattr(widget, "_orig_geom"):
            frame.update_idletasks()
            widget._orig_geom = {
                "x": widget.winfo_x(),
                "y": widget.winfo_y(),
                "w": widget.winfo_width(),
            }
        return widget._orig_geom

    label_path_geom = _init_geom(label_path)
    path_entry_geom = _init_geom(path_entry)
    select_button_geom = _init_geom(select_button)

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
        label_source_X.place_forget()
        combo_source_X.place_forget()
        label_source_Y.place_forget()
        combo_source_Y.place_forget()

        label_path.place(x=label_path_geom["x"], y=label_path_geom["y"])
        path_entry.place(x=path_entry_geom["x"], y=path_entry_geom["y"], width=path_entry_geom["w"])
        select_button.place(x=select_button_geom["x"], y=select_button_geom["y"])
        label_path_X.place_forget()
        path_entry_X.place_forget()
        select_button_X.place_forget()
        label_path_Y.place_forget()
        path_entry_Y.place_forget()
        select_button_Y.place_forget()
    elif combo.get() == "Комбинированный":
        label_curve_typeX.place_forget()
        combo_curve_typeX.place_forget()
        label_curve_typeY.place_forget()
        combo_curve_typeY.place_forget()
        label_curve_typeX_type.place_forget()
        combo_curve_typeX_type.place_forget()
        label_curve_typeY_type.place_forget()
        combo_curve_typeY_type.place_forget()

        label_path.place_forget()
        path_entry.place_forget()
        select_button.place_forget()

        if not label_source_X.winfo_viewable():
            frame.update_idletasks()
            label_source_X.place(x=combo.winfo_x() + 170,
                                 y=combo.winfo_y() - 20)
            combo_source_X.place(x=combo.winfo_x() + 170,
                                 y=combo.winfo_y(), width=150)
            frame.update_idletasks()
            label_source_Y.place(x=combo_source_X.winfo_x() + 170,
                                 y=combo.winfo_y() - 20)
            combo_source_Y.place(x=combo_source_X.winfo_x() + 170,
                                 y=combo.winfo_y(), width=150)

        frame.update_idletasks()

        base_x = path_entry_geom["x"]
        width = (label_source_X.winfo_x() - base_x - select_button_geom["w"] - 20)
        base_y_label = label_path_geom["y"] - 30
        base_y_entry = path_entry_geom["y"] - 30
        base_y_button = select_button_geom["y"] - 30
        button_x = base_x + width + 10

        label_path_X.place(x=base_x, y=base_y_label)
        path_entry_X.place(x=base_x, y=base_y_entry, width=width)
        select_button_X.place(x=button_x, y=base_y_button)
        label_path_Y.place(x=base_x, y=base_y_label + 50)
        path_entry_Y.place(x=base_x, y=base_y_entry + 50, width=width)
        select_button_Y.place(x=button_x, y=base_y_button + 50)
    elif combo.get() == "Файл кривой LS-Dyna":
        label_curve_typeX.place_forget()
        combo_curve_typeX.place_forget()
        label_curve_typeY.place_forget()
        combo_curve_typeY.place_forget()
        label_curve_typeX_type.place_forget()
        combo_curve_typeX_type.place_forget()
        label_curve_typeY_type.place_forget()
        combo_curve_typeY_type.place_forget()
        label_source_X.place_forget()
        combo_source_X.place_forget()
        label_source_Y.place_forget()
        combo_source_Y.place_forget()

        label_path.place(x=label_path_geom["x"], y=label_path_geom["y"])
        path_entry.place(x=path_entry_geom["x"], y=path_entry_geom["y"], width=path_entry_geom["w"])
        select_button.place(x=select_button_geom["x"], y=select_button_geom["y"])
        label_path_X.place_forget()
        path_entry_X.place_forget()
        select_button_X.place_forget()
        label_path_Y.place_forget()
        path_entry_Y.place_forget()
        select_button_Y.place_forget()

    else:
        label_curve_typeX.place_forget()
        combo_curve_typeX.place_forget()
        label_curve_typeY.place_forget()
        combo_curve_typeY.place_forget()
        label_curve_typeX_type.place_forget()
        combo_curve_typeX_type.place_forget()
        label_curve_typeY_type.place_forget()
        combo_curve_typeY_type.place_forget()
        label_source_X.place_forget()
        combo_source_X.place_forget()
        label_source_Y.place_forget()
        combo_source_Y.place_forget()

        label_path.place(x=label_path_geom["x"], y=label_path_geom["y"])
        path_entry.place(x=path_entry_geom["x"], y=path_entry_geom["y"], width=path_entry_geom["w"])
        select_button.place(x=select_button_geom["x"], y=select_button_geom["y"])
        label_path_X.place_forget()
        path_entry_X.place_forget()
        select_button_X.place_forget()
        label_path_Y.place_forget()
        path_entry_Y.place_forget()
        select_button_Y.place_forget()
