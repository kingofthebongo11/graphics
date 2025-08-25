from enum import Enum

class AnalysisType(str, Enum):
    """Допустимые типы анализа."""

    TIME_AXIAL_FORCE = "Время - Продольная сила"
    TIME_SHEAR_FORCE_Y = "Время - Поперечная сила по Y"
    TIME_SHEAR_FORCE_Z = "Время - Поперечная сила по Z"
    TIME_BENDING_MOMENT_MS_MY = "Время - Изгибающий момент Ms (My)"
    TIME_BENDING_MOMENT_MT_MZ = "Время - Изгибающий момент Mt (Mz)"
    TIME_TORQUE_MX = "Время - Крутящий момент Mx"
    TIME_NORMAL_STRESS_X = "Время - Нормальное напряжение X"
    TIME_NORMAL_STRESS_Y = "Время - Нормальное напряжение Y"
    TIME_NORMAL_STRESS_Z = "Время - Нормальное напряжение Z"
    TIME_SHEAR_STRESS_XY = "Время - Касательное напряжение XY"
    TIME_SHEAR_STRESS_YZ = "Время - Касательное напряжение YZ"
    TIME_SHEAR_STRESS_ZX = "Время - Касательное напряжение ZX"
    TIME_PLASTIC_STRAIN_INTENSITY = (
        "Время - Интенсивность пластических деформаций"
    )
    TIME_ELONGATION = "Время - Удлинение"
    TIME_STRESS_INTENSITY = "Время - Интенсивность напряжений"
    TIME_PRESSURE = "Время - Давление (п)"
    TIME_BENDING_MOMENT_MX = "Время - Изгибающий момент Mx(п)"
    TIME_BENDING_MOMENT_MY = "Время - Изгибающий момент My(п)"
    TIME_BENDING_MOMENT_MXY = "Время - Изгибающий момент Mxy(п)"

    @classmethod
    def list(cls) -> list[str]:
        """Возвращает список строковых значений."""
        return [item.value for item in cls]

ANALYSIS_TYPES = AnalysisType.list()

# Отдельные списки типов анализа для балочных и оболочечных элементов.
ANALYSIS_TYPES_BEAM: list[str] = [
    AnalysisType.TIME_AXIAL_FORCE.value,
    AnalysisType.TIME_SHEAR_FORCE_Y.value,
    AnalysisType.TIME_SHEAR_FORCE_Z.value,
    AnalysisType.TIME_BENDING_MOMENT_MS_MY.value,
    AnalysisType.TIME_BENDING_MOMENT_MT_MZ.value,
    AnalysisType.TIME_TORQUE_MX.value,
    AnalysisType.TIME_NORMAL_STRESS_X.value,
    AnalysisType.TIME_SHEAR_STRESS_XY.value,
    AnalysisType.TIME_SHEAR_STRESS_ZX.value,
    AnalysisType.TIME_PLASTIC_STRAIN_INTENSITY.value,
    AnalysisType.TIME_ELONGATION.value,
    AnalysisType.TIME_STRESS_INTENSITY.value,
]

ANALYSIS_TYPES_SHELL: list[str] = [
    AnalysisType.TIME_NORMAL_STRESS_X.value,
    AnalysisType.TIME_NORMAL_STRESS_Y.value,
    AnalysisType.TIME_NORMAL_STRESS_Z.value,
    AnalysisType.TIME_SHEAR_STRESS_XY.value,
    AnalysisType.TIME_SHEAR_STRESS_YZ.value,
    AnalysisType.TIME_SHEAR_STRESS_ZX.value,
    AnalysisType.TIME_PLASTIC_STRAIN_INTENSITY.value,
    AnalysisType.TIME_STRESS_INTENSITY.value,
    AnalysisType.TIME_PRESSURE.value,
    AnalysisType.TIME_BENDING_MOMENT_MX.value,
    AnalysisType.TIME_BENDING_MOMENT_MY.value,
    AnalysisType.TIME_BENDING_MOMENT_MXY.value,
]

# Карта доступных типов анализа для разных типов элементов.
ANALYSIS_TYPES_BY_ELEMENT: dict[str | None, list[str]] = {
    "beam": ANALYSIS_TYPES_BEAM,
    "shell": ANALYSIS_TYPES_SHELL,
    "node": [],
}

# Соответствие названия анализа номеру команды etime для разных типов элементов.
ANALYSIS_TYPE_CODES: dict[str, dict[str, int]] = {
    "beam": {
        AnalysisType.TIME_AXIAL_FORCE.value: 1,
        AnalysisType.TIME_SHEAR_FORCE_Y.value: 2,
        AnalysisType.TIME_SHEAR_FORCE_Z.value: 3,
        AnalysisType.TIME_BENDING_MOMENT_MS_MY.value: 4,
        AnalysisType.TIME_BENDING_MOMENT_MT_MZ.value: 5,
        AnalysisType.TIME_TORQUE_MX.value: 6,
        AnalysisType.TIME_NORMAL_STRESS_X.value: 7,
        AnalysisType.TIME_SHEAR_STRESS_XY.value: 8,
        AnalysisType.TIME_SHEAR_STRESS_ZX.value: 9,
        AnalysisType.TIME_PLASTIC_STRAIN_INTENSITY.value: 10,
        AnalysisType.TIME_ELONGATION.value: 11,
        AnalysisType.TIME_STRESS_INTENSITY.value: 12,
    },
    "shell": {
        AnalysisType.TIME_NORMAL_STRESS_X.value: 1,
        AnalysisType.TIME_NORMAL_STRESS_Y.value: 2,
        AnalysisType.TIME_NORMAL_STRESS_Z.value: 3,
        AnalysisType.TIME_SHEAR_STRESS_XY.value: 4,
        AnalysisType.TIME_SHEAR_STRESS_YZ.value: 5,
        AnalysisType.TIME_SHEAR_STRESS_ZX.value: 6,
        AnalysisType.TIME_PLASTIC_STRAIN_INTENSITY.value: 7,
        AnalysisType.TIME_STRESS_INTENSITY.value: 8,
        AnalysisType.TIME_PRESSURE.value: 9,
        AnalysisType.TIME_BENDING_MOMENT_MX.value: 26,
        AnalysisType.TIME_BENDING_MOMENT_MY.value: 27,
        AnalysisType.TIME_BENDING_MOMENT_MXY.value: 28,
    },
}

__all__ = [
    "AnalysisType",
    "ANALYSIS_TYPES",
    "ANALYSIS_TYPES_BEAM",
    "ANALYSIS_TYPES_SHELL",
    "ANALYSIS_TYPES_BY_ELEMENT",
    "ANALYSIS_TYPE_CODES",
]
