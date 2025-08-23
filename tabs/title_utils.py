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
    """Wrap text parts of a title in bold italic while preserving math.

    The input string may contain segments enclosed in ``$`` which should
    remain untouched. All other parts are considered plain text and are
    wrapped with ``\textbf{\textit{...}}`` without adding extra ``$``
    around the whole title.
    """

    if not text:
        return text

    # Split into math and non-math segments. The regex keeps the math
    # delimiters so that the resulting list alternates between text and
    # math parts.
    segments = re.split(r"(\$[^$]*\$)", text)
    formatted: list[str] = []

    for segment in segments:
        if not segment:
            continue
        if segment.startswith("$") and segment.endswith("$"):
            # Math expression – keep as is.
            formatted.append(segment)
        else:
            # Plain text – wrap with bold italic commands.
            formatted.append(rf"\textbf{{\textit{{{segment}}}}}")

    return "".join(formatted)
