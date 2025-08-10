import logging

logger = logging.getLogger(__name__)

def read_curve_from_lsdyna(file_path):
    """Извлекает значения X и Y из файла кривой LS-Dyna."""
    X_data = []
    Y_data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 2:
                    continue
                try:
                    x = float(parts[0])
                    y = float(parts[1])
                except ValueError:
                    continue
                X_data.append(x)
                Y_data.append(y)
    except FileNotFoundError:
        logger.error("Файл '%s' не найден.", file_path)
    except IOError:
        logger.error("Ошибка при чтении файла '%s'.", file_path)
    return X_data, Y_data
