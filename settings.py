import matplotlib.pyplot as plt


def configure_matplotlib():
    """Configure global matplotlib settings used across the application."""
    plt.rcParams.update({
        'text.usetex': True,
        'font.family': 'serif',
        'font.size': 14,  # Общий размер шрифта
        'axes.titlesize': 14,  # Размер шрифта для заголовков осей
        'axes.labelsize': 14,  # Размер шрифта для подписей осей
        'xtick.labelsize': 14,  # Размер шрифта для меток оси X
        'ytick.labelsize': 14,  # Размер шрифта для меток оси Y
        'legend.fontsize': 14,  # Размер шрифта для легенды
        'text.latex.preamble': "\n".join([
            r'\usepackage[utf8]{inputenc}',
            r'\usepackage[T1]{fontenc}',
            r'\usepackage[russian]{babel}',
            r'\usepackage{tempora}',
            r'\usepackage{newtxmath}',
            r'\usepackage{amsmath}',
            r'\usepackage{bm}',
            r'\usepackage{upgreek}',
        ]),
    })
