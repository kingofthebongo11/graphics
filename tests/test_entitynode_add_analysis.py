import pytest

from analysis_types import AnalysisType
from tree_schema import EntityNode


def test_add_analysis_valid():
    node = EntityNode(user_name="user", entity_kind="nodal")
    analysis = node.add_analysis(AnalysisType.TIME_AXIAL_FORCE.value)
    assert analysis in node.children
    assert analysis.analysis_type == AnalysisType.TIME_AXIAL_FORCE.value


def test_add_analysis_invalid():
    node = EntityNode(user_name="user", entity_kind="nodal")
    with pytest.raises(ValueError):
        node.add_analysis("неизвестный тип")


def test_add_analysis_duplicate():
    node = EntityNode(user_name="user", entity_kind="nodal")
    node.add_analysis(AnalysisType.TIME_AXIAL_FORCE.value)
    with pytest.raises(ValueError):
        node.add_analysis(AnalysisType.TIME_AXIAL_FORCE.value)
