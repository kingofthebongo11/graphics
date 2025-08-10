import logging
from pathlib import Path

import openpyxl

logger = logging.getLogger(__name__)


def _cells_to_list(cells):
    return [float(cell.value) for row in cells for cell in row if cell.value is not None]


def read_X_Y_from_excel(curve_info):
    """Читает данные X и Y из Excel-файла.

    Поддерживается выбор ориентации (по горизонтали/по вертикали)
    и указание диапазонов ячеек для X и Y."""
    try:
        file_path = Path(curve_info['curve_file'])
        wb = openpyxl.load_workbook(file_path, data_only=True)
        ws = wb.active

        horizontal = bool(curve_info.get('horizontal'))
        x_range = curve_info.get('X_range')
        y_range = curve_info.get('Y_range')

        if horizontal:
            if x_range and y_range:
                X_cells = ws[x_range]
                Y_cells = ws[y_range]
            else:
                X_cells = [ws[1]]  # первая строка
                Y_cells = [ws[2]]  # вторая строка
            X_data = _cells_to_list(X_cells)
            Y_data = _cells_to_list(Y_cells)
        else:
            if x_range and y_range:
                X_cells = ws[x_range]
                Y_cells = ws[y_range]
                X_data = _cells_to_list(X_cells)
                Y_data = _cells_to_list(Y_cells)
            else:
                X_data = [float(cell[0].value) for cell in ws.iter_rows(min_col=1, max_col=1) if cell[0].value is not None]
                Y_data = [float(cell[0].value) for cell in ws.iter_rows(min_col=2, max_col=2) if cell[0].value is not None]

        curve_info['X_values'] = X_data
        curve_info['Y_values'] = Y_data
    except FileNotFoundError:
        logger.error("Файл '%s' не найден.", curve_info['curve_file'])
    except IOError:
        logger.error("Ошибка при чтении файла '%s'.", curve_info['curve_file'])
    except Exception as e:
        logger.error("Некорректные данные в файле '%s': %s", curve_info['curve_file'], e)
