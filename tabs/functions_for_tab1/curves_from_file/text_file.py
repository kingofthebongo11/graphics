import logging

logger = logging.getLogger(__name__)


def read_X_Y_from_text_file(curve_info):
    try:
        X_data = []
        Y_data = []
        with open(curve_info['curve_file'], 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.replace(',', ' ').split()
                if len(parts) < 2:
                    continue
                try:
                    X_data.append(float(parts[0]))
                    Y_data.append(float(parts[1]))
                except ValueError:
                    logger.error("Некорректная строка данных: %s", line)
        curve_info['X_values'] = X_data
        curve_info['Y_values'] = Y_data
    except FileNotFoundError:
        logger.error("Файл '%s' не найден.", curve_info['curve_file'])
    except IOError:
        logger.error("Ошибка при чтении файла '%s'.", curve_info['curve_file'])
