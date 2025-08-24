from enum import Enum

class AnalysisType(str, Enum):
    """Допустимые типы анализа."""
    TIME_AXIAL_FORCE = "Время-Продольная сила"
    TIME_SHEAR_FORCE_Y = "Время-Поперечная сила по Y"
    TIME_SHEAR_FORCE_Z = "Время-Поперечная сила по Z"
    TIME_BENDING_MOMENT_MS_MY = "Время-Изгибающий момент Ms (My)"
    TIME_BENDING_MOMENT_MT_MZ = "Время-Изгибающий момент Mt (Mz)"
    TIME_TORQUE_MX = "Время-Крутящий момент Mx"
    TIME_NORMAL_STRESS_X = "Время-Нормальное напряжение X"
    TIME_SHEAR_STRESS_XY = "Время-Касательное напряжение XY"
    TIME_SHEAR_STRESS_ZX = "Время-Касательное напряжение ZX"
    TIME_PLASTIC_STRAIN_INTENSITY = (
        "Время-Интенсивность пластических деформаций"
    )
    TIME_ELONGATION = "Время-Удлинение"
    TIME_STRESS_INTENSITY = "Время-Интенсивность напряжений"

    @classmethod
    def list(cls) -> list[str]:
        """Возвращает список строковых значений."""
        return [item.value for item in cls]

ANALYSIS_TYPES = AnalysisType.list()

__all__ = ["AnalysisType", "ANALYSIS_TYPES"]
