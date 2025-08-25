import pytest
import tkinter as tk
from tkinter import ttk

import tabs.tab4 as tab4mod
from tabs.tab4 import create_tab4
from topfolder_codec import encode_topfolder
from analysis_types import ANALYSIS_TYPES_BEAM, ANALYSIS_TYPES_SHELL


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

    add_params = {"name": "top", "kind": "node", "elem": None}
    rename_params = {"name": "new", "kind": "element", "elem": "beam"}

    def _make_dialog(params):
        class DummySectionDialog:
            def __init__(self, _parent, tree_widget, item=None):
                text = encode_topfolder(
                    params["name"], params["kind"], params["elem"]
                )
                if item:
                    tree_widget.item(item, text=text)
                else:
                    tree_widget.insert("", "end", text=text)
                self.result = text

        return DummySectionDialog

    monkeypatch.setattr(tab4mod, "SectionDialog", _make_dialog(add_params))
    tab.add_node()
    new_item = tree.get_children()[-1]
    assert tree.item(new_item, "text") == encode_topfolder(**add_params)

    tree.selection_set(new_item)
    monkeypatch.setattr(tab4mod, "SectionDialog", _make_dialog(rename_params))
    tab.rename_node()
    assert tree.item(new_item, "text") == encode_topfolder(**rename_params)

    tab.remove_node()
    assert len(tree.get_children()) == start
    root.destroy()


def test_analysis_types_dependent_on_element_type(monkeypatch):
    root, tab = _create_app()
    tree = tab.tree

    captured: list[list[str]] = []

    class DummyDialog:
        def __init__(self, _parent, title, values):  # noqa: D401
            captured.append(values)
            self.result = None

    monkeypatch.setattr(tab4mod, "AnalysisTypeDialog", DummyDialog)

    beam_top = tree.insert(
        "", "end", text=encode_topfolder("b", "element", "beam")
    )
    tree.selection_set(beam_top)
    tab.add_node()

    shell_top = tree.insert(
        "", "end", text=encode_topfolder("s", "element", "shell")
    )
    tree.selection_set(shell_top)
    tab.add_node()

    assert captured[0] == ANALYSIS_TYPES_BEAM
    assert captured[1] == ANALYSIS_TYPES_SHELL
    assert "Время - Изгибающий момент Mx(п)" in ANALYSIS_TYPES_SHELL
    assert "Время - Изгибающий момент My(п)" in ANALYSIS_TYPES_SHELL
    assert "Время - Изгибающий момент Mxy(п)" in ANALYSIS_TYPES_SHELL
    assert "Время - Давление" in ANALYSIS_TYPES_SHELL
    root.destroy()
