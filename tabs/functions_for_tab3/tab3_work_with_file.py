from pathlib import Path


def extract_data_frec_from_file(file_path, file_name):
    file = (Path(file_path) / file_name).resolve()
    with file.open('r') as fileeig:
        lines = fileeig.readlines()

    time = None
    cycles_values = []
    numbers_mass_value = []

    # Переменные для контроля состояния
    start_cycles = False
    start_modal = -1

    # Проходим по каждой строке файла
    for line in lines:
        # Извлечение времени (problem time)
        if "problem time" in line and time is None:
            words = line.split()
            time = float(words[-1])

        # Извлечение значений CYCLES
        if "CYCLES" in line:
            words = line.split()
            index = words.index("CYCLES")
            start_cycles = True
            continue
        if start_cycles:
            numbers = line.split()
            if numbers:
                cycles_values.append(float(numbers[index]))
            else:
                start_cycles = False

        # Извлечение данных для модальных частот (X-TRAN, X-ROT)
        if "X-TRAN" in line and "X-ROT" not in line:
            start_modal = 2
        elif "X-ROT" in line and "X-TRAN" not in line:
            start_modal = 5
        elif start_modal == 0:
            numbers = line.split()
            if numbers:
                numbers_mass_value.append({"X": numbers[1],
                                           "Y": numbers[3],
                                           "Z": numbers[5],
                                           "prX": numbers[2],
                                           "prY": numbers[4],
                                           "prZ": numbers[6],
                                           "N": numbers[0]})
            else:
                start_modal = -1
        elif start_modal == 3:
            numbers = line.split()
            if numbers:
                for value in numbers_mass_value:
                    if value["N"] == numbers[0]:
                        value["XR"] = numbers[1]
                        value["YR"] = numbers[3]
                        value["ZR"] = numbers[5]
                        value["prXR"] = numbers[2]
                        value["prYR"] = numbers[4]
                        value["prZR"] = numbers[6]
            else:
                start_modal = -1
        else:
            start_modal -= 1

    return {"time": time, "cycles_values": cycles_values, "modal_data": numbers_mass_value}
