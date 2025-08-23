from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.append(str(Path(__file__).resolve().parent.parent))
from tabs.function_for_all_tabs import create_plot
from tabs.title_utils import split_signature


def test_default_title_fontstyle_normal():
    fig, ax = plt.subplots()
    curves = [{"X_values": [0, 1], "Y_values": [0, 1]}]
    create_plot(
        curves,
        split_signature("X", bold=False),
        split_signature("Y", bold=False),
        split_signature("Title", bold=True),
        fig=fig,
        ax=ax,
    )
    assert ax.texts[0].get_fontstyle() == "normal"
    plt.close(fig)
