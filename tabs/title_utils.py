import re


# Mapping of Greek letters to commands from the ``upgreek`` package.
_GREEK_MAP = {
    "α": "upalpha",
    "β": "upbeta",
    "γ": "upgamma",
    "δ": "updelta",
    "ε": "upepsilon",
    "ζ": "upzeta",
    "η": "upeta",
    "θ": "uptheta",
    "ι": "upiota",
    "κ": "upkappa",
    "λ": "uplambda",
    "μ": "upmu",
    "ν": "upnu",
    "ξ": "upxi",
    "π": "uppi",
    "ρ": "uprho",
    "σ": "upsigma",
    "ς": "upvarsigma",
    "τ": "uptau",
    "υ": "upupsilon",
    "φ": "upphi",
    "χ": "upchi",
    "ψ": "uppsi",
    "ω": "upomega",
    "Α": "Upalpha",
    "Β": "Upbeta",
    "Γ": "Upgamma",
    "Δ": "Updelta",
    "Ε": "Upepsilon",
    "Ζ": "Upzeta",
    "Η": "Upeta",
    "Θ": "Uptheta",
    "Ι": "Upiota",
    "Κ": "Upkappa",
    "Λ": "Uplambda",
    "Μ": "Upmu",
    "Ν": "Upnu",
    "Ξ": "Upxi",
    "Π": "Uppi",
    "Ρ": "Uprho",
    "Σ": "Upsigma",
    "Τ": "Uptau",
    "Υ": "Upupsilon",
    "Φ": "Upphi",
    "Χ": "Upchi",
    "Ψ": "Uppsi",
    "Ω": "Upomega",
}


_LETTER_RANGE = r"A-Za-z\u0370-\u03FF"
_INDEX_BODY = rf"(?:{{[^}}]+}}|[{_LETTER_RANGE}0-9]+)"
_TOKEN_PATTERN = re.compile(
    rf"(?<![{_LETTER_RANGE}0-9])"
    rf"([{_LETTER_RANGE}])"
    rf"(?:_({_INDEX_BODY}))?"
    rf"(?:\^({_INDEX_BODY}))?"
    rf"(?![{_LETTER_RANGE}0-9])"
)


def _format_component(token: str) -> str:
    """Преобразовать строку индекса или показателя степени."""

    result = []
    for ch in token:
        if ch in _GREEK_MAP:
            result.append(f"\\{_GREEK_MAP[ch]}")
        elif ch.isalpha() and ch.isascii():
            result.append(f"\\mathit{{{ch}}}")
        else:
            result.append(ch)
    return "".join(result)


def _format_signature_impl(text: str, bold: bool) -> str:
    """Internal helper implementing signature formatting."""

    def is_inside_math(s: str, pos: int) -> bool:
        count = 0
        escaped = False
        for ch in s[:pos]:
            if escaped:
                escaped = False
                continue
            if ch == "\\":
                escaped = True
            elif ch == "$":
                count += 1
        return count % 2 == 1

    def repl(match: re.Match) -> str:
        base, sub, sup = match.groups()

        base_fmt = _format_component(base)

        formatted = base_fmt
        if sub:
            sub_token = sub[1:-1] if sub.startswith("{") else sub
            formatted += f"_{{{_format_component(sub_token)}}}"
        if sup:
            sup_token = sup[1:-1] if sup.startswith("{") else sup
            formatted += f"^{{{_format_component(sup_token)}}}"

        if bold:
            formatted = f"\\boldsymbol{{{formatted}}}"

        return formatted if is_inside_math(match.string, match.start()) else f"${formatted}$"

    result = _TOKEN_PATTERN.sub(repl, text)
    if bold:
        parts = re.split(r"(\$[^$]*\$)", result)
        result = "".join(
            f"\\textbf{{{part}}}" if part and not part.startswith("$") else part
            for part in parts
            if part
        )
    return result


def split_signature(text: str, bold: bool) -> list[tuple[str, bool]]:
    """Разбить ``text`` на сегменты ``(фрагмент, is_latex)``.

    Латинские и греческие обозначения преобразуются в LaTeX так же, как в
    :func:`format_signature`. Сегменты с ``is_latex=True`` предназначены для
    отображения в математическом режиме.

    Пример
    -------
    >>> split_signature('Угол α', bold=False)
    [('Угол ', False), ('\\upalpha', True)]
    """

    formatted = _format_signature_impl(text, bold)
    parts = re.split(r"(\$[^$]*\$)", formatted)
    segments: list[tuple[str, bool]] = []
    for part in parts:
        if not part:
            continue
        if part.startswith("$") and part.endswith("$"):
            segments.append((part[1:-1], True))
        else:
            segments.append((part, False))
    return segments


def format_signature(text: str, *, bold: bool) -> str:
    r"""Вернуть ``text`` с оформленными обозначениями.

    Функция является обёрткой над :func:`split_signature`, объединяющей
    полученные сегменты в одну строку с ``$`` вокруг математических частей.
    """

    segments = split_signature(text, bold)
    return "".join(
        f"${frag}$" if is_latex else frag for frag, is_latex in segments
    )


def format_designation(token: str, in_math: bool) -> str:
    """Wrap ``token`` in ``\boldsymbol{}`` and add ``$`` if needed.

    Parameters
    ----------
    token:
        LaTeX token representing a designation (e.g. ``M_x`` or
        ``\mathit{t}``).
    in_math:
        ``True`` if ``token`` already resides inside math mode, ``False``
        otherwise.
    """

    wrapped = f"\\boldsymbol{{{token}}}"
    return wrapped if in_math else f"${wrapped}$"


def bold_math_symbols(text: str) -> str:
    r"""Wrap math expressions ``\mathit{...}`` and ``M_x``, ``My``, ``Mz``
    with ``$\\boldsymbol{...}$`` or ``$\\boldsymbol{\\mathit{...}}$``.

    The function skips parts that are already bold (``\boldsymbol`` or
    ``\mathbfit``) and respects existing math mode delimited by ``$``.
    """

    pattern = re.compile(r"\\mathit\{[^}]+\}|\bM(?:_?[xyz])\b")

    def is_inside_math(s: str, pos: int) -> bool:
        count = 0
        escaped = False
        for ch in s[:pos]:
            if escaped:
                escaped = False
                continue
            if ch == "\\":
                escaped = True
            elif ch == "$":
                count += 1
        return count % 2 == 1

    def already_bold(s: str, start: int) -> bool:
        prefix = s[:start]
        return bool(
            re.search(r"(\\boldsymbol|\\mathbfit)\s*\{\s*$", prefix)
        )

    def repl(match: re.Match) -> str:
        s = match.string
        start = match.start()
        token = match.group(0)
        if already_bold(s, start):
            return token
        return format_designation(token, is_inside_math(s, start))

    return pattern.sub(repl, text)


def format_title_bolditalic(text: str) -> str:
    """Return ``text`` without LaTeX formatting.

    Ранее функция оборачивала текст в ``\textbf{\textit{...}}``, что
    приводило к наличию «сырых» LaTeX-команд в строке заголовка. Теперь
    выделение делается средствами Matplotlib (параметры ``fontweight`` и
    ``fontstyle``), поэтому функция просто возвращает исходную строку.
    """

    return text
