from tkinter import ttk


def on_combobox_event(event, *callbacks):
    """Вызывает все переданные функции-обработчики последовательно."""
    for callback in callbacks:
        if callable(callback):
            try:
                callback(event)
            except TypeError:
                callback()


def toggle_range_fields(check_button, label_x, entry_x, label_y, entry_y):
    if check_button.var.get():
        label_x.place(x=check_button.winfo_x(), y=check_button.winfo_y() + 25)
        entry_x.place(x=check_button.winfo_x() + 100, y=check_button.winfo_y() + 25, width=150)
        label_y.place(x=check_button.winfo_x(), y=check_button.winfo_y() + 50)
        entry_y.place(x=check_button.winfo_x() + 100, y=check_button.winfo_y() + 50, width=150)
    else:
        label_x.place_forget()
        entry_x.place_forget()
        label_y.place_forget()
        entry_y.place_forget()


def on_combo_change_curve_type(frame, combo, label_curve_typeX, combo_curve_typeX, label_curve_typeY, combo_curve_typeY,
                               label_curve_typeX_type, combo_curve_typeX_type, label_curve_typeY_type,
                               combo_curve_typeY_type, check_horizontal, check_range,
                               label_x_range, entry_x_range, label_y_range, entry_y_range):
    curve_type = combo.get()
    if curve_type == "Частотный анализ":
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
        check_horizontal.place_forget()
        check_range.place_forget()
        label_x_range.place_forget()
        entry_x_range.place_forget()
        label_y_range.place_forget()
        entry_y_range.place_forget()
    elif curve_type == "Excel/CSV файл":
        label_curve_typeX.place_forget()
        combo_curve_typeX.place_forget()
        label_curve_typeY.place_forget()
        combo_curve_typeY.place_forget()
        label_curve_typeX_type.place_forget()
        combo_curve_typeX_type.place_forget()
        label_curve_typeY_type.place_forget()
        combo_curve_typeY_type.place_forget()

        check_horizontal.place(x=combo.winfo_x() + 170, y=combo.winfo_y())
        check_range.place(x=combo.winfo_x() + 170, y=combo.winfo_y() + 25)
        if not check_range.var.get():
            label_x_range.place_forget()
            entry_x_range.place_forget()
            label_y_range.place_forget()
            entry_y_range.place_forget()
    else:
        label_curve_typeX.place_forget()
        combo_curve_typeX.place_forget()
        label_curve_typeY.place_forget()
        combo_curve_typeY.place_forget()
        label_curve_typeX_type.place_forget()
        combo_curve_typeX_type.place_forget()
        label_curve_typeY_type.place_forget()
        combo_curve_typeY_type.place_forget()
        check_horizontal.place_forget()
        check_range.place_forget()
        label_x_range.place_forget()
        entry_x_range.place_forget()
        label_y_range.place_forget()
        entry_y_range.place_forget()
