import logging
import os
from openpyxl import load_workbook
import csv
from openpyxl.utils import range_boundaries

logger = logging.getLogger(__name__)


def _extract_from_ws(ws, cell_range, horizontal):
    """Extract numeric data from worksheet for given range."""
    cells = ws[cell_range]
    data = []
    try:
        if horizontal:
            # cells is tuple with one row
            for cell in cells[0]:
                if cell.value is not None:
                    try:
                        data.append(float(cell.value))
                    except (TypeError, ValueError):
                        continue
        else:
            for row in cells:
                cell = row[0]
                if cell.value is not None:
                    try:
                        data.append(float(cell.value))
                    except (TypeError, ValueError):
                        continue
    except IndexError:
        pass
    return data


def _extract_from_csv(rows, cell_range, horizontal):
    """Extract numeric data from CSV rows based on Excel-like range."""
    min_col, min_row, max_col, max_row = range_boundaries(cell_range)
    data = []
    if horizontal:
        row_idx = min_row - 1
        if 0 <= row_idx < len(rows):
            row = rows[row_idx]
            for col in range(min_col, max_col + 1):
                col_idx = col - 1
                if col_idx < len(row):
                    try:
                        data.append(float(row[col_idx]))
                    except (TypeError, ValueError):
                        continue
    else:
        col_idx = min_col - 1
        for row in range(min_row, max_row + 1):
            row_idx = row - 1
            if 0 <= row_idx < len(rows) and col_idx < len(rows[row_idx]):
                try:
                    data.append(float(rows[row_idx][col_idx]))
                except (TypeError, ValueError):
                    continue
    return data


def read_X_Y_from_excel(curve_info):
    """Read X and Y values from an Excel or CSV file."""
    try:
        file_path = curve_info['curve_file']
        horizontal = curve_info.get('horizontal', False)
        use_range = curve_info.get('use_range', False)
        X_range = curve_info.get('X_range')
        Y_range = curve_info.get('Y_range')
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            with open(file_path, newline='', encoding='utf-8') as f:
                rows = list(csv.reader(f))
            if use_range and X_range and Y_range:
                X_data = _extract_from_csv(rows, X_range, horizontal)
                Y_data = _extract_from_csv(rows, Y_range, horizontal)
            else:
                if horizontal:
                    X_data = [float(v) for v in rows[0] if v]
                    Y_data = [float(v) for v in rows[1] if v]
                else:
                    X_data, Y_data = [], []
                    for row in rows:
                        if len(row) >= 2:
                            try:
                                X_data.append(float(row[0]))
                                Y_data.append(float(row[1]))
                            except ValueError:
                                continue
        else:
            wb = load_workbook(file_path, data_only=True)
            ws = wb.active
            if use_range and X_range and Y_range:
                X_data = _extract_from_ws(ws, X_range, horizontal)
                Y_data = _extract_from_ws(ws, Y_range, horizontal)
            else:
                if horizontal:
                    X_data = _extract_from_ws(ws, '1:1', True)
                    Y_data = _extract_from_ws(ws, '2:2', True)
                else:
                    X_data = _extract_from_ws(ws, 'A:A', False)
                    Y_data = _extract_from_ws(ws, 'B:B', False)
        curve_info['X_values'] = X_data
        curve_info['Y_values'] = Y_data
    except FileNotFoundError:
        logger.error("Файл '%s' не найден.", curve_info.get('curve_file'))
    except Exception as e:
        logger.error("Ошибка при чтении файла '%s': %s", curve_info.get('curve_file'), e)
