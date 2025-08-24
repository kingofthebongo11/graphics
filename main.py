import tkinter as tk
from tkinter import ttk

import logging

from tabs.tab4 import create_tab4
from tabs.tab3 import create_tab3
from tabs.tab2 import create_tab2
from tabs.tab1 import create_tab1

from settings import configure_matplotlib


def on_closing(root):
    root.quit()  # Останавливаем цикл Tkinter
    root.destroy()  # Уничтожаем окно


def main():
    configure_matplotlib()
    # Создание главного окна
    root = tk.Tk()
    root.geometry("1500x1100")
    root.title("Работа с графиками")
    root.resizable(True, True)

    # Создание вкладок
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill=tk.BOTH)

    # Добавляем вкладки
    create_tab1(notebook)
    create_tab2(notebook)
    create_tab3(notebook)
    create_tab4(notebook)

    # Привязка обработчика закрытия окна
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    # Запуск окна
    root.mainloop()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
