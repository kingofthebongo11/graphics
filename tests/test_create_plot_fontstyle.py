from pathlib import Path
import shutil
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from unittest.mock import patch

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))
from tabs.function_for_all_tabs import create_plot
from tabs.function_for_all_tabs.plotting import TITLE_SIZE, LABEL_SIZE


@pytest.mark.skipif(shutil.which("latex") is None, reason="LaTeX not installed")
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
            legend_title=None,
        )
    expected_title_size = FontProperties(size=TITLE_SIZE).get_size_in_points()
    expected_label_size = FontProperties(size=LABEL_SIZE).get_size_in_points()
    assert ax.title.get_fontstyle() == "normal"
    assert ax.title.get_fontsize() == expected_title_size
    assert ax.xaxis.label.get_fontsize() == expected_label_size
    assert ax.yaxis.label.get_fontsize() == expected_label_size
    plt.close(fig)
