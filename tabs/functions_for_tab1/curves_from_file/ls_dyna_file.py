import logging
from tkinter import messagebox

logger = logging.getLogger(__name__)


def read_X_Y_from_ls_dyna(curve_info):
    """Читает значения X и Y из файла LS-Dyna.

    Строки, не содержащие хотя бы двух числовых значений (заголовки,
    комментарии и т.п.), пропускаются без генерации сообщения об ошибке.
    """
    try:
        path = curve_info['curve_file']
        X_data: list[float] = []
        Y_data: list[float] = []
        with open(path, 'r', encoding='utf-8') as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue
                if line.startswith('*') or line.startswith('#'):
                    continue
                if '#' in line:
                    line = line.split('#', 1)[0].strip()
                parts = line.split()
                numbers = []
                for part in parts:
                    try:
                        numbers.append(float(part))
                    except ValueError:
                        continue
                if len(numbers) < 2:
                    continue
                X_data.append(numbers[0])
                Y_data.append(numbers[1])
        curve_info['X_values'] = X_data
        curve_info['Y_values'] = Y_data
    except FileNotFoundError:
        logger.error("Файл '%s' не найден.", curve_info['curve_file'])
        messagebox.showerror("Ошибка", f"Не удалось открыть файл {path}")
    except Exception:
        logger.error("Ошибка при чтении файла '%s'.", curve_info['curve_file'])
        messagebox.showerror("Ошибка", f"Не удалось открыть файл {path}")
