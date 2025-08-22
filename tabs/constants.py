# -*- coding: utf-8 -*-
"""Константы для вкладок приложения."""

from collections.abc import Sequence


def sort_options(
    options: Sequence[str],
    none_label: str = "Нет",
    other_label: str = "Другое",
) -> list[str]:
    """Сортирует список опций.

    Параметры:
        options: последовательность строк для упорядочивания.
        none_label: метка, которая должна быть первой в списке.
        other_label: метка, которая должна быть последней в списке.

    Возвращает:
        Отсортированный список, где ``none_label`` стоит первым,
        а ``other_label`` — последним.
    """

    first = [none_label] if none_label in options else []
    middle = sorted(
        [opt for opt in options if opt not in (none_label, other_label)]
    )
    last = [other_label] if other_label in options else []
    return first + middle + last


STRESS_UNITS = sort_options(
    [
        "Па",
        "кПа",
        "МПа",
        "Н/мм²",
        "Н/см²",
        "Н/м²",
        "кН/мм²",
        "кН/см²",
        "кН/м²",
        "МН/мм²",
        "МН/см²",
        "МН/м²",
        "кгс/мм²",
        "кгс/см²",
        "кгс/м²",
        "тс/см²",
        "тс/м²",
    ]
)

STRESS_UNITS_EN = sort_options(
    [
        "Pa",
        "kPa",
        "MPa",
        "N/mm²",
        "N/cm²",
        "N/m²",
        "kN/mm²",
        "kN/cm²",
        "kN/m²",
        "MN/mm²",
        "MN/cm²",
        "MN/m²",
        "kgf/mm²",
        "kgf/cm²",
        "kgf/m²",
        "tf/cm²",
        "tf/m²",
    ]
)

UNITS_MAPPING = {
    "Время": sort_options(["мс", "с", "мин", "ч"]),
    "Перемещение по X": sort_options(["мм", "см", "м"]),
    "Перемещение по Y": sort_options(["мм", "см", "м"]),
    "Перемещение по Z": sort_options(["мм", "см", "м"]),
    "Удлинение": sort_options(["мм", "см", "м"]),
    "Удлинение по X": sort_options(["мм", "см", "м"]),
    "Удлинение по Y": sort_options(["мм", "см", "м"]),
    "Удлинение по Z": sort_options(["мм", "см", "м"]),
    "Деформация": sort_options(["—", "%"]),
    "Пластическая деформация": sort_options(["—", "%"]),
    "Сила": sort_options(["мН", "Н", "кН", "кгс", "тс"]),
    "Продольная сила": sort_options(["мН", "Н", "кН", "кгс", "тс"]),
    "Поперечная сила": sort_options(["мН", "Н", "кН", "кгс", "тс"]),
    "Поперечная сила по Y": sort_options(["мН", "Н", "кН", "кгс", "тс"]),
    "Поперечная сила по Z": sort_options(["мН", "Н", "кН", "кгс", "тс"]),
    "Масса": sort_options(["г", "кг", "т"]),
    "Напряжение": STRESS_UNITS,
    "Интенсивность напряжений": STRESS_UNITS,
    "Нормальное напряжение X": STRESS_UNITS,
    "Нормальное напряжение Y": STRESS_UNITS,
    "Нормальное напряжение Z": STRESS_UNITS,
    "Касательное напряжение XY": STRESS_UNITS,
    "Касательное напряжение YX": STRESS_UNITS,
    "Касательное напряжение YZ": STRESS_UNITS,
    "Касательное напряжение ZY": STRESS_UNITS,
    "Касательное напряжение ZX": STRESS_UNITS,
    "Касательное напряжение XZ": STRESS_UNITS,
    "Крутящий момент Mx": sort_options(["Н·м", "кН·м"]),
    "Изгибающий момент Mx": sort_options(["Н·м", "кН·м"]),
    "Изгибающий момент My": sort_options(["Н·м", "кН·м"]),
    "Изгибающий момент Mz": sort_options(["Н·м", "кН·м"]),
    "Частота 1": sort_options(["Гц", "кГц"]),
    "Частота 2": sort_options(["Гц", "кГц"]),
    "Частота 3": sort_options(["Гц", "кГц"]),
    "Другое": [],
}

DEFAULT_UNITS = {
    "Время": "с",
    "Перемещение по X": "м",
    "Перемещение по Y": "м",
    "Перемещение по Z": "м",
    "Удлинение": "м",
    "Удлинение по X": "м",
    "Удлинение по Y": "м",
    "Удлинение по Z": "м",
    "Деформация": "—",
    "Пластическая деформация": "—",
    "Сила": "Н",
    "Продольная сила": "Н",
    "Поперечная сила": "Н",
    "Поперечная сила по Y": "Н",
    "Поперечная сила по Z": "Н",
    "Масса": "кг",
    "Напряжение": "Па",
    "Интенсивность напряжений": "Па",
    "Нормальное напряжение X": "Па",
    "Нормальное напряжение Y": "Па",
    "Нормальное напряжение Z": "Па",
    "Касательное напряжение XY": "Па",
    "Касательное напряжение YX": "Па",
    "Касательное напряжение YZ": "Па",
    "Касательное напряжение ZY": "Па",
    "Касательное напряжение ZX": "Па",
    "Касательное напряжение XZ": "Па",
    "Крутящий момент Mx": "Н·м",
    "Изгибающий момент Mx": "Н·м",
    "Изгибающий момент My": "Н·м",
    "Изгибающий момент Mz": "Н·м",
    "Частота 1": "Гц",
    "Частота 2": "Гц",
    "Частота 3": "Гц",
}

PHYSICAL_QUANTITIES = sort_options(
    [
        "Нет",
        "Время",
        "Деформация",
        "Изгибающий момент Mx",
        "Изгибающий момент My",
        "Изгибающий момент Mz",
        "Интенсивность напряжений",
        "Касательное напряжение XY",
        "Касательное напряжение XZ",
        "Касательное напряжение YX",
        "Касательное напряжение YZ",
        "Касательное напряжение ZX",
        "Касательное напряжение ZY",
        "Крутящий момент Mx",
        "Масса",
        "Напряжение",
        "Нормальное напряжение X",
        "Нормальное напряжение Y",
        "Нормальное напряжение Z",
        "Перемещение по X",
        "Перемещение по Y",
        "Перемещение по Z",
        "Пластическая деформация",
        "Поперечная сила",
        "Поперечная сила по Y",
        "Поперечная сила по Z",
        "Продольная сила",
        "Сила",
        "Удлинение",
        "Удлинение по X",
        "Удлинение по Y",
        "Удлинение по Z",
        "Частота 1",
        "Частота 2",
        "Частота 3",
        "Другое",
    ]
)

PHYSICAL_QUANTITIES_TRANSLATION = {
    "Нет": "None",
    "Время": "Time",
    "Деформация": "Strain",
    "Изгибающий момент Mx": "Bending moment Mx",
    "Изгибающий момент My": "Bending moment My",
    "Изгибающий момент Mz": "Bending moment Mz",
    "Интенсивность напряжений": "Stress intensity",
    "Касательное напряжение XY": "Shear stress XY",
    "Касательное напряжение XZ": "Shear stress XZ",
    "Касательное напряжение YX": "Shear stress YX",
    "Касательное напряжение YZ": "Shear stress YZ",
    "Касательное напряжение ZX": "Shear stress ZX",
    "Касательное напряжение ZY": "Shear stress ZY",
    "Крутящий момент Mx": "Torque Mx",
    "Масса": "Mass",
    "Напряжение": "Stress",
    "Нормальное напряжение X": "Normal stress X",
    "Нормальное напряжение Y": "Normal stress Y",
    "Нормальное напряжение Z": "Normal stress Z",
    "Перемещение по X": "Displacement X",
    "Перемещение по Y": "Displacement Y",
    "Перемещение по Z": "Displacement Z",
    "Пластическая деформация": "Plastic strain",
    "Поперечная сила": "Shear force",
    "Поперечная сила по Y": "Shear force Y",
    "Поперечная сила по Z": "Shear force Z",
    "Продольная сила": "Axial force",
    "Сила": "Force",
    "Удлинение": "Elongation",
    "Удлинение по X": "Elongation X",
    "Удлинение по Y": "Elongation Y",
    "Удлинение по Z": "Elongation Z",
    "Частота 1": "Frequency 1",
    "Частота 2": "Frequency 2",
    "Частота 3": "Frequency 3",
    "Другое": "Other",
}

PHYSICAL_QUANTITIES_EN = sort_options(
    list(PHYSICAL_QUANTITIES_TRANSLATION.values()),
    none_label="None",
    other_label="Other",
)

PHYSICAL_QUANTITIES_EN_TO_RU = {
    en: ru for ru, en in PHYSICAL_QUANTITIES_TRANSLATION.items()
}

TIME_UNITS_EN = sort_options(["ms", "s", "min", "h"])
LENGTH_UNITS_EN = sort_options(["mm", "cm", "m"])
DEFORMATION_UNITS_EN = sort_options(["—", "%"])
FORCE_UNITS_EN = sort_options(["mN", "N", "kN", "kgf", "tf"])
MASS_UNITS_EN = sort_options(["g", "kg", "t"])
MOMENT_UNITS_EN = sort_options(["N·m", "kN·m"])
FREQUENCY_UNITS_EN = sort_options(["Hz", "kHz"])

UNITS_MAPPING_EN = {
    "Time": TIME_UNITS_EN,
    "Displacement X": LENGTH_UNITS_EN,
    "Displacement Y": LENGTH_UNITS_EN,
    "Displacement Z": LENGTH_UNITS_EN,
    "Elongation": LENGTH_UNITS_EN,
    "Elongation X": LENGTH_UNITS_EN,
    "Elongation Y": LENGTH_UNITS_EN,
    "Elongation Z": LENGTH_UNITS_EN,
    "Strain": DEFORMATION_UNITS_EN,
    "Plastic strain": DEFORMATION_UNITS_EN,
    "Force": FORCE_UNITS_EN,
    "Axial force": FORCE_UNITS_EN,
    "Shear force": FORCE_UNITS_EN,
    "Shear force Y": FORCE_UNITS_EN,
    "Shear force Z": FORCE_UNITS_EN,
    "Mass": MASS_UNITS_EN,
    "Stress": STRESS_UNITS_EN,
    "Stress intensity": STRESS_UNITS_EN,
    "Normal stress X": STRESS_UNITS_EN,
    "Normal stress Y": STRESS_UNITS_EN,
    "Normal stress Z": STRESS_UNITS_EN,
    "Shear stress XY": STRESS_UNITS_EN,
    "Shear stress YX": STRESS_UNITS_EN,
    "Shear stress YZ": STRESS_UNITS_EN,
    "Shear stress ZY": STRESS_UNITS_EN,
    "Shear stress ZX": STRESS_UNITS_EN,
    "Shear stress XZ": STRESS_UNITS_EN,
    "Torque Mx": MOMENT_UNITS_EN,
    "Bending moment Mx": MOMENT_UNITS_EN,
    "Bending moment My": MOMENT_UNITS_EN,
    "Bending moment Mz": MOMENT_UNITS_EN,
    "Frequency 1": FREQUENCY_UNITS_EN,
    "Frequency 2": FREQUENCY_UNITS_EN,
    "Frequency 3": FREQUENCY_UNITS_EN,
    "Other": [],
}

DEFAULT_UNITS_EN = {
    "Time": "s",
    "Displacement X": "m",
    "Displacement Y": "m",
    "Displacement Z": "m",
    "Elongation": "m",
    "Elongation X": "m",
    "Elongation Y": "m",
    "Elongation Z": "m",
    "Strain": "—",
    "Plastic strain": "—",
    "Force": "N",
    "Axial force": "N",
    "Shear force": "N",
    "Shear force Y": "N",
    "Shear force Z": "N",
    "Mass": "kg",
    "Stress": "Pa",
    "Stress intensity": "Pa",
    "Normal stress X": "Pa",
    "Normal stress Y": "Pa",
    "Normal stress Z": "Pa",
    "Shear stress XY": "Pa",
    "Shear stress YX": "Pa",
    "Shear stress YZ": "Pa",
    "Shear stress ZY": "Pa",
    "Shear stress ZX": "Pa",
    "Shear stress XZ": "Pa",
    "Torque Mx": "N·m",
    "Bending moment Mx": "N·m",
    "Bending moment My": "N·m",
    "Bending moment Mz": "N·m",
    "Frequency 1": "Hz",
    "Frequency 2": "Hz",
    "Frequency 3": "Hz",
}

TITLE_TRANSLATIONS = {
    "Время": {"Русский": r"Время $\mathbf{t}$", "Английский": r"Time $\mathbf{t}$"},
    "Перемещение по X": {
        "Русский": r"Перемещение $\mathbf{x}$",
        "Английский": r"Displacement $\mathbf{x}$",
    },
    "Перемещение по Y": {
        "Русский": r"Перемещение $\mathbf{y}$",
        "Английский": r"Displacement $\mathbf{y}$",
    },
    "Перемещение по Z": {
        "Русский": r"Перемещение $\mathbf{z}$",
        "Английский": r"Displacement $\mathbf{z}$",
    },
    "Удлинение": {
        "Русский": r"Удлинение $\Delta \mathbf{l}$",
        "Английский": r"Elongation $\Delta \mathbf{l}$",
    },
    "Удлинение по X": {
        "Русский": r"Удлинение $\Delta \mathbf{l}_{\mathbf{x}}$",
        "Английский": r"Elongation $\Delta \mathbf{l}_{\mathbf{x}}$",
    },
    "Удлинение по Y": {
        "Русский": r"Удлинение $\Delta \mathbf{l}_{\mathbf{y}}$",
        "Английский": r"Elongation $\Delta \mathbf{l}_{\mathbf{y}}$",
    },
    "Удлинение по Z": {
        "Русский": r"Удлинение $\Delta \mathbf{l}_{\mathbf{z}}$",
        "Английский": r"Elongation $\Delta \mathbf{l}_{\mathbf{z}}$",
    },
    "Деформация": {
        "Русский": r"Деформация $\mathbf{\varepsilon}$",
        "Английский": r"Strain $\mathbf{\varepsilon}$",
    },
    "Пластическая деформация": {
        "Русский": r"Пластическая деформация $\mathbf{\varepsilon}_{\mathbf{p}}$",
        "Английский": r"Plastic strain $\mathbf{\varepsilon}_{\mathbf{p}}$",
    },
    "Сила": {"Русский": r"Сила $\mathbf{F}$", "Английский": r"Force $\mathbf{F}$"},
    "Продольная сила": {
        "Русский": r"Продольная сила $\mathbf{N}$",
        "Английский": r"Axial force $\mathbf{N}$",
    },
    "Поперечная сила": {
        "Русский": r"Поперечная сила $\mathbf{Q}$",
        "Английский": r"Shear force $\mathbf{Q}$",
    },
    "Поперечная сила по Y": {
        "Русский": r"Поперечная сила $\mathbf{Q}_{\mathbf{y}}$",
        "Английский": r"Shear force $\mathbf{Q}_{\mathbf{y}}$",
    },
    "Поперечная сила по Z": {
        "Русский": r"Поперечная сила $\mathbf{Q}_{\mathbf{z}}$",
        "Английский": r"Shear force $\mathbf{Q}_{\mathbf{z}}$",
    },
    "Масса": {"Русский": r"Масса $\mathbf{m}$", "Английский": r"Mass $\mathbf{m}$"},
    "Напряжение": {
        "Русский": r"Напряжение $\mathbf{\sigma}$",
        "Английский": r"Stress $\mathbf{\sigma}$",
    },
    "Интенсивность напряжений": {
        "Русский": r"Интенсивность напряжений $\mathbf{\sigma}_{\mathbf{i}}$",
        "Английский": r"Stress intensity $\mathbf{\sigma}_{\mathbf{i}}$",
    },
    "Нормальное напряжение X": {
        "Русский": r"Нормальное напряжение $\mathbf{\sigma}_{\mathbf{x}}$",
        "Английский": r"Normal stress $\mathbf{\sigma}_{\mathbf{x}}$",
    },
    "Нормальное напряжение Y": {
        "Русский": r"Нормальное напряжение $\mathbf{\sigma}_{\mathbf{y}}$",
        "Английский": r"Normal stress $\mathbf{\sigma}_{\mathbf{y}}$",
    },
    "Нормальное напряжение Z": {
        "Русский": r"Нормальное напряжение $\mathbf{\sigma}_{\mathbf{z}}$",
        "Английский": r"Normal stress $\mathbf{\sigma}_{\mathbf{z}}$",
    },
    "Касательное напряжение XY": {
        "Русский": r"Касательное напряжение $\mathbf{\tau}_{\mathbf{x}\mathbf{y}}$",
        "Английский": r"Shear stress $\mathbf{\tau}_{\mathbf{x}\mathbf{y}}$",
    },
    "Касательное напряжение XZ": {
        "Русский": r"Касательное напряжение $\mathbf{\tau}_{\mathbf{x}\mathbf{z}}$",
        "Английский": r"Shear stress $\mathbf{\tau}_{\mathbf{x}\mathbf{z}}$",
    },
    "Касательное напряжение YX": {
        "Русский": r"Касательное напряжение $\mathbf{\tau}_{\mathbf{y}\mathbf{x}}$",
        "Английский": r"Shear stress $\mathbf{\tau}_{\mathbf{y}\mathbf{x}}$",
    },
    "Касательное напряжение YZ": {
        "Русский": r"Касательное напряжение $\mathbf{\tau}_{\mathbf{y}\mathbf{z}}$",
        "Английский": r"Shear stress $\mathbf{\tau}_{\mathbf{y}\mathbf{z}}$",
    },
    "Касательное напряжение ZX": {
        "Русский": r"Касательное напряжение $\mathbf{\tau}_{\mathbf{z}\mathbf{x}}$",
        "Английский": r"Shear stress $\mathbf{\tau}_{\mathbf{z}\mathbf{x}}$",
    },
    "Касательное напряжение ZY": {
        "Русский": r"Касательное напряжение $\mathbf{\tau}_{\mathbf{z}\mathbf{y}}$",
        "Английский": r"Shear stress $\mathbf{\tau}_{\mathbf{z}\mathbf{y}}$",
    },
    "Крутящий момент Mx": {
        "Русский": r"Крутящий момент $\mathbf{M}_{\mathbf{x}}$",
        "Английский": r"Torque $\mathbf{M}_{\mathbf{x}}$",
    },
    "Изгибающий момент Mx": {
        "Русский": r"Изгибающий момент $\mathbf{M}_{\mathbf{x}}$",
        "Английский": r"Bending moment $\mathbf{M}_{\mathbf{x}}$",
    },
    "Изгибающий момент My": {
        "Русский": r"Изгибающий момент $\mathbf{M}_{\mathbf{y}}$",
        "Английский": r"Bending moment $\mathbf{M}_{\mathbf{y}}$",
    },
    "Изгибающий момент Mz": {
        "Русский": r"Изгибающий момент $\mathbf{M}_{\mathbf{z}}$",
        "Английский": r"Bending moment $\mathbf{M}_{\mathbf{z}}$",
    },
    "Частота 1": {
        "Русский": r"Частота $\mathbf{f}_{\mathit{1}}$",
        "Английский": r"Frequency $\mathbf{f}_{\mathit{1}}$",
    },
    "Частота 2": {
        "Русский": r"Частота $\mathbf{f}_{\mathit{2}}$",
        "Английский": r"Frequency $\mathbf{f}_{\mathit{2}}$",
    },
    "Частота 3": {
        "Русский": r"Частота $\mathbf{f}_{\mathit{3}}$",
        "Английский": r"Frequency $\mathbf{f}_{\mathit{3}}$",
    },
}

__all__ = [
    "STRESS_UNITS",
    "UNITS_MAPPING",
    "DEFAULT_UNITS",
    "PHYSICAL_QUANTITIES",
    "STRESS_UNITS_EN",
    "UNITS_MAPPING_EN",
    "DEFAULT_UNITS_EN",
    "PHYSICAL_QUANTITIES_EN",
    "PHYSICAL_QUANTITIES_EN_TO_RU",
    "TITLE_TRANSLATIONS",
]
