import pytest
from analysis_types import AnalysisType, ANALYSIS_TYPE_CODES
from tabs.function4tabs4.command_single import (
    build_curve_commands,
    build_global_curve_commands,
    ETYPE_BY_ELEMENT,
)


def test_build_curve_commands_element():
    analysis = AnalysisType.TIME_AXIAL_FORCE.value
    etype = ETYPE_BY_ELEMENT["beam"]
    etime = ANALYSIS_TYPE_CODES[("element", "beam")][analysis]
    cmds = build_curve_commands(
        base_project_dir="C:\\proj",
        top_folder_name="pilon-element-beam",
        analysis_type=analysis,
        entity_kind="element",
        element_type="beam",
        element_id=7,
    )
    assert cmds == [
        "genselect clear all",
        "genselect target beam",
        "genselect beam add beam 7/0",
        f"etype {etype} ;etime {etime}",
        f'xyplot 1 savefile curve_file "C:\\proj\\curves\\pilon-element-beam\\{analysis}\\7.txt" 1 all',
        "xyplot 1 donemenu",
        "deletewin 1",
    ]


def test_build_curve_commands_nodal():
    analysis = AnalysisType.TIME_NODE_DISPLACEMENT_X.value
    ntime = ANALYSIS_TYPE_CODES[("nodal", None)][analysis]
    cmds = build_curve_commands(
        base_project_dir="C:\\proj",
        top_folder_name="uzli-nodal",
        analysis_type=analysis,
        entity_kind="nodal",
        element_type=None,
        element_id=15,
    )
    assert cmds == [
        "genselect clear all",
        "genselect node add node 15",
        f"ntime {ntime}",
        f'xyplot 1 savefile curve_file "C:\\proj\\curves\\uzli-nodal\\{analysis}\\15.txt" 1 all',
        "xyplot 1 donemenu",
        "deletewin 1",
    ]


def test_build_curve_commands_custom_dirname():
    analysis = AnalysisType.TIME_NODE_DISPLACEMENT_X.value
    cmds = build_curve_commands(
        base_project_dir="C:\\proj",
        top_folder_name="uzli-nodal",
        analysis_type=analysis,
        entity_kind="nodal",
        element_type=None,
        element_id=15,
        analysis_dirname="1-custom",
    )
    assert cmds[3] == (
        'xyplot 1 savefile curve_file "C:\\proj\\curves\\uzli-nodal\\1-custom\\15.txt" 1 all'
    )


@pytest.mark.parametrize(
    "kwargs",
    [
        {"analysis_type": ""},
        {"analysis_type": "unsupported"},
        {"entity_kind": "unknown"},
        {"entity_kind": "element", "element_type": "foo"},
        {"entity_kind": "nodal", "element_type": "beam"},
        {"element_id": 0},
    ],
)
def test_build_curve_commands_invalid(kwargs):
    base_args = dict(
        base_project_dir="C:\\proj",
        top_folder_name="p-nodal",
        analysis_type=AnalysisType.TIME_NODE_DISPLACEMENT_X.value,
        entity_kind="nodal",
        element_type=None,
        element_id=1,
    )
    base_args.update(kwargs)
    with pytest.raises(ValueError):
        build_curve_commands(**base_args)


@pytest.mark.parametrize(
    "analysis, etime", ANALYSIS_TYPE_CODES[("element", "shell")].items()
)
def test_build_curve_commands_shell(analysis, etime):
    etype = ETYPE_BY_ELEMENT["shell"]
    cmds = build_curve_commands(
        base_project_dir="C:\\proj",
        top_folder_name="pilon-element-shell",
        analysis_type=analysis,
        entity_kind="element",
        element_type="shell",
        element_id=3,
    )
    assert cmds[:3] == [
        "genselect clear all",
        "genselect target shell",
        "genselect shell add shell 3/0",
    ]
    assert cmds[3] == f"etype {etype} ;etime {etime}"


def test_analysis_type_codes_shell_updated():
    codes = ANALYSIS_TYPE_CODES[("element", "shell")]
    assert "Время - Изгибающий момент Mx(п)" in codes
    assert "Время - Изгибающий момент My(п)" in codes
    assert "Время - Изгибающий момент Mxy(п)" in codes
    assert "Время - Давление" in codes


def test_build_global_curve_commands():
    analysis = AnalysisType.TIME_GLOBAL_POTENTIAL_ENERGY.value
    gtime = ANALYSIS_TYPE_CODES[("none", None)][analysis]
    cmds = build_global_curve_commands(
        base_project_dir="C:\\proj",
        top_folder_name="global-none",
        analysis_type=analysis,
    )
    assert cmds[0] == "genselect clear all"
    assert cmds[1] == f"gtime {gtime}"
    assert cmds[2].endswith(f"\\{analysis}\\{gtime}.txt\" 1 all")
