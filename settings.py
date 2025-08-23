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
        'text.latex.preamble': (
            r'\usepackage[utf8]{inputenc}\n'
            r'\usepackage[T1]{fontenc}\n'
            r'\usepackage[russian]{babel}\n'
            r'\usepackage{tempora}\n'
            r'\usepackage{newtxmath}\n'
            r'\usepackage{amsmath}\n'
            r'\usepackage{bm}\n'
            r'\usepackage{upgreek}'
        ),
    })
