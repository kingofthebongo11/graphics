import matplotlib

from tabs.function_for_all_tabs.plotting import format_plot_title_bfit


def test_format_plot_title_bfit_mathtext():
    prev = matplotlib.rcParams["text.usetex"]
    matplotlib.rcParams["text.usetex"] = False
    try:
        assert format_plot_title_bfit("σ_x, МПа") == r"$\boldsymbol{\mathit{σ_x}}$, МПа"
        assert format_plot_title_bfit("Time, s") == "Time, s"
    finally:
        matplotlib.rcParams["text.usetex"] = prev


def test_format_plot_title_bfit_usetex():
    prev = matplotlib.rcParams["text.usetex"]
    matplotlib.rcParams["text.usetex"] = True
    try:
        assert format_plot_title_bfit("E, ГПа") == r"$\bm{\mathit{E}}$, ГПа"
    finally:
        matplotlib.rcParams["text.usetex"] = prev


def test_format_plot_title_bfit_no_double_wrap():
    prev = matplotlib.rcParams["text.usetex"]
    matplotlib.rcParams["text.usetex"] = False
    try:
        s = r"$\boldsymbol{\mathit{t}}$"
        assert format_plot_title_bfit(s) == s
    finally:
        matplotlib.rcParams["text.usetex"] = prev
