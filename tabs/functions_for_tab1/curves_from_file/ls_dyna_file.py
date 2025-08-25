import logging
from pathlib import Path
from tkinter import messagebox

logger = logging.getLogger(__name__)


def read_X_Y_from_ls_dyna(curve_info):
    """Читает значения X и Y из файла LS-Dyna.

    Сначала функция ищет в первых строках специальные маркеры формата
    LS-DYNA (``LS-DYNA``, ``*KEYWORD`` или ``Curveplot``). Если маркеры не
    обнаружены, то выполняется дополнительная проверка: первая строка
    интерпретируется как количество точек, после чего считываются пары
    чисел.

    Строки, не содержащие хотя бы двух числовых значений (заголовки,
    комментарии и т.п.), пропускаются без генерации сообщения об ошибке.
    """
    path = Path(curve_info['curve_file']).resolve()
    X_data: list[float] = []
    Y_data: list[float] = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            header_lines = [file.readline() for _ in range(5)]
            markers = ("LS-DYNA", "*KEYWORD", "Curveplot")
            has_markers = any(
                any(marker in line for marker in markers) for line in header_lines
            )

            file.seek(0)
            if has_markers:
                lines_iterator = file
            else:
                first_line = header_lines[0].strip()
                parts = first_line.split()
                if len(parts) == 1:
                    try:
                        expected_points = int(parts[0])
                    except ValueError:  # строка не число
                        logger.error(
                            "Файл '%s' не является файлом LS-DYNA.", path
                        )
                        messagebox.showerror(
                            "Ошибка", f"Файл {path} не соответствует формату LS-DYNA"
                        )
                        raise ValueError("Файл не соответствует формату LS-DYNA")
                    # Считываем строки после первой как источник точек
                    file.readline()  # пропускаем строку с количеством точек
                    lines_iterator = (file.readline() for _ in range(expected_points))
                else:
                    logger.error("Файл '%s' не является файлом LS-DYNA.", path)
                    messagebox.showerror(
                        "Ошибка", f"Файл {path} не соответствует формату LS-DYNA"
                    )
                    raise ValueError("Файл не соответствует формату LS-DYNA")

            for raw_line in lines_iterator:
                if raw_line is None:
                    break
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
