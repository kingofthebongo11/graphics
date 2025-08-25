import pytest
import tkinter as tk
from tkinter import ttk

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


def test_move_root_level():
    root, tab = _create_app()
    tree = tab.tree

    a = tree.insert("", "end", text="a")
    b = tree.insert("", "end", text="b")
    c = tree.insert("", "end", text="c")

    tree.selection_set(b)
    tab.move_up()
    assert tree.get_children("") == (b, a, c)

    tree.selection_set(b)
    tab.move_up()
    assert tree.get_children("") == (b, a, c)

    tree.selection_set(b)
    tab.move_down()
    assert tree.get_children("") == (a, b, c)

    tree.selection_set(c)
    tab.move_down()
    assert tree.get_children("") == (a, b, c)
    root.destroy()


def test_move_second_level():
    root, tab = _create_app()
    tree = tab.tree

    parent = tree.insert("", "end", text="top")
    c1 = tree.insert(parent, "end", text="1")
    c2 = tree.insert(parent, "end", text="2")
    c3 = tree.insert(parent, "end", text="3")

    tree.selection_set(c2)
    tab.move_up()
    assert tree.get_children(parent) == (c2, c1, c3)

    tree.selection_set(c2)
    tab.move_up()
    assert tree.get_children(parent) == (c2, c1, c3)

    tree.selection_set(c2)
    tab.move_down()
    assert tree.get_children(parent) == (c1, c2, c3)

    tree.selection_set(c3)
    tab.move_down()
    assert tree.get_children(parent) == (c1, c2, c3)
    root.destroy()
