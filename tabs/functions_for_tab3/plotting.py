import os
from mylibproject.Figurenameclass import FigureNames
from mylibproject.myutils_widgets import message_log


def create_png_plots(graph_with_time, file_path_outeig, log_text):
    """Создает PNG-графики характеристик во времени."""
    from main import create_plot  # локальный импорт для избежания циклической зависимости

    for name, graph in graph_with_time.items():
        X_values = [float(item[0]) for item in graph]
        xlabel = 'Время $t$, с'
        namefig = FigureNames(name)

        keys = ['XR', 'YR', 'ZR', 'X', 'Y', 'Z']
        for key in keys:
            if key in name:
                directory = os.path.join(file_path_outeig, key)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                file_plt = os.path.join(directory, f'{namefig.generate_filename()}.png')
                break
        if 'pr' in name:
            Y_values = [float(value[1].strip('%')) if isinstance(value[1], str) else value[1] for value in graph]
            curves_info = [{'X_values': X_values, 'Y_values': Y_values}]
            create_plot(curves_info, xlabel, namefig.generate_plot_ylabel(), namefig.generate_plot_title(),
                        True, True, file_plt)
        else:
            Y_values = [float(item[1]) for item in graph]
            curves_info = [{'X_values': X_values, 'Y_values': Y_values}]
            create_plot(curves_info, xlabel, namefig.generate_plot_ylabel(), namefig.generate_plot_title(),
                        False, True, file_plt)

    message_log(log_text, "Созданы графики всех характеристик")
