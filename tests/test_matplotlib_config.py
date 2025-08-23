import matplotlib.pyplot as plt
from settings import configure_matplotlib


def test_matplotlib_usetex_and_preamble():
    plt.rcdefaults()
    configure_matplotlib()
    assert plt.rcParams['text.usetex'] is True
    assert plt.rcParams['font.size'] == 12
    assert plt.rcParams['axes.labelsize'] == 14.4
    assert plt.rcParams['axes.titlesize'] == 20.74
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
