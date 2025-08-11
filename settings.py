import matplotlib.pyplot as plt


def configure_matplotlib():
    """Configure global matplotlib settings used across the application."""
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 14  # Общий размер шрифта
    plt.rcParams['axes.titlesize'] = 14  # Размер шрифта для заголовков осей
    plt.rcParams['axes.labelsize'] = 14  # Размер шрифта для подписей осей
    plt.rcParams['xtick.labelsize'] = 14  # Размер шрифта для меток оси X
    plt.rcParams['ytick.labelsize'] = 14  # Размер шрифта для меток оси Y
    plt.rcParams['legend.fontsize'] = 14  # Размер шрифта для легенды
