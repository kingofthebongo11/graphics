import pytest
import tkinter as tk
from tkinter import ttk

import tabs.tab4 as tab4mod
from tabs.tab4 import create_tab4


def _create_app():
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tkinter requires a display")
    root.withdraw()
    nb = ttk.Notebook(root)
    tab = create_tab4(nb)
    return root, tab


def test_add_rename_remove_top_nodes(monkeypatch):
    root, tab = _create_app()
    tree = tab.tree

    start = len(tree.get_children())

    class DummySectionDialog:
        def __init__(self, _parent, tree_widget, item=None):
            if item:
                tree_widget.item(item, text="Renamed")
            else:
                tree_widget.insert("", "end", text="Added")
            self.result = "ok"

    monkeypatch.setattr(tab4mod, "SectionDialog", DummySectionDialog)

    tab.add_node()
    assert len(tree.get_children()) == start + 1

    new_item = tree.get_children()[-1]
    tree.selection_set(new_item)
    tab.rename_node()
    assert tree.item(new_item, "text") == "Renamed"

    tab.remove_node()
    assert len(tree.get_children()) == start
    root.destroy()
