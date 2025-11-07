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
    TIME_PRESSURE = "Время - Давление"
    TIME_BENDING_MOMENT_MX = "Время - Изгибающий момент Mx(п)"
    TIME_BENDING_MOMENT_MY = "Время - Изгибающий момент My(п)"
    TIME_BENDING_MOMENT_MXY = "Время - Изгибающий момент Mxy(п)"
    TIME_GLOBAL_KINETIC_ENERGY = "Время - Кинетическая энергия"
    TIME_GLOBAL_POTENTIAL_ENERGY = "Время - Потенциальная энергия"
    TIME_GLOBAL_TOTAL_ENERGY = "Время - Полная энергия"
    TIME_NODE_COORDINATE_X = "Время - Координата X"
    TIME_NODE_COORDINATE_Y = "Время - Координата Y"
    TIME_NODE_COORDINATE_Z = "Время - Координата Z"
    TIME_NODE_COORDINATE_TOTAL = "Время - Суммарная координата (модуль)"
    TIME_NODE_DISPLACEMENT_X = "Время - Перемещение по X"
    TIME_NODE_DISPLACEMENT_Y = "Время - Перемещение по Y"
    TIME_NODE_DISPLACEMENT_Z = "Время - Перемещение по Z"
    TIME_NODE_DISPLACEMENT_TOTAL = "Время - Результирующее перемещение (модуль)"
    TIME_NODE_VELOCITY_X = "Время - Скорость по X"
    TIME_NODE_VELOCITY_Y = "Время - Скорость по Y"
    TIME_NODE_VELOCITY_Z = "Время - Скорость по Z"
    TIME_NODE_VELOCITY_TOTAL = "Время - Результирующая скорость (модуль)"
    TIME_NODE_ACCELERATION_X = "Время - Ускорение по X"
    TIME_NODE_ACCELERATION_Y = "Время - Ускорение по Y"
    TIME_NODE_ACCELERATION_Z = "Время - Ускорение по Z"
    TIME_NODE_ACCELERATION_TOTAL = "Время - Результирующее ускорение (модуль)"

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

ANALYSIS_TYPES_GLOBAL: list[str] = [
    AnalysisType.TIME_GLOBAL_KINETIC_ENERGY.value,
    AnalysisType.TIME_GLOBAL_POTENTIAL_ENERGY.value,
    AnalysisType.TIME_GLOBAL_TOTAL_ENERGY.value,
]

ANALYSIS_TYPES_NODAL: list[str] = [
    AnalysisType.TIME_NODE_COORDINATE_X.value,
    AnalysisType.TIME_NODE_COORDINATE_Y.value,
    AnalysisType.TIME_NODE_COORDINATE_Z.value,
    AnalysisType.TIME_NODE_COORDINATE_TOTAL.value,
    AnalysisType.TIME_NODE_DISPLACEMENT_X.value,
    AnalysisType.TIME_NODE_DISPLACEMENT_Y.value,
    AnalysisType.TIME_NODE_DISPLACEMENT_Z.value,
    AnalysisType.TIME_NODE_DISPLACEMENT_TOTAL.value,
    AnalysisType.TIME_NODE_VELOCITY_X.value,
    AnalysisType.TIME_NODE_VELOCITY_Y.value,
    AnalysisType.TIME_NODE_VELOCITY_Z.value,
    AnalysisType.TIME_NODE_VELOCITY_TOTAL.value,
    AnalysisType.TIME_NODE_ACCELERATION_X.value,
    AnalysisType.TIME_NODE_ACCELERATION_Y.value,
    AnalysisType.TIME_NODE_ACCELERATION_Z.value,
    AnalysisType.TIME_NODE_ACCELERATION_TOTAL.value,
]

# Карта доступных типов анализа для разных комбинаций сущностей.
ANALYSIS_TYPES_BY_ENTITY: dict[tuple[str, str | None], list[str]] = {
    ("element", "beam"): ANALYSIS_TYPES_BEAM,
    ("element", "shell"): ANALYSIS_TYPES_SHELL,
    ("element", "solid"): [],
    ("nodal", None): ANALYSIS_TYPES_NODAL,
    ("none", None): ANALYSIS_TYPES_GLOBAL,
}

# Соответствие названия анализа номеру команды etime для разных типов элементов.
ANALYSIS_TYPE_CODES: dict[tuple[str, str | None], dict[str, int]] = {
    ("element", "beam"): {
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
    ("element", "shell"): {
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
    ("nodal", None): {
        AnalysisType.TIME_NODE_COORDINATE_X.value: 1,
        AnalysisType.TIME_NODE_COORDINATE_Y.value: 2,
        AnalysisType.TIME_NODE_COORDINATE_Z.value: 3,
        AnalysisType.TIME_NODE_COORDINATE_TOTAL.value: 4,
        AnalysisType.TIME_NODE_DISPLACEMENT_X.value: 5,
        AnalysisType.TIME_NODE_DISPLACEMENT_Y.value: 6,
        AnalysisType.TIME_NODE_DISPLACEMENT_Z.value: 7,
        AnalysisType.TIME_NODE_DISPLACEMENT_TOTAL.value: 8,
        AnalysisType.TIME_NODE_VELOCITY_X.value: 9,
        AnalysisType.TIME_NODE_VELOCITY_Y.value: 10,
        AnalysisType.TIME_NODE_VELOCITY_Z.value: 11,
        AnalysisType.TIME_NODE_VELOCITY_TOTAL.value: 12,
        AnalysisType.TIME_NODE_ACCELERATION_X.value: 13,
        AnalysisType.TIME_NODE_ACCELERATION_Y.value: 14,
        AnalysisType.TIME_NODE_ACCELERATION_Z.value: 15,
        AnalysisType.TIME_NODE_ACCELERATION_TOTAL.value: 16,
    },
    ("none", None): {
        AnalysisType.TIME_GLOBAL_KINETIC_ENERGY.value: 1,
        AnalysisType.TIME_GLOBAL_POTENTIAL_ENERGY.value: 2,
        AnalysisType.TIME_GLOBAL_TOTAL_ENERGY.value: 3,
    },
}

__all__ = [
    "AnalysisType",
    "ANALYSIS_TYPES",
    "ANALYSIS_TYPES_BEAM",
    "ANALYSIS_TYPES_SHELL",
    "ANALYSIS_TYPES_GLOBAL",
    "ANALYSIS_TYPES_NODAL",
    "ANALYSIS_TYPES_BY_ENTITY",
    "ANALYSIS_TYPE_CODES",
]
