import json
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

    top_text = f"1-{encode_topfolder('user', 'node')}"
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

    # Проверка сериализации в JSON
    data = [node.to_dict() for node in nodes]
    json_str = json.dumps(data)
    loaded = json.loads(json_str)

    # Восстановление дерева из JSON
    tree2 = ttk.Treeview(root)
    for item in loaded:
        entity = EntityNode.from_dict(item)
        top2 = tree2.insert(
            "",
            "end",
            text=f"1-{encode_topfolder(entity.user_name, entity.entity_kind, entity.element_type)}",
        )
        for analysis2 in entity.children:
            an_id = tree2.insert(top2, "end", text=analysis2.analysis_type)
            for file in analysis2.children:
                tree2.insert(an_id, "end", text=str(file.id))
    assert treeview_to_entity_nodes(tree2) == expected

    numbered = [f"1-{encode_topfolder('user', 'node')}" for _ in nodes]
    commands = walk_tree_and_build_commands(
        nodes, tmp_path, top_folder_names=numbered
    )
    path = tmp_path / "out.cfile"
    write_cfile(commands, path)
    assert path.exists()
    assert path.read_text(encoding="utf-8").splitlines() == commands
    root.destroy()
