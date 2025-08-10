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
                               combo_curve_typeY_type, checkbox_horizontal=None, label_rangeX=None,
                               entry_rangeX=None, label_rangeY=None, entry_rangeY=None):
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
        if checkbox_horizontal:
            checkbox_horizontal.place_forget()
        if label_rangeX:
            label_rangeX.place_forget()
        if entry_rangeX:
            entry_rangeX.place_forget()
        if label_rangeY:
            label_rangeY.place_forget()
        if entry_rangeY:
            entry_rangeY.place_forget()
    elif combo.get() == "Excel файл":
        label_curve_typeX.place_forget()
        combo_curve_typeX.place_forget()
        label_curve_typeY.place_forget()
        combo_curve_typeY.place_forget()
        label_curve_typeX_type.place_forget()
        combo_curve_typeX_type.place_forget()
        label_curve_typeY_type.place_forget()
        combo_curve_typeY_type.place_forget()
        if checkbox_horizontal:
            frame.update_idletasks()
            checkbox_horizontal.place(x=combo.winfo_x() + 170, y=combo.winfo_y())

            def toggle_entries():
                if checkbox_horizontal.instate(['selected']):
                    if label_rangeX and entry_rangeX and label_rangeY and entry_rangeY:
                        label_rangeX.place(x=checkbox_horizontal.winfo_x() + 170,
                                           y=checkbox_horizontal.winfo_y() - 20)
                        entry_rangeX.place(x=checkbox_horizontal.winfo_x() + 170,
                                           y=checkbox_horizontal.winfo_y(), width=150)
                        label_rangeY.place(x=entry_rangeX.winfo_x() + 170,
                                           y=checkbox_horizontal.winfo_y() - 20)
                        entry_rangeY.place(x=entry_rangeX.winfo_x() + 170,
                                           y=checkbox_horizontal.winfo_y(), width=150)
                else:
                    if label_rangeX and entry_rangeX and label_rangeY and entry_rangeY:
                        label_rangeX.place_forget()
                        entry_rangeX.place_forget()
                        label_rangeY.place_forget()
                        entry_rangeY.place_forget()

            checkbox_horizontal.configure(command=toggle_entries)
            toggle_entries()
    else:
        label_curve_typeX.place_forget()
        combo_curve_typeX.place_forget()
        label_curve_typeY.place_forget()
        combo_curve_typeY.place_forget()
        label_curve_typeX_type.place_forget()
        combo_curve_typeX_type.place_forget()
        label_curve_typeY_type.place_forget()
        combo_curve_typeY_type.place_forget()
        if checkbox_horizontal:
            checkbox_horizontal.place_forget()
        if label_rangeX:
            label_rangeX.place_forget()
        if entry_rangeX:
            entry_rangeX.place_forget()
        if label_rangeY:
            label_rangeY.place_forget()
        if entry_rangeY:
            entry_rangeY.place_forget()
