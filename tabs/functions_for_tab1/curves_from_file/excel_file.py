import logging
import os
import openpyxl
import csv

logger = logging.getLogger(__name__)


def _is_number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _read_range(cells):
    data = []
    for row in cells:
        for cell in row:
            num = _is_number(cell.value)
            if num is not None:
                data.append(num)
    return data


def read_X_Y_from_excel(curve_info):
    """Читает данные X и Y из файла Excel или CSV.

    Ожидается, что curve_info содержит ключи:
    - curve_file: путь к файлу
    - excel_horizontal: bool, чтение по строкам, если True
    - excel_rangeX: диапазон ячеек для X (например, "A1:A10" или "1:1")
    - excel_rangeY: диапазон ячеек для Y
    """
    try:
        file_path = curve_info['curve_file']
        horizontal = curve_info.get('excel_horizontal', False)
        range_x = curve_info.get('excel_rangeX')
        range_y = curve_info.get('excel_rangeY')

        _, ext = os.path.splitext(file_path)
        ext = ext.lower()

        X_data = []
        Y_data = []

        if ext == '.csv':
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = list(csv.reader(csvfile))
            if horizontal:
                row_x = int(range_x.split(':')[0]) if range_x else 1
                row_y = int(range_y.split(':')[0]) if range_y else 2
                X_data = [_is_number(v) for v in reader[row_x - 1] if _is_number(v) is not None]
                Y_data = [_is_number(v) for v in reader[row_y - 1] if _is_number(v) is not None]
            else:
                col_x = range_x.split(':')[0] if range_x else 'A'
                col_y = range_y.split(':')[0] if range_y else 'B'
                idx_x = openpyxl.utils.column_index_from_string(col_x) - 1
                idx_y = openpyxl.utils.column_index_from_string(col_y) - 1
                for row in reader:
                    if idx_x < len(row):
                        num = _is_number(row[idx_x])
                        if num is not None:
                            X_data.append(num)
                    if idx_y < len(row):
                        num = _is_number(row[idx_y])
                        if num is not None:
                            Y_data.append(num)
        else:
            wb = openpyxl.load_workbook(file_path, data_only=True)
            ws = wb.active
            if horizontal:
                range_x = range_x or '1:1'
                range_y = range_y or '2:2'
                X_data = _read_range(ws[range_x])
                Y_data = _read_range(ws[range_y])
            else:
                range_x = range_x or 'A:A'
                range_y = range_y or 'B:B'
                X_data = _read_range(ws[range_x])
                Y_data = _read_range(ws[range_y])

        curve_info['X_values'] = X_data
        curve_info['Y_values'] = Y_data
    except FileNotFoundError:
        logger.error("Файл '%s' не найден.", curve_info['curve_file'])
    except Exception as e:
        logger.error("Ошибка при чтении файла '%s': %s", curve_info['curve_file'], e)
