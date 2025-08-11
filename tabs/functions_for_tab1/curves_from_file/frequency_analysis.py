import ast
import logging
from tkinter import messagebox

logger = logging.getLogger(__name__)


def read_X_Y_from_frequency_analysis(curve_info):
    try:
        path = curve_info['curve_file']
        with open(path, 'r') as file:
            lines = file.readlines()

        header_XF = (
            f"t {curve_info['curve_typeXF_type']}N {curve_info['curve_typeXF_type']}eig "
            f"{curve_info['curve_typeXF_type']}mass pr{curve_info['curve_typeXF_type']}mass "
            f"totalpr{curve_info['curve_typeXF_type']}mass"
        )
        header_YF = (
            f"t {curve_info['curve_typeYF_type']}N {curve_info['curve_typeYF_type']}eig "
            f"{curve_info['curve_typeYF_type']}mass pr{curve_info['curve_typeYF_type']}mass "
            f"totalpr{curve_info['curve_typeYF_type']}mass"
        )

        headers_map = {
            "Время": 0,
            "Номер доминантной частота": 1,
            "Частота": 2,
            "Масса": 3,
            "Процент от общей массы": 4,
            "Процент общей массы": 5,
        }

        index_X = headers_map.get(curve_info['curve_typeXF'])
        index_Y = headers_map.get(curve_info['curve_typeYF'])

        if index_X is None or index_Y is None:
            logger.error("Ошибка: некорректные параметры curve_typeXF или curve_typeYF.")
            return

        X_data = []
        Y_data = []
        current_block_X = False
        current_block_Y = False

        for line in lines:
            line = line.strip()

            if line == header_XF and line == header_YF:
                current_block_X = True
                current_block_Y = True
                continue
            elif line == header_XF:
                current_block_X = True
                current_block_Y = False
                continue
            elif line == header_YF:
                current_block_Y = True
                current_block_X = False
                continue
            elif line == '':
                current_block_X = False
                current_block_Y = False
                continue

            if current_block_X:
                try:
                    data_list = ast.literal_eval(line)
                    if isinstance(data_list, list) and len(data_list) > index_X:
                        if index_X in (4, 5):
                            X_data.append(float(data_list[index_X].strip('%')))
                        else:
                            X_data.append(float(data_list[index_X]))
                    else:
                        logger.error("Некорректная строка данных: %s", line)
                        messagebox.showerror("Ошибка", f"Некорректные данные в строке: {line}")
                        return
                except (ValueError, SyntaxError):
                    logger.error("Ошибка преобразования строки: %s", line)
                    messagebox.showerror("Ошибка", f"Некорректные данные в строке: {line}")
                    return

            if current_block_Y:
                try:
                    data_list = ast.literal_eval(line)
                    if isinstance(data_list, list) and len(data_list) > index_Y:
                        if index_Y in (4, 5):
                            logger.debug("%s", data_list[index_Y])
                            Y_data.append(float(data_list[index_Y].strip('%')))
                        else:
                            Y_data.append(float(data_list[index_Y]))
                    else:
                        logger.error("Некорректная строка данных: %s", line)
                        messagebox.showerror("Ошибка", f"Некорректные данные в строке: {line}")
                        return
                except (ValueError, SyntaxError):
                    logger.error("Ошибка преобразования строки: %s", line)
                    messagebox.showerror("Ошибка", f"Некорректные данные в строке: {line}")
                    return

        curve_info['X_values'] = X_data
        curve_info['Y_values'] = Y_data

    except FileNotFoundError:
        logger.error("Файл '%s' не найден.", curve_info['curve_file'])
        messagebox.showerror("Ошибка", f"Не удалось открыть файл {path}")
    except Exception:
        logger.error("Ошибка при чтении файла '%s'.", curve_info['curve_file'])
        messagebox.showerror("Ошибка", f"Не удалось открыть файл {path}")
