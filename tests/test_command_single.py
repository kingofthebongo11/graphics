import pytest
from tabs.function4tabs4.command_single import build_curve_commands


def test_build_curve_commands_element():
    cmds = build_curve_commands(
        base_project_dir="C:\\proj",
        top_folder_name="pilon-element-beam",
        analysis_type="static",
        entity_kind="element",
        element_type="beam",
        element_id=7,
    )
    assert cmds == [
        "genselect clear all",
        "genselect beam add beam 7/0",
        "etype 1 ;etime 4",
        'xyplot 1 savefile curve_file "C:\\proj\\curves\\pilon-element-beam\\static\\7.txt" 1 all',
        "xyplot 1 donemenu",
        "deletewin 1",
    ]


def test_build_curve_commands_node():
    cmds = build_curve_commands(
        base_project_dir="C:\\proj",
        top_folder_name="uzli-node",
        analysis_type="dynamic",
        entity_kind="node",
        element_type=None,
        element_id=15,
    )
    assert cmds == [
        "genselect clear all",
        "genselect node add node 15",
        'xyplot 1 savefile curve_file "C:\\proj\\curves\\uzli-node\\dynamic\\15.txt" 1 all',
        "xyplot 1 donemenu",
        "deletewin 1",
    ]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"analysis_type": ""},
        {"entity_kind": "unknown"},
        {"entity_kind": "element", "element_type": "foo"},
        {"entity_kind": "node", "element_type": "beam"},
        {"element_id": 0},
    ],
)
def test_build_curve_commands_invalid(kwargs):
    base_args = dict(
        base_project_dir="C:\\proj",
        top_folder_name="p-node",
        analysis_type="static",
        entity_kind="node",
        element_type=None,
        element_id=1,
    )
    base_args.update(kwargs)
    with pytest.raises(ValueError):
        build_curve_commands(**base_args)
