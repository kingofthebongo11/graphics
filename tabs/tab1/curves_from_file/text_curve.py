import logging

logger = logging.getLogger(__name__)

def read_curve_from_text(file_path):
    """Извлекает значения X и Y из простого текстового файла."""
    X_data = []
    Y_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
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
    except FileNotFoundError:
        logger.error("Файл '%s' не найден.", file_path)
    except IOError:
        logger.error("Ошибка при чтении файла '%s'.", file_path)
    return X_data, Y_data
