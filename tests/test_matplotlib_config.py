import matplotlib.pyplot as plt
from cycler import cycler

from color_palettes import PALETTES
from settings import configure_matplotlib


def test_matplotlib_usetex_and_preamble():
    plt.rcdefaults()
    configure_matplotlib()
    assert plt.rcParams['text.usetex'] is True
    assert plt.rcParams['font.size'] == 12
    assert plt.rcParams['axes.labelsize'] == 14.4
    assert plt.rcParams['axes.titlesize'] == 17.28
    assert plt.rcParams['axes.prop_cycle'] == cycler(color=PALETTES['LS-Dyna'])
    preamble = plt.rcParams['text.latex.preamble']
    required_packages = [
        '\\usepackage[utf8]{inputenc}',
        '\\usepackage[T2A]{fontenc}',
        '\\usepackage[protrusion=true,expansion=false,final]{microtype}',
        '\\usepackage{graphicx}',
        '\\usepackage[russian]{babel}',
        '\\usepackage{tempora}',
        '\\usepackage{newtxmath}',
        '\\usepackage{amsmath}',
        '\\usepackage{bm}',
        '\\usepackage{upgreek}',
    ]
    for pkg in required_packages:
        assert pkg in preamble
    assert '\\usepackage[T1]{fontenc}' not in preamble
