from matplotlib.mathtext import MathTextParser

import pytest

from tabs.constants import TITLE_TRANSLATIONS


parser = MathTextParser("agg")


def test_all_titles_mathtext_parsable():
    for quantity, translations in TITLE_TRANSLATIONS.items():
        for lang, text in translations.items():
            try:
                parser.parse(text)
            except Exception as exc:  # pragma: no cover - ошибка приводит к падению теста
                pytest.fail(f"Ошибка парсинга '{quantity}' ({lang}): {exc}")
