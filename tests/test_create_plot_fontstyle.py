from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.append(str(Path(__file__).resolve().parent.parent))
from tabs.function_for_all_tabs import create_plot
from unittest.mock import patch


def test_default_title_fontstyle_normal():
    fig, ax = plt.subplots()
    curves = [{"X_values": [0, 1], "Y_values": [0, 1]}]
    with patch(
        "tabs.function_for_all_tabs.plotting.configure_matplotlib", lambda: None
    ):
        plt.rcParams.update({"text.usetex": False})
        create_plot(
            curves,
            "X",
            "Y",
            "Title",
            fig=fig,
            ax=ax,
        )
    assert ax.title.get_fontstyle() == "normal"
    plt.close(fig)
