import csv
import logging
from openpyxl import load_workbook
from openpyxl.utils import range_boundaries

logger = logging.getLogger(__name__)


def _read_all_data(file_path):
    if file_path.lower().endswith('.csv'):
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            return [row for row in reader]
    else:
        wb = load_workbook(file_path, data_only=True)
        ws = wb.active
        return [list(row) for row in ws.iter_rows(values_only=True)]


def _extract_range(data, cell_range, horizontal):
    min_col, min_row, max_col, max_row = range_boundaries(cell_range)
    result = []
    if horizontal:
        row_idx = min_row - 1
        for col in range(min_col, max_col + 1):
            value = data[row_idx][col - 1] if row_idx < len(data) and col - 1 < len(data[row_idx]) else None
            if value not in (None, ''):
                try:
                    result.append(float(value))
                except ValueError:
                    logger.error("Некорректное значение: %s", value)
    else:
        col_idx = min_col - 1
        for row in range(min_row, max_row + 1):
            if row - 1 < len(data) and col_idx < len(data[row - 1]):
                value = data[row - 1][col_idx]
                if value not in (None, ''):
                    try:
                        result.append(float(value))
                    except ValueError:
                        logger.error("Некорректное значение: %s", value)
    return result


def read_X_Y_from_excel(curve_info):
    try:
        file_path = curve_info['curve_file']
        horizontal = curve_info.get('excel_horizontal', False)
        x_range = curve_info.get('excel_x_range')
        y_range = curve_info.get('excel_y_range')

        data = _read_all_data(file_path)

        if x_range and y_range:
            X_data = _extract_range(data, x_range, horizontal)
            Y_data = _extract_range(data, y_range, horizontal)
        else:
            if horizontal:
                X_data = [float(v) for v in data[0] if v not in (None, '')]
                Y_data = [float(v) for v in data[1] if v not in (None, '')]
            else:
                X_data = []
                Y_data = []
                for row in data:
                    if len(row) >= 2:
                        x_val, y_val = row[0], row[1]
                        if x_val not in (None, '') and y_val not in (None, ''):
                            try:
                                X_data.append(float(x_val))
                                Y_data.append(float(y_val))
                            except ValueError:
                                logger.error("Некорректная строка данных: %s", row)
        curve_info['X_values'] = X_data
        curve_info['Y_values'] = Y_data
    except FileNotFoundError:
        logger.error("Файл '%s' не найден.", curve_info['curve_file'])
    except Exception as e:
        logger.error("Ошибка при чтении файла '%s': %s", curve_info['curve_file'], e)
