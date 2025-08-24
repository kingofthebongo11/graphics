import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.mathtext import MathTextParser
import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))
from tabs.title_utils import (
    bold_math_symbols,
    format_designation,
    format_signature,
    format_title_bolditalic,
)


parser = MathTextParser('agg')


@pytest.mark.parametrize(
    "title,xlabel,expected_tokens",
    [
        (
            "Момент M_x",
            "M_x",
            [r"\boldsymbol{\mathit{M}_{\mathit{x}}}"],
        ),
        (
            "Сумма M_x + M_y",
            "M_x + M_y",
            [
                r"\boldsymbol{\mathit{M}_{\mathit{x}}}",
                r"\boldsymbol{\mathit{M}_{\mathit{y}}}",
            ],
        ),
        (
            "Заголовок $M_x + M_y$",
            "$M_x + M_y$",
            [
                r"\boldsymbol{\mathit{M}_{\mathit{x}}}",
                r"\boldsymbol{\mathit{M}_{\mathit{y}}}",
            ],
        ),
    ],
)
def test_titles_bold_italic_math(title, xlabel, expected_tokens):
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    formatted_title = format_signature(title, bold=True)
    formatted_label = format_signature(xlabel, bold=False)
    ax.set_title(formatted_title)
    ax.set_xlabel(formatted_label)
    ax.set_ylabel(formatted_label)

    parser.parse(ax.get_title())
    parser.parse(ax.get_xlabel())
    parser.parse(ax.get_ylabel())

    for token in expected_tokens:
        assert token in ax.get_title()

    assert r"\textbf{" in ax.get_title()
    assert r"\textbf{" not in ax.get_xlabel()
    assert r"\textbf{" not in ax.get_ylabel()

    assert ax.get_xlabel() == formatted_label
    assert ax.get_ylabel() == formatted_label
    assert r"\boldsymbol" not in formatted_label

    plt.close(fig)


@pytest.mark.parametrize(
    "token,expected_title,expected_label",
    [
        ("σ_x", r"\boldsymbol{\upsigma_{\mathit{x}}}", r"\upsigma_{\mathit{x}}"),
        ("λ_i", r"\boldsymbol{\uplambda_{\mathit{i}}}", r"\uplambda_{\mathit{i}}"),
    ],
)
def test_greek_letters_with_latin_indices(token, expected_title, expected_label):
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    formatted_title = format_signature(f"Параметр {token}", bold=True)
    formatted_label = format_signature(token, bold=False)
    ax.set_title(formatted_title)
    ax.set_xlabel(formatted_label)
    ax.set_ylabel(formatted_label)

    for item in (ax.get_title(), ax.get_xlabel(), ax.get_ylabel()):
        sanitized = item.replace("\\upsigma", "\\sigma").replace("\\uplambda", "\\lambda")
        parser.parse(sanitized)

    assert expected_title in ax.get_title()
    assert ax.get_xlabel() == f"${expected_label}$"
    assert ax.get_ylabel() == f"${expected_label}$"
    assert r"\boldsymbol" not in ax.get_xlabel()

    plt.close(fig)


@pytest.mark.parametrize(
    "token,bold,expected",
    [
        ("σ_x^2", True, r"\boldsymbol{\upsigma_{\mathit{x}}^{2}}"),
        ("σ_x^2", False, r"\upsigma_{\mathit{x}}^{2}"),
        ("λ_i^j", True, r"\boldsymbol{\uplambda_{\mathit{i}}^{\mathit{j}}}"),
        ("λ_i^j", False, r"\uplambda_{\mathit{i}}^{\mathit{j}}"),
    ],
)
def test_format_signature_with_super_and_sub(token, bold, expected):
    formatted = format_signature(token, bold=bold)
    sanitized = formatted.replace("\\upsigma", "\\sigma").replace("\\uplambda", "\\lambda")
    parser.parse(sanitized)
    assert formatted == f"${expected}$"


def test_format_signature_bold_text_only():
    formatted = format_signature("Просто текст", bold=True)
    parser.parse(formatted)
    assert formatted == r"\textbf{Просто текст}"


@pytest.mark.parametrize(
    "token,in_math,expected",
    [
        ("M_x", True, r"\boldsymbol{M_x}"),
        ("M_x", False, r"$\boldsymbol{M_x}$"),
        (r"\mathit{t}", True, r"\boldsymbol{\mathit{t}}"),
        (r"\mathit{t}", False, r"$\boldsymbol{\mathit{t}}$"),
    ],
)
def test_format_designation(token, in_math, expected):
    assert format_designation(token, in_math) == expected


@pytest.mark.parametrize(
    "text,expected_calls",
    [
        ("M_x", [("M_x", False)]),
        (r"\upalpha", [(r"\upalpha", False)]),
    ],
)
def test_bold_math_symbols_uses_format_designation(monkeypatch, text, expected_calls):
    calls = []

    def fake(token, in_math):
        calls.append((token, in_math))
        return token

    monkeypatch.setattr("tabs.title_utils.format_designation", fake)
    bold_math_symbols(text)
    assert calls == expected_calls


@pytest.mark.parametrize(
    "text,expected",
    [
        (r"\upalpha", r"$\boldsymbol{\upalpha}$"),
        (r"$\upbeta$", r"$\boldsymbol{\upbeta}$"),
    ],
)
def test_bold_math_symbols_handles_upgreek(text, expected):
    result = bold_math_symbols(text)
    sanitized = result.replace("\\upalpha", "\\alpha").replace(
        "\\upbeta", "\\beta"
    )
    parser.parse(sanitized)
    assert result == expected


def test_format_title_bolditalic_plain_text():
    assert format_title_bolditalic("Заголовок") == "Заголовок"


def test_format_title_bolditalic_with_math():
    result = format_title_bolditalic("Сумма $x+y$ равна")
    assert result == "Сумма $x+y$ равна"


def test_format_title_bolditalic_only_math():
    assert format_title_bolditalic("$a+b$") == "$a+b$"


def test_axis_labels_combined_format():
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    x_label = format_signature("Время t, с", bold=False)
    y_label = format_signature("Угол α, рад", bold=False)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    assert ax.get_xlabel() == "Время $\\mathit{t}$, с"
    assert ax.get_ylabel() == "Угол $\\upalpha$, рад"
    parser.parse(ax.get_xlabel())
    assert "\\boldsymbol" not in ax.get_xlabel()
    assert "\\boldsymbol" not in ax.get_ylabel()

    plt.close(fig)
