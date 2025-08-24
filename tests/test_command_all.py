from pathlib import Path, PureWindowsPath
from analysis_types import AnalysisType
from tabs.function4tabs4.command_all import collect_commands, walk_tree_and_build_commands
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
    analysis = AnalysisType.TIME_AXIAL_FORCE.value
    entity = EntityNode(
        user_name="user",
        entity_kind="node",
        children=[AnalysisNode(analysis, children=[FileNode(1)])],
    )
    commands = walk_tree_and_build_commands([entity], base_project_dir=tmp_path)
    top_folder = encode_topfolder("user", "node")
    expected_path = PureWindowsPath(
        tmp_path, "curves", top_folder, analysis, "1.txt"
    )
    assert commands == [
        "genselect clear all",
        "genselect node add node 1",
        f'xyplot 1 savefile curve_file "{expected_path}" 1 all',
        "xyplot 1 donemenu",
        "deletewin 1",
    ]
