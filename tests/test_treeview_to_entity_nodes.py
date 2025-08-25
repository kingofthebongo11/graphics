import pytest
import tkinter as tk
from tkinter import ttk

from tabs.tab4 import treeview_to_entity_nodes
from topfolder_codec import encode_topfolder
from tree_schema import EntityNode, AnalysisNode, FileNode
from tabs.function4tabs4.command_all import walk_tree_and_build_commands
from tabs.function4tabs4.cfile_writer import write_cfile
from analysis_types import ANALYSIS_TYPES_BEAM


def test_treeview_to_entity_nodes_and_cfile(tmp_path):
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Tkinter requires a display")
    root.withdraw()
    tree = ttk.Treeview(root)

    top_text = encode_topfolder("user", "node")
    top = tree.insert("", "end", text=top_text)
    analysis_type = ANALYSIS_TYPES_BEAM[0]
    analysis = tree.insert(top, "end", text=analysis_type)
    tree.insert(analysis, "end", text="1")

    nodes = treeview_to_entity_nodes(tree)
    expected = [
        EntityNode(
            user_name="user",
            entity_kind="node",
            element_type=None,
            children=[
                AnalysisNode(analysis_type=analysis_type, children=[FileNode(id=1)])
            ],
        )
    ]
    assert nodes == expected

    commands = walk_tree_and_build_commands(nodes, tmp_path)
    path = tmp_path / "out.cfile"
    write_cfile(commands, path)
    assert path.exists()
    assert path.read_text(encoding="utf-8").splitlines() == commands
    root.destroy()
