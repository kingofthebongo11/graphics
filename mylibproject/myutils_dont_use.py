

def txt_from_file(curve_txt):
    try:
        with open(curve_txt, 'r', encoding='utf-8') as file:
            curve_db = file.read()
            return curve_db
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Произошла ошибка при открытии файла: {e}"

def work_with_curve_db(data):
    strings = data.split('\n')
    start_recording = False  # Флаг для начала записи данных после Maxval
    result = []  # Список для сохранения результатов

    for string in strings:
        if 'Maxval=' in string:  # Проверяем, содержит ли строка 'Maxval='
            start_recording = True  # Если да, начинаем запись данных после этой строки
        elif string.startswith('endcurve'):  # Проверяем, не является ли строка концом данных
            break  # Если да, прерываем цикл
        elif len(string.split()) == 1 and string.split()[0].isnumeric():
            start_recording = True
        elif string == "":
            break
        elif start_recording:  # Если флаг записи активенz
            result.append(string)  # Добавляем строку в результат
    # Объединяем строки из списка результатов в одну строку, используя пробел в качестве разделителя
    return result