import re


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
