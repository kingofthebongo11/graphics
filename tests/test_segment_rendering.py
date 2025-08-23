import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pytest
from unittest.mock import patch

from tabs.function_for_all_tabs.plotting import create_plot


def test_labels_applied():
    fig, ax = plt.subplots()
    plt.rcParams.update({"text.usetex": False})
    curves = [{"X_values": [0, 1], "Y_values": [0, 1]}]
    with patch(
        "tabs.function_for_all_tabs.plotting.configure_matplotlib",
        lambda: plt.rcParams.update({"text.usetex": False}),
    ):
        create_plot(curves, "X", "Y", "Title", fig=fig, ax=ax)
    assert ax.get_xlabel() == "X"
    assert ax.get_ylabel() == "Y"
    assert ax.get_title() == "Title"
    plt.close(fig)


def test_invalid_latex_raises():
    fig, ax = plt.subplots()
    plt.rcParams.update({"text.usetex": False})
    curves = [{"X_values": [0, 1], "Y_values": [0, 1]}]
    with patch(
        "tabs.function_for_all_tabs.plotting.configure_matplotlib",
        lambda: plt.rcParams.update({"text.usetex": False}),
    ):
        with pytest.raises(ValueError):
            create_plot(curves, "X$", "Y", "Title", fig=fig, ax=ax)
    plt.close(fig)
