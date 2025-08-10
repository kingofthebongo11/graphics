# Файл содержит обработчики событий для элементов управления.
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
                               combo_curve_typeY_type):
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
    else:
        label_curve_typeX.place_forget()
        combo_curve_typeX.place_forget()
        label_curve_typeY.place_forget()
        combo_curve_typeY.place_forget()
        label_curve_typeX_type.place_forget()
        combo_curve_typeX_type.place_forget()
        label_curve_typeY_type.place_forget()
        combo_curve_typeY_type.place_forget()


def on_combo_change_curve_type_excel(frame, combo, checkbox_horizontal, checkbox_range,
                                     label_X_range, entry_X_range, label_Y_range, entry_Y_range):
    if combo.get() == "Excel файл":
        if not checkbox_horizontal.winfo_viewable():
            frame.update_idletasks()
            checkbox_horizontal.place(x=combo.winfo_x() + 170, y=combo.winfo_y())
            checkbox_range.place(x=combo.winfo_x() + 170, y=combo.winfo_y() + 25)
            on_range_checkbox_toggle(checkbox_range, label_X_range, entry_X_range, label_Y_range, entry_Y_range)
    else:
        checkbox_horizontal.place_forget()
        checkbox_range.place_forget()
        label_X_range.place_forget()
        entry_X_range.place_forget()
        label_Y_range.place_forget()
        entry_Y_range.place_forget()
        checkbox_range.var.set(False)


def on_range_checkbox_toggle(checkbox_range, label_X_range, entry_X_range, label_Y_range, entry_Y_range):
    if checkbox_range.var.get():
        x = checkbox_range.winfo_x()
        y = checkbox_range.winfo_y() + 25
        label_X_range.place(x=x, y=y)
        entry_X_range.place(x=x + 80, y=y, width=100)
        label_Y_range.place(x=x + 200, y=y)
        entry_Y_range.place(x=x + 280, y=y, width=100)
    else:
        label_X_range.place_forget()
        entry_X_range.place_forget()
        label_Y_range.place_forget()
        entry_Y_range.place_forget()
