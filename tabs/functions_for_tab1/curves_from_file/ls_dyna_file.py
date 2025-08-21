import logging
from tkinter import messagebox

logger = logging.getLogger(__name__)


def read_X_Y_from_ls_dyna(curve_info):
    """Читает значения X и Y из файла LS-Dyna.

    Функция проверяет несколько первых строк файла на наличие маркеров
    формата LS-DYNA (``LS-DYNA``, ``*KEYWORD`` или ``Curveplot``). Если ни
    один из них не найден, выбрасывается исключение :class:`ValueError`.

    Строки, не содержащие хотя бы двух числовых значений (заголовки,
    комментарии и т.п.), пропускаются без генерации сообщения об ошибке.
    """
    path = curve_info['curve_file']
    X_data: list[float] = []
    Y_data: list[float] = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            header_lines = [file.readline() for _ in range(5)]
            markers = ("LS-DYNA", "*KEYWORD", "Curveplot")
            if not any(any(marker in line for marker in markers) for line in header_lines):
                logger.error("Файл '%s' не является файлом LS-DYNA.", path)
                raise ValueError("Файл не соответствует формату LS-DYNA")
            file.seek(0)
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
        curve_info.pop('X_values', None)
        curve_info.pop('Y_values', None)
        logger.error("Файл '%s' не найден.", path)
        messagebox.showerror("Ошибка", f"Не удалось открыть файл {path}")
    except ValueError:
        curve_info.pop('X_values', None)
        curve_info.pop('Y_values', None)
        raise
    except Exception:
        curve_info.pop('X_values', None)
        curve_info.pop('Y_values', None)
        logger.error("Ошибка при чтении файла '%s'.", path)
        messagebox.showerror("Ошибка", f"Не удалось открыть файл {path}")
