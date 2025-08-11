import tkinter as tk
from tkinter import ttk
from widgets.select_path import select_path
from widgets.text_widget import create_text, clear_text
from .functions_for_tab3.processing import function1


def create_tab3(notebook):
    """Создает вкладку для извлечения частотных параметров из LS-DYNA."""
    # Создание третьей вкладки
    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text="Извлечение частотных параметров из LS-DYNA")

    # Создаем фрейм для размещения текстового поля и кнопки
    input_frame = ttk.Frame(tab3)
    input_frame.place(x=10, y=10, width=1280, height=200)

    # Метка над текстовым полем
    label = ttk.Label(input_frame, text="Выберите папку рабочего проекта:")
    label.place(x=10, y=0)

    # Создаем текстовое поле для ввода пути с отступом слева
    path_entry = create_text(input_frame, method="entry", height=1, state='normal', scrollbar=False)
    path_entry.place(x=10, y=30, width=600)

    select_button = ttk.Button(input_frame, text="Выбор папки", command=lambda: select_path(path_entry))
    select_button.place(x=600, y=28)

    # Фрейм для текстового поля логов и скроллбара
    log_frame = ttk.Frame(tab3)
    log_frame.place(x=10, y=150, width=1280, height=200)

    # Метка над окном логирования
    log_label = ttk.Label(log_frame, text="Окно логирования:")
    log_label.place(x=0, y=0)

    # Создаем текстовое поле для логов с прокруткой
    log_text, log_scrollbar = create_text(log_frame, height=10, state='disabled', scrollbar=True)
    log_text.place(x=0, y=20, width=1260, height=180)
    log_scrollbar.place(x=1260, y=20, width=20, height=180)

    # Кнопка "Получить данные" под текстовым полем
    get_data_button = ttk.Button(
        input_frame,
        text="Получить данные",
        command=lambda: function1(log_text=log_text, path_entry=path_entry),
    )
    get_data_button.place(x=300, y=60)

    # Кнопка для очистки окна логирования
    clear_button = ttk.Button(tab3, text="Очистить окно логирования", command=lambda: clear_text(log_text))
    clear_button.place(x=10, y=360)
