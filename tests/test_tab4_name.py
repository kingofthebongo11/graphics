import pytest
import tkinter as tk
from tkinter import ttk

from tabs.tab4 import create_tab4


def test_tab4_tab_name():
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tkinter requires a display")
    root.withdraw()
    nb = ttk.Notebook(root)
    create_tab4(nb)
    tab_id = nb.tabs()[-1]
    assert nb.tab(tab_id, "text") == "Авто-кривые Ls-Dyna"
    root.destroy()
