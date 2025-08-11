import logging

logger = logging.getLogger(__name__)


def read_X_Y_from_ls_dyna(curve_info):
    try:
        path = curve_info['curve_file']
        X_data = []
        Y_data = []
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 2:
                    continue
                try:
                    x = float(parts[0])
                    y = float(parts[1])
                except ValueError:
                    continue
                X_data.append(x)
                Y_data.append(y)
        curve_info['X_values'] = X_data
        curve_info['Y_values'] = Y_data
    except FileNotFoundError:
        logger.error("Файл '%s' не найден.", curve_info['curve_file'])
        from tkinter import messagebox
        messagebox.showerror("Ошибка", f"Не удалось открыть файл {path}")
    except Exception:
        logger.error("Ошибка при чтении файла '%s'.", curve_info['curve_file'])
        from tkinter import messagebox
        messagebox.showerror("Ошибка", f"Не удалось открыть файл {path}")
