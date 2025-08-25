import pytest
import tkinter as tk
from tkinter import ttk

import tabs.tab4 as tab4mod
from tabs.tab4 import create_tab4
from analysis_types import ANALYSIS_TYPES_BEAM


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

    class DummySectionDialog:
        def __init__(self, _parent, tree_widget, item=None):
            tree_widget.insert("", "end", text="top")
            self.result = "top"

    monkeypatch.setattr(tab4mod, "SectionDialog", DummySectionDialog)
    tab.add_node()
    parent = tree.get_children("")[-1]
    tree.selection_set(parent)

    choice = ANALYSIS_TYPES_BEAM[0]

    class DummyDialog:
        def __init__(self, *a, **k):
            self.result = choice

    monkeypatch.setattr(tab4mod, "AnalysisTypeDialog", DummyDialog)
    tab.add_node()
    child = tree.get_children(parent)[-1]
    assert tree.item(child, "text") == choice
    root.destroy()


def test_add_element_number(monkeypatch):
    root, tab = _create_app()
    tree = tab.tree

    class DummySectionDialog:
        def __init__(self, _parent, tree_widget, item=None):
            tree_widget.insert("", "end", text="top")
            self.result = "top"

    monkeypatch.setattr(tab4mod, "SectionDialog", DummySectionDialog)
    tab.add_node()
    top = tree.get_children("")[-1]
    tree.selection_set(top)

    choice = ANALYSIS_TYPES_BEAM[0]

    class DummyDialog:
        def __init__(self, *a, **k):
            self.result = choice

    monkeypatch.setattr(tab4mod, "AnalysisTypeDialog", DummyDialog)
    tab.add_node()
    analysis = tree.get_children(top)[-1]
    tree.selection_set(analysis)

    monkeypatch.setattr(tab4mod.simpledialog, "askstring", lambda *a, **k: "15")
    tab.add_node()
    child = tree.get_children(analysis)[-1]
    assert tree.item(child, "text") == "15"
    root.destroy()
