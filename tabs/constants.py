# -*- coding: utf-8 -*-
"""Константы для вкладок приложения."""

from collections.abc import Sequence
import re


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


def sort_unit_pairs(
    pairs: Sequence[tuple[str, str]],
    none_label: str = "Нет",
    other_label: str = "Другое",
) -> list[tuple[str, str]]:
    """Сортирует пары единиц измерения."""

    ru_to_en = dict(pairs)
    sorted_ru = sort_options(ru_to_en.keys(), none_label, other_label)
    return [(ru, ru_to_en[ru]) for ru in sorted_ru]


STRESS_UNITS_PAIRS = sort_unit_pairs(
    [
        ("Па", "Pa"),
        ("кПа", "kPa"),
        ("МПа", "MPa"),
        ("Н/мм²", "N/mm²"),
        ("Н/см²", "N/cm²"),
        ("Н/м²", "N/m²"),
        ("кН/мм²", "kN/mm²"),
        ("кН/см²", "kN/cm²"),
        ("кН/м²", "kN/m²"),
        ("МН/мм²", "MN/mm²"),
        ("МН/см²", "MN/cm²"),
        ("МН/м²", "MN/m²"),
        ("кгс/мм²", "kgf/mm²"),
        ("кгс/см²", "kgf/cm²"),
        ("кгс/м²", "kgf/m²"),
        ("тс/см²", "tf/cm²"),
        ("тс/м²", "tf/m²"),
    ]
)

STRESS_UNITS = [ru for ru, _ in STRESS_UNITS_PAIRS]
STRESS_UNITS_EN = [en for _, en in STRESS_UNITS_PAIRS]

TIME_UNIT_PAIRS = sort_unit_pairs([
    ("мс", "ms"),
    ("с", "s"),
    ("мин", "min"),
    ("ч", "h"),
])

LENGTH_UNIT_PAIRS = sort_unit_pairs([
    ("мм", "mm"),
    ("см", "cm"),
    ("м", "m"),
])

DEFORMATION_UNIT_PAIRS = sort_unit_pairs([
    ("—", "—"),
    ("%", "%"),
])

FORCE_UNIT_PAIRS = sort_unit_pairs([
    ("мН", "mN"),
    ("Н", "N"),
    ("кН", "kN"),
    ("кгс", "kgf"),
    ("тс", "tf"),
])

MASS_UNIT_PAIRS = sort_unit_pairs([
    ("г", "g"),
    ("кг", "kg"),
    ("т", "t"),
])

MOMENT_UNIT_PAIRS = sort_unit_pairs([
    ("Н·м", "N·m"),
    ("кН·м", "kN·m"),
    ("кгс·м", "kgf·m"),
    ("тс·м", "tf·m"),
])

FREQUENCY_UNIT_PAIRS = sort_unit_pairs([
    ("Гц", "Hz"),
    ("кГц", "kHz"),
])


UNITS_PAIRS = {
    "Время": TIME_UNIT_PAIRS,
    "Перемещение по X": LENGTH_UNIT_PAIRS,
    "Перемещение по Y": LENGTH_UNIT_PAIRS,
    "Перемещение по Z": LENGTH_UNIT_PAIRS,
    "Удлинение": LENGTH_UNIT_PAIRS,
    "Удлинение по X": LENGTH_UNIT_PAIRS,
    "Удлинение по Y": LENGTH_UNIT_PAIRS,
    "Удлинение по Z": LENGTH_UNIT_PAIRS,
    "Деформация": DEFORMATION_UNIT_PAIRS,
    "Пластическая деформация": DEFORMATION_UNIT_PAIRS,
    "Интенсивность пластических деформаций": DEFORMATION_UNIT_PAIRS,
    "Сила": FORCE_UNIT_PAIRS,
    "Продольная сила": FORCE_UNIT_PAIRS,
    "Поперечная сила": FORCE_UNIT_PAIRS,
    "Поперечная сила по Y": FORCE_UNIT_PAIRS,
    "Поперечная сила по Z": FORCE_UNIT_PAIRS,
    "Масса": MASS_UNIT_PAIRS,
    "Напряжение": STRESS_UNITS_PAIRS,
    "Интенсивность напряжений": STRESS_UNITS_PAIRS,
    "Нормальное напряжение X": STRESS_UNITS_PAIRS,
    "Нормальное напряжение Y": STRESS_UNITS_PAIRS,
    "Нормальное напряжение Z": STRESS_UNITS_PAIRS,
    "Касательное напряжение XY": STRESS_UNITS_PAIRS,
    "Касательное напряжение YX": STRESS_UNITS_PAIRS,
    "Касательное напряжение YZ": STRESS_UNITS_PAIRS,
    "Касательное напряжение ZY": STRESS_UNITS_PAIRS,
    "Касательное напряжение ZX": STRESS_UNITS_PAIRS,
    "Касательное напряжение XZ": STRESS_UNITS_PAIRS,
    "Крутящий момент Mx": MOMENT_UNIT_PAIRS,
    "Изгибающий момент Mx": MOMENT_UNIT_PAIRS,
    "Изгибающий момент Ms (My)": MOMENT_UNIT_PAIRS,
    "Изгибающий момент My": MOMENT_UNIT_PAIRS,
    "Изгибающий момент Mt (Mz)": MOMENT_UNIT_PAIRS,
    "Изгибающий момент Mz": MOMENT_UNIT_PAIRS,
    "Частота 1": FREQUENCY_UNIT_PAIRS,
    "Частота 2": FREQUENCY_UNIT_PAIRS,
    "Частота 3": FREQUENCY_UNIT_PAIRS,
    "Другое": [],
}

UNITS_MAPPING = {
    quantity: [ru for ru, _ in pairs]
    for quantity, pairs in UNITS_PAIRS.items()
}

UNITS_TRANSLATION = {
    quantity: {ru: en for ru, en in pairs}
    for quantity, pairs in UNITS_PAIRS.items()
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
    "Интенсивность пластических деформаций": "—",
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
    "Изгибающий момент Ms (My)": "Н·м",
    "Изгибающий момент My": "Н·м",
    "Изгибающий момент Mt (Mz)": "Н·м",
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
        "Изгибающий момент Ms (My)",
        "Изгибающий момент My",
        "Изгибающий момент Mt (Mz)",
        "Изгибающий момент Mz",
        "Интенсивность пластических деформаций",
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
    "Изгибающий момент Ms (My)": "Bending moment Ms (My)",
    "Изгибающий момент My": "Bending moment My",
    "Изгибающий момент Mt (Mz)": "Bending moment Mt (Mz)",
    "Изгибающий момент Mz": "Bending moment Mz",
    "Интенсивность пластических деформаций": "Plastic strain intensity",
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

TIME_UNITS_EN = [en for _, en in TIME_UNIT_PAIRS]
LENGTH_UNITS_EN = [en for _, en in LENGTH_UNIT_PAIRS]
DEFORMATION_UNITS_EN = [en for _, en in DEFORMATION_UNIT_PAIRS]
FORCE_UNITS_EN = [en for _, en in FORCE_UNIT_PAIRS]
MASS_UNITS_EN = [en for _, en in MASS_UNIT_PAIRS]
MOMENT_UNITS_EN = [en for _, en in MOMENT_UNIT_PAIRS]
FREQUENCY_UNITS_EN = [en for _, en in FREQUENCY_UNIT_PAIRS]

UNITS_MAPPING_EN = {
    PHYSICAL_QUANTITIES_TRANSLATION[ru]: [en for _, en in pairs]
    for ru, pairs in UNITS_PAIRS.items()
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
    "Plastic strain intensity": "—",
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
    "Bending moment Ms (My)": "N·m",
    "Bending moment My": "N·m",
    "Bending moment Mt (Mz)": "N·m",
    "Bending moment Mz": "N·m",
    "Frequency 1": "Hz",
    "Frequency 2": "Hz",
    "Frequency 3": "Hz",
}

# Подписи осей с обычным курсивом
TITLE_TRANSLATIONS = {
    "Время": {"Русский": r"Время $\mathit{t}$", "Английский": r"Time $\mathit{t}$"},
    "Перемещение по X": {
        "Русский": r"Перемещение $\mathit{x}$",
        "Английский": r"Displacement $\mathit{x}$",
    },
    "Перемещение по Y": {
        "Русский": r"Перемещение $\mathit{y}$",
        "Английский": r"Displacement $\mathit{y}$",
    },
    "Перемещение по Z": {
        "Русский": r"Перемещение $\mathit{z}$",
        "Английский": r"Displacement $\mathit{z}$",
    },
    "Удлинение": {
        "Русский": r"Удлинение $\Delta \mathit{l}$",
        "Английский": r"Elongation $\Delta \mathit{l}$",
    },
    "Удлинение по X": {
        "Русский": r"Удлинение $\Delta \mathit{l}_{\mathit{x}}$",
        "Английский": r"Elongation $\Delta \mathit{l}_{\mathit{x}}$",
    },
    "Удлинение по Y": {
        "Русский": r"Удлинение $\Delta \mathit{l}_{\mathit{y}}$",
        "Английский": r"Elongation $\Delta \mathit{l}_{\mathit{y}}$",
    },
    "Удлинение по Z": {
        "Русский": r"Удлинение $\Delta \mathit{l}_{\mathit{z}}$",
        "Английский": r"Elongation $\Delta \mathit{l}_{\mathit{z}}$",
    },
    "Деформация": {
        "Русский": r"Деформация \upvarepsilon",
        "Английский": r"Strain \upvarepsilon",
    },
    "Пластическая деформация": {
        "Русский": r"Пластическая деформация \upvarepsilon_{\mathit{p}}",
        "Английский": r"Plastic strain \upvarepsilon_{\mathit{p}}",
    },
    "Интенсивность пластических деформаций": {
        "Русский": r"Интенсивность пластических деформаций \upvarepsilon_{\mathit{i}\mathit{p}}",
        "Английский": r"Plastic strain intensity \upvarepsilon_{\mathit{i}\mathit{p}}",
    },
    "Сила": {"Русский": r"Сила $\mathit{F}$", "Английский": r"Force $\mathit{F}$"},
    "Продольная сила": {
        "Русский": r"Продольная сила $\mathit{N}$",
        "Английский": r"Axial force $\mathit{N}$",
    },
    "Поперечная сила": {
        "Русский": r"Поперечная сила $\mathit{Q}$",
        "Английский": r"Shear force $\mathit{Q}$",
    },
    "Поперечная сила по Y": {
        "Русский": r"Поперечная сила $\mathit{Q}_{\mathit{y}}$",
        "Английский": r"Shear force $\mathit{Q}_{\mathit{y}}$",
    },
    "Поперечная сила по Z": {
        "Русский": r"Поперечная сила $\mathit{Q}_{\mathit{z}}$",
        "Английский": r"Shear force $\mathit{Q}_{\mathit{z}}$",
    },
    "Масса": {"Русский": r"Масса $\mathit{m}$", "Английский": r"Mass $\mathit{m}$"},
    "Напряжение": {
        "Русский": r"Напряжение \upsigma",
        "Английский": r"Stress \upsigma",
    },
    "Интенсивность напряжений": {
        "Русский": r"Интенсивность напряжений \upsigma_{\mathit{i}}",
        "Английский": r"Stress intensity \upsigma_{\mathit{i}}",
    },
    "Нормальное напряжение X": {
        "Русский": r"Нормальное напряжение \upsigma_{\mathit{x}}",
        "Английский": r"Normal stress \upsigma_{\mathit{x}}",
    },
    "Нормальное напряжение Y": {
        "Русский": r"Нормальное напряжение \upsigma_{\mathit{y}}",
        "Английский": r"Normal stress \upsigma_{\mathit{y}}",
    },
    "Нормальное напряжение Z": {
        "Русский": r"Нормальное напряжение \upsigma_{\mathit{z}}",
        "Английский": r"Normal stress \upsigma_{\mathit{z}}",
    },
    "Касательное напряжение XY": {
        "Русский": r"Касательное напряжение \uptau_{\mathit{x}\mathit{y}}",
        "Английский": r"Shear stress \uptau_{\mathit{x}\mathit{y}}",
    },
    "Касательное напряжение XZ": {
        "Русский": r"Касательное напряжение \uptau_{\mathit{x}\mathit{z}}",
        "Английский": r"Shear stress \uptau_{\mathit{x}\mathit{z}}",
    },
    "Касательное напряжение YX": {
        "Русский": r"Касательное напряжение \uptau_{\mathit{y}\mathit{x}}",
        "Английский": r"Shear stress \uptau_{\mathit{y}\mathit{x}}",
    },
    "Касательное напряжение YZ": {
        "Русский": r"Касательное напряжение \uptau_{\mathit{y}\mathit{z}}",
        "Английский": r"Shear stress \uptau_{\mathit{y}\mathit{z}}",
    },
    "Касательное напряжение ZX": {
        "Русский": r"Касательное напряжение \uptau_{\mathit{z}\mathit{x}}",
        "Английский": r"Shear stress \uptau_{\mathit{z}\mathit{x}}",
    },
    "Касательное напряжение ZY": {
        "Русский": r"Касательное напряжение \uptau_{\mathit{z}\mathit{y}}",
        "Английский": r"Shear stress \uptau_{\mathit{z}\mathit{y}}",
    },
    "Крутящий момент Mx": {
        "Русский": r"Крутящий момент $\mathit{M}_{\mathit{x}}$",
        "Английский": r"Torque $\mathit{M}_{\mathit{x}}$",
    },
    "Изгибающий момент Mx": {
        "Русский": r"Изгибающий момент $\mathit{M}_{\mathit{x}}$",
        "Английский": r"Bending moment $\mathit{M}_{\mathit{x}}$",
    },
    "Изгибающий момент Ms (My)": {
        "Русский": r"Изгибающий момент $\mathit{M}_{\mathit{s}} (\mathit{M}_{\mathit{y}})$",
        "Английский": r"Bending moment $\mathit{M}_{\mathit{s}} (\mathit{M}_{\mathit{y}})$",
    },
    "Изгибающий момент My": {
        "Русский": r"Изгибающий момент $\mathit{M}_{\mathit{y}}$",
        "Английский": r"Bending moment $\mathit{M}_{\mathit{y}}$",
    },
    "Изгибающий момент Mt (Mz)": {
        "Русский": r"Изгибающий момент $\mathit{M}_{\mathit{t}} (\mathit{M}_{\mathit{z}})$",
        "Английский": r"Bending moment $\mathit{M}_{\mathit{t}} (\mathit{M}_{\mathit{z}})$",
    },
    "Изгибающий момент Mz": {
        "Русский": r"Изгибающий момент $\mathit{M}_{\mathit{z}}$",
        "Английский": r"Bending moment $\mathit{M}_{\mathit{z}}$",
    },
    "Частота 1": {
        "Русский": r"Частота $\mathit{f}_{\mathit{1}}$",
        "Английский": r"Frequency $\mathit{f}_{\mathit{1}}$",
    },
    "Частота 2": {
        "Русский": r"Частота $\mathit{f}_{\mathit{2}}$",
        "Английский": r"Frequency $\mathit{f}_{\mathit{2}}$",
    },
    "Частота 3": {
        "Русский": r"Частота $\mathit{f}_{\mathit{3}}$",
        "Английский": r"Frequency $\mathit{f}_{\mathit{3}}$",
    },
}

# Символы для заголовков (копия словаря для осей)
TITLES_SYMBOLS = {key: value.copy() for key, value in TITLE_TRANSLATIONS.items()}

# Заголовки графиков — жирный курсив
TITLE_TRANSLATIONS_BOLD = {
    key: {lang: re.sub(r"(\\mathit{[^}]+}|\\up[a-zA-Z]+)", r"\\boldsymbol{\1}", text)
          for lang, text in value.items()}
    for key, value in TITLE_TRANSLATIONS.items()
}

# Подписи легенды графиков
LEGEND_TITLE_TRANSLATIONS = {
    "Нет": {"Русский": "Нет", "Английский": "No"},
    "№ Элементов": {"Русский": "№ Элементов", "Английский": "Element ID"},
    "№ Узлов": {"Русский": "№ Узлов", "Английский": "Node ID"},
    "Другое": {"Русский": "Другое", "Английский": "Other"},
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
    "UNITS_TRANSLATION",
    "TITLES_SYMBOLS",
    "TITLE_TRANSLATIONS",
    "TITLE_TRANSLATIONS_BOLD",
    "LEGEND_TITLE_TRANSLATIONS",
]
