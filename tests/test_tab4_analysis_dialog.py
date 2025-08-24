import pytest
import tkinter as tk
from tkinter import ttk

import tabs.tab4 as tab4mod
from tabs.tab4 import create_tab4
from analysis_types import ANALYSIS_TYPES


def _create_app():
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tkinter requires a display")
    root.withdraw()
    nb = ttk.Notebook(root)
    tab = create_tab4(nb)
    return root, tab


def test_add_analysis_type(monkeypatch):
    root, tab = _create_app()
    tree = tab.tree
    parent = tree.get_children()[0]
    tree.selection_set(parent)
    choice = ANALYSIS_TYPES[0]

    class DummyDialog:
        def __init__(self, *a, **k):
            self.result = choice

    monkeypatch.setattr(tab4mod, "AnalysisTypeDialog", DummyDialog)
    tab.add_node()
    child = tree.get_children(parent)[-1]
    assert tree.item(child, "text") == choice
    root.destroy()
