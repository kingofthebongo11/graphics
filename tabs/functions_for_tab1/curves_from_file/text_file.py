import logging
from pathlib import Path
from tkinter import messagebox

logger = logging.getLogger(__name__)


def read_X_Y_from_text_file(curve_info):
    try:
        path = Path(curve_info['curve_file']).resolve()
        suffix = path.suffix.lower()
        if suffix and suffix != '.txt':
            logger.error("Неподдерживаемый формат файла: %s", suffix)
            messagebox.showerror(
                "Ошибка",
                f"Ожидался файл с расширением .txt, получен {suffix}"
            )
            return

        X_data = []
        Y_data = []
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.replace(',', ' ').split()
                if len(parts) != 2:
                    logger.error("Некорректная строка данных: %s", line)
                    messagebox.showerror("Ошибка", f"Некорректные данные в строке: {line}")
                    return
                try:
                    X_data.append(float(parts[0]))
                    Y_data.append(float(parts[1]))
                except ValueError:
                    logger.error("Некорректная строка данных: %s", line)
                    messagebox.showerror("Ошибка", f"Некорректные данные в строке: {line}")
                    return
        curve_info['X_values'] = X_data
        curve_info['Y_values'] = Y_data
    except FileNotFoundError:
        logger.error("Файл '%s' не найден.", curve_info['curve_file'])
        messagebox.showerror("Ошибка", f"Не удалось открыть файл {path}")
    except Exception:
        logger.error("Ошибка при чтении файла '%s'.", curve_info['curve_file'])
        messagebox.showerror("Ошибка", f"Не удалось открыть файл {path}")
