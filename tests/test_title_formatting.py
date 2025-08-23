from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.mathtext import MathTextParser
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))
from tabs.title_utils import bold_math_symbols, format_title_bolditalic

parser = MathTextParser('agg')


@pytest.mark.parametrize(
    'title,xlabel,expected_tokens',
    [
        (
            'Момент M_x',
            'M_x',
            [r"\boldsymbol{M_x}"],
        ),
        (
            'Сумма My + Mz',
            'My + Mz',
            [r"\boldsymbol{My}", r"\boldsymbol{Mz}"],
        ),
        (
            'Заголовок $M_x + My$',
            '$M_x + My$',
            [r"\boldsymbol{M_x}", r"\boldsymbol{My}"],
        ),
    ],
)
def test_titles_bold_italic_math(title, xlabel, expected_tokens):
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    processed_title = bold_math_symbols(title)
    ax.set_title(processed_title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(xlabel)

    # Проверяем, что итоговые строки корректно парсятся
    parser.parse(ax.get_title())
    parser.parse(ax.get_xlabel())
    parser.parse(ax.get_ylabel())

    # В заголовке каждое указанное обозначение должно быть жирным
    for token in expected_tokens:
        assert token in ax.get_title()

    # Подписи осей не должны изменяться
    assert ax.get_xlabel() == xlabel
    assert ax.get_ylabel() == xlabel
    assert r"\boldsymbol" not in ax.get_xlabel()
    assert r"\boldsymbol" not in ax.get_ylabel()

    plt.close(fig)


def test_format_title_bolditalic_plain_text():
    assert (
        format_title_bolditalic("Заголовок")
        == r"\textbf{\textit{Заголовок}}"
    )


def test_format_title_bolditalic_with_math():
    result = format_title_bolditalic("Сумма $x+y$ равна")
    assert result == r"\textbf{\textit{Сумма }}$x+y$\textbf{\textit{ равна}}"


def test_format_title_bolditalic_only_math():
    assert format_title_bolditalic("$a+b$") == "$a+b$"
