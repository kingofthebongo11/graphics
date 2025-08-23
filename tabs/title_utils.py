import re


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
        wrapped = f"\\boldsymbol{{{token}}}"
        if is_inside_math(s, start):
            return wrapped
        return f"${wrapped}$"

    return pattern.sub(repl, text)


def format_title_bolditalic(text: str) -> str:
    """Return ``text`` without LaTeX formatting.

    Ранее функция оборачивала текст в ``\textbf{\textit{...}}``, что
    приводило к наличию «сырых» LaTeX-команд в строке заголовка. Теперь
    выделение делается средствами Matplotlib (параметры ``fontweight`` и
    ``fontstyle``), поэтому функция просто возвращает исходную строку.
    """

    return text
