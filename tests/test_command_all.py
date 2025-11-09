from pathlib import Path, PureWindowsPath
from analysis_types import AnalysisType
from tabs.function4tabs4.command_all import (
    collect_commands,
    walk_tree_and_build_commands,
)
from tabs.function4tabs4.tree_schema import Tree, AnalysisFolder, CurveNode
from tabs.function4tabs4.naming import safe_name
from tree_schema import EntityNode, AnalysisNode, FileNode
from topfolder_codec import encode_topfolder


def test_collect_commands():
    tree = Tree(
        analyses=[
            AnalysisFolder(
                name="static",
                curves=[CurveNode(name="curve 1", path="p", props={"b": 2, "a": 1})],
            )
        ]
    )
    cmds = collect_commands(tree)
    assert cmds == [f"{safe_name('curve 1')} --a=1 --b=2"]


def test_walk_tree_and_build_commands(tmp_path):
    analysis = AnalysisType.TIME_NODE_DISPLACEMENT_X.value
    entity = EntityNode(
        user_name="user",
        entity_kind="nodal",
        children=[AnalysisNode(analysis, children=[FileNode(1)])],
    )
    numbered = f"1-{encode_topfolder('user', 'nodal')}"
    folder_map = {(0, 0): f"1-{analysis}"}
    commands = walk_tree_and_build_commands(
        [entity],
        base_project_dir=tmp_path,
        top_folder_names=[numbered],
        analysis_folder_names=folder_map,
    )
    top_folder = numbered
    expected_path = PureWindowsPath(
        tmp_path, "curves", top_folder, folder_map[(0, 0)], "1.txt"
    )
    assert commands == [
        "genselect clear all",
        "genselect node add node 1",
        "ntime 5",
        f'xyplot 1 savefile curve_file "{expected_path}" 1 all',
        "xyplot 1 donemenu",
        "deletewin 1",
    ]


def test_walk_tree_and_build_commands_handles_global(tmp_path):
    entity = EntityNode(
        user_name="global",
        entity_kind="none",
        children=[
            AnalysisNode(AnalysisType.TIME_GLOBAL_KINETIC_ENERGY.value, children=[])
        ],
    )
    numbered = f"1-{encode_topfolder('global', 'none')}"
    commands = walk_tree_and_build_commands(
        [entity], base_project_dir=tmp_path, top_folder_names=[numbered]
    )
    assert commands[0] == "genselect clear all"
    assert commands[1] == "gtime 1"
