import logging
from openpyxl import load_workbook

logger = logging.getLogger(__name__)


def _extract_values(ws, range_str):
    cells = ws[range_str]
    return [cell.value for row in cells for cell in row if isinstance(cell.value, (int, float))]


def read_X_Y_from_excel_file(curve_info):
    try:
        wb = load_workbook(curve_info['curve_file'], data_only=True)
        ws = wb.active

        horizontal = curve_info.get('horizontal', False)
        x_range = curve_info.get('x_range') or ('1:1' if horizontal else 'A:A')
        y_range = curve_info.get('y_range') or ('2:2' if horizontal else 'B:B')

        curve_info['X_values'] = _extract_values(ws, x_range)
        curve_info['Y_values'] = _extract_values(ws, y_range)
    except FileNotFoundError:
        logger.error("Файл '%s' не найден.", curve_info['curve_file'])
    except Exception as e:
        logger.error("Ошибка при чтении файла '%s': %s", curve_info['curve_file'], e)
