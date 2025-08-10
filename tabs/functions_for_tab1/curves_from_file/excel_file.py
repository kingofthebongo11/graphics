import csv
import logging
from pathlib import Path

from openpyxl import load_workbook

logger = logging.getLogger(__name__)


def read_X_Y_from_excel(curve_info):
    try:
        path = Path(curve_info['curve_file'])
        suffix = path.suffix.lower()
        X_data = []
        Y_data = []
        horizontal = curve_info.get('horizontal', False)

        if suffix in {'.xlsx', '.xlsm'}:
            wb = load_workbook(path, read_only=True, data_only=True)
            ws = wb.active
            if horizontal:
                rows = list(ws.iter_rows(values_only=True))
                if len(rows) >= 2:
                    row_x, row_y = rows[0], rows[1]
                    for x, y in zip(row_x, row_y):
                        if x is None or y is None:
                            continue
                        try:
                            X_data.append(float(str(x).replace(',', '.')))
                            Y_data.append(float(str(y).replace(',', '.')))
                        except (ValueError, TypeError):
                            logger.error("Некорректная пара данных: %s, %s", x, y)
            else:
                for row in ws.iter_rows(values_only=True):
                    if row is None or len(row) < 2:
                        continue
                    x, y = row[0], row[1]
                    if x is None or y is None:
                        continue
                    try:
                        X_data.append(float(str(x).replace(',', '.')))
                        Y_data.append(float(str(y).replace(',', '.')))
                    except (ValueError, TypeError):
                        logger.error("Некорректная строка данных: %s", row)
        elif suffix == '.csv':
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                if horizontal:
                    rows = list(reader)
                    if len(rows) >= 2:
                        for x, y in zip(rows[0], rows[1]):
                            try:
                                X_data.append(float(x.replace(',', '.')))
                                Y_data.append(float(y.replace(',', '.')))
                            except ValueError:
                                logger.error("Некорректная пара данных: %s, %s", x, y)
                else:
                    for row in reader:
                        if len(row) < 2:
                            continue
                        try:
                            X_data.append(float(row[0].replace(',', '.')))
                            Y_data.append(float(row[1].replace(',', '.')))
                        except ValueError:
                            logger.error("Некорректная строка данных: %s", row)
        else:
            logger.error("Неподдерживаемый формат файла: %s", suffix)
            return

        curve_info['X_values'] = X_data
        curve_info['Y_values'] = Y_data
    except FileNotFoundError:
        logger.error("Файл '%s' не найден.", curve_info['curve_file'])
    except Exception:
        logger.error("Ошибка при чтении файла '%s'.", curve_info['curve_file'])
