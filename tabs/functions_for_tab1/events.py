from tkinter import ttk


def on_combobox_event(event, *callbacks):
    """Вызывает все переданные функции-обработчики последовательно."""
    for callback in callbacks:
        if callable(callback):
            try:
                callback(event)
            except TypeError:
                callback()


def on_combo_change_curve_type(frame, combo, label_curve_typeX, combo_curve_typeX, label_curve_typeY, combo_curve_typeY,
                               label_curve_typeX_type, combo_curve_typeX_type, label_curve_typeY_type,
                               combo_curve_typeY_type, path_entry, horizontal_check,
                               label_X_range, entry_X_range, label_Y_range, entry_Y_range):
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
        horizontal_check.place_forget()
        label_X_range.place_forget()
        entry_X_range.place_forget()
        label_Y_range.place_forget()
        entry_Y_range.place_forget()
    elif combo.get() == "Excel файл":
        label_curve_typeX.place_forget()
        combo_curve_typeX.place_forget()
        label_curve_typeY.place_forget()
        combo_curve_typeY.place_forget()
        label_curve_typeX_type.place_forget()
        combo_curve_typeX_type.place_forget()
        label_curve_typeY_type.place_forget()
        combo_curve_typeY_type.place_forget()

        horizontal_check.var.set(0)
        horizontal_check.place(x=path_entry.winfo_x(), y=path_entry.winfo_y() + 10)
        label_X_range.place_forget()
        entry_X_range.place_forget()
        label_Y_range.place_forget()
        entry_Y_range.place_forget()
    else:
        label_curve_typeX.place_forget()
        combo_curve_typeX.place_forget()
        label_curve_typeY.place_forget()
        combo_curve_typeY.place_forget()
        label_curve_typeX_type.place_forget()
        combo_curve_typeX_type.place_forget()
        label_curve_typeY_type.place_forget()
        combo_curve_typeY_type.place_forget()
        horizontal_check.place_forget()
        label_X_range.place_forget()
        entry_X_range.place_forget()
        label_Y_range.place_forget()
        entry_Y_range.place_forget()
