import pytest

from analysis_types import AnalysisType
from tabs.function_for_all_tabs.validation import (
    ensure_analysis_type,
    InvalidAnalysisTypeError,
)


def test_ensure_analysis_type_valid():
    assert ensure_analysis_type(AnalysisType.TIME_AXIAL_FORCE.value) == AnalysisType.TIME_AXIAL_FORCE.value


def test_ensure_analysis_type_invalid():
    with pytest.raises(InvalidAnalysisTypeError):
        ensure_analysis_type("неизвестный тип")
