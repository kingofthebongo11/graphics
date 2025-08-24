from enum import Enum

class AnalysisType(str, Enum):
    """Допустимые типы анализа."""
    TIME_AXIAL_FORCE = "Время-Продольное усилие"
    TIME_SHEAR_FORCE_QY = "Время-Поперечная сила QY"
    TIME_SHEAR_FORCE_QZ = "Время-Поперечная сила QZ"
    TIME_MOMENT_MX = "Время-Момент MX"
    TIME_MOMENT_MY = "Время-Момент MY"
    TIME_MOMENT_MZ = "Время-Момент MZ"

    @classmethod
    def list(cls) -> list[str]:
        """Возвращает список строковых значений."""
        return [item.value for item in cls]

ANALYSIS_TYPES = AnalysisType.list()

__all__ = ["AnalysisType", "ANALYSIS_TYPES"]
