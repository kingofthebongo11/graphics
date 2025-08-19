import os
from tabs.functions_for_tab3.Figurenameclass import FigureNames
from widgets.message_log import message_log

from tabs.function_for_all_tabs import create_plot


def create_png_plots(graph_with_time, file_path_outeig, log_text):
    """Создает PNG-графики характеристик во времени."""

    for name, graph in graph_with_time.items():
        X_values = [float(item[0]) for item in graph]
        xlabel = "Время $t$, с"
        namefig = FigureNames(name)

        keys = ["XR", "YR", "ZR", "X", "Y", "Z"]
        for key in keys:
            if key in name:
                directory = os.path.join(file_path_outeig, key)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                file_plt = os.path.join(directory, f"{namefig.generate_filename()}.png")
                break
        if "pr" in name:
            Y_values = [
                float(value[1].strip("%")) if isinstance(value[1], str) else value[1]
                for value in graph
            ]
            curves_info = [{"X_values": X_values, "Y_values": Y_values}]
            create_plot(
                curves_info,
                xlabel,
                namefig.generate_plot_ylabel(),
                namefig.generate_plot_title(),
                pr_y=True,
                save_file=True,
                file_plt=file_plt,
            )
        else:
            Y_values = [float(item[1]) for item in graph]
            curves_info = [{"X_values": X_values, "Y_values": Y_values}]
            create_plot(
                curves_info,
                xlabel,
                namefig.generate_plot_ylabel(),
                namefig.generate_plot_title(),
                pr_y=False,
                save_file=True,
                file_plt=file_plt,
            )

    message_log(log_text, "Созданы графики всех характеристик")
