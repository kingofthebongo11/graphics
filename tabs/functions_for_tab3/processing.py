from pathlib import Path

from tabs.functions_for_tab3.tab3_work_with_file import extract_data_frec_from_file
from mylibproject.myutils_widgets import message_log

from .plotting import create_png_plots
from .file_io import create_txt_file_with_result, create_xlsx_file_with_result


def function1(log_text, path_entry):
    """Основная функция обработки данных для третьей вкладки."""
    file_path_str = path_entry.get()
    if file_path_str:
        file_path = Path(file_path_str)
        message_log(log_text, f"Выбранный путь к проетку LS-Dyna: {file_path}")
        file_path_outeig = file_path / "eigresults"
        file_out_txt = file_path_outeig / "eigoutput.txt"
        file_out_xlsx = file_path_outeig / "eigoutput.xlsx"
        file_path_outeig.mkdir(parents=True, exist_ok=True)
        all_frequencies = []
        all_modal_mass = []
        time_data = []
        index = 1
        n_file = 0
        while True:
            file_name = f"eigout{index}"
            try:
                data_freq = extract_data_frec_from_file(file_path, file_name)
                frequencies = data_freq['cycles_values']
                modal_data = data_freq['modal_data']
                time = data_freq['time']
                time_data.append(time)
                all_modal_mass.append(modal_data)
                all_frequencies.append(frequencies)
                index += 1
            except FileNotFoundError:
                if index == 1:
                    message_log(log_text, "В данной папке нет расчетных файлов по частотному анализу")
                    return
                else:
                    n_file = index - 1
                    message_log(log_text, f"eigout{index} не найден. Значит последний eigout{n_file}")
                    message_log(log_text, "Точки во времени для модального анализа:")
                    message_log(log_text, str(time_data))
                break
        graphs = {
            "Xmass": [],
            "totalprXmass": [],
            "Ymass": [],
            "totalprYmass": [],
            "Zmass": [],
            "totalprZmass": [],
            "XRmass": [],
            "totalprXRmass": [],
            "YRmass": [],
            "totalprYRmass": [],
            "ZRmass": [],
            "totalprZRmass": [],
            "Xeig": [],
            "Yeig": [],
            "Zeig": [],
            "XReig": [],
            "YReig": [],
            "ZReig": [],
            "XN": [],
            "YN": [],
            "ZN": [],
            "XRN": [],
            "YRN": [],
            "ZRN": [],
            "prXmass": [],
            "prYmass": [],
            "prZmass": [],
            "prXRmass": [],
            "prYRmass": [],
            "prZRmass": [],
        }
        for mass, frequencies in zip(all_modal_mass, all_frequencies):
            onecoord = {
                "Xmass": 0,
                "Ymass": 0,
                "Zmass": 0,
                "XRmass": 0,
                "YRmass": 0,
                "ZRmass": 0,
            }
            for i, item in enumerate(mass):
                for key, value in item.items():
                    if key in ["X", "Y", "Z", "XR", "YR", "ZR"]:
                        if float(value) > onecoord[key + 'mass']:
                            onecoord[key + 'mass'] = float(value)
                            onecoord[key + 'eig'] = frequencies[int(item['N']) - 1]
                            onecoord[key + 'N'] = item['N']
                            onecoord['pr' + key + 'mass'] = item['pr' + key]
                            if i > 0:
                                onecoord['pr' + key + 'mass'] = str(
                                    float(onecoord['pr' + key + 'mass'].strip('%')) -
                                    float(mass[i - 1]['pr' + key].strip('%'))
                                ) + '%'
                        onecoord['totalpr' + key + 'mass'] = item['pr' + key]

            for key, value in onecoord.items():
                if key in graphs:
                    graphs[key].append(value)
        data_for_file = {
            't XN Xeig Xmass prXmass totalprXmass': [],
            't YN Yeig Ymass prYmass totalprYmass': [],
            't ZN Zeig Zmass prZmass totalprZmass': [],
            't XRN XReig XRmass prXRmass totalprXRmass': [],
            't YRN YReig YRmass prYRmass totalprYRmass': [],
            't ZRN ZReig ZRmass prZRmass totalprZRmass': []
        }
        for i in range(n_file):
            for s in ['X', 'Y', 'Z', 'XR', 'YR', 'ZR']:
                data_for_file[f't {s}N {s}eig {s}mass pr{s}mass totalpr{s}mass'].append(
                    [time_data[i], graphs[f'{s}N'][i], graphs[f'{s}eig'][i], graphs[f'{s}mass'][i],
                     graphs[f'pr{s}mass'][i], graphs[f'totalpr{s}mass'][i]])

        graph_with_time = {}
        for key, graph in graphs.items():
            values_with_time = []
            for time, value in zip(time_data, graph):
                values_with_time.append([time, value])
            graph_with_time[key] = values_with_time
        create_png_plots(graph_with_time, file_path_outeig, log_text)
        create_txt_file_with_result(file_out_txt, data_for_file, log_text)
        create_xlsx_file_with_result(file_out_xlsx, data_for_file, log_text)

    else:
        message_log(log_text, "Вы не выбрали путь к проетку LS-Dyna, выберите путь в ячейке выше...")
