import tkinter as tk
from tkinter import filedialog

from mylibproject.myutils import is_russian_layout


def make_context_menu(widget):
    # Создаем контекстное меню
    context_menu = tk.Menu(widget, tearoff=0)
    context_menu.add_command(label="Вырезать", command=lambda: widget.event_generate("<<Cut>>"))
    context_menu.add_command(label="Копировать", command=lambda: widget.event_generate("<<Copy>>"))
    context_menu.add_command(label="Вставить", command=lambda: widget.event_generate("<<Paste>>"))
    context_menu.add_command(label="Выделить все", command=lambda: widget.event_generate("<<SelectAll>>"))

    # Функция для отображения контекстного меню
    def show_context_menu(event):
        context_menu.tk_popup(event.x_root, event.y_root)

    # Привязываем отображение контекстного меню к правой кнопке мыши
    widget.bind("<Button-3>", show_context_menu)

def add_hotkeys(text_widget):
    def on_key_press(event, text_widget):
        if is_russian_layout():  # Выполняем бинды только при русской раскладке
            # Проверяем, что зажата клавиша Control
            if event.state & 0x4:  # 0x4 — это битовое представление состояния Control
                # Проверяем, какая именно клавиша была нажата по ее keycode
                if event.keycode == 67:  # Код клавиши 'C' или 'С'
                    text_widget.event_generate("<<Copy>>")
                elif event.keycode == 86:  # Код клавиши 'V' или 'М'
                    text_widget.event_generate("<<Paste>>")
                elif event.keycode == 88:  # Код клавиши 'X' или 'Ч'
                    text_widget.event_generate("<<Cut>>")
                elif event.keycode == 65:  # Код клавиши 'A' или 'Ф'
                    text_widget.event_generate("<<SelectAll>>")
    # Привязка на уровне конкретного текстового поля
    text_widget.bind('<KeyPress>', lambda event: on_key_press(event, text_widget))


def select_path(entry_widget, path_type="folder", saved_data=None):
    # Открываем диалоговое окно для выбора папки или файла
    if path_type == "folder":
        selected_path = filedialog.askdirectory()  # Выбор папки
    elif path_type == "file":
        selected_path = filedialog.askopenfilename()  # Выбор файла
    else:
        raise ValueError("Недопустимый тип пути: используйте 'folder' или 'file'.")

    if selected_path:
        # Вставляем выбранный путь в текстовое поле
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, selected_path)

        # Обновляем сохраненные данные, если передан параметр saved_data
        if saved_data:
            key = 'path'
            saved_data.update({key: entry_widget.get()})


def message_log(log_text, message):
    log_text.config(state='normal')  # Разрешаем редактирование
    log_text.insert(tk.END, message + "\n")  # Вставляем текст в конец
    log_text.config(state='disabled')  # Запрещаем редактирование после вставки
    log_text.yview(tk.END)  # Прокрутка вниз к последнему сообщению
