"""Запись набора команд в файл ``.cfile``."""

from __future__ import annotations

from pathlib import Path
import re


def write_cfile(commands: list[str], out_path: Path) -> Path:
    """Записать ``commands`` в файл ``out_path``.

    Кодировка CP1251 выбирается при наличии кириллических символов, иначе UTF-8.
    """
    out_path = Path(out_path).resolve()
    encoding = (
        "cp1251" if any(re.search(r"[А-Яа-яЁё]", cmd) for cmd in commands) else "utf-8"
    )
    try:
        with out_path.open("w", encoding=encoding, newline="\r\n") as file:
            file.write("\n".join(commands) + "\n")
    except OSError as exc:
        raise RuntimeError(f"Не удалось записать файл {out_path}") from exc
    return out_path


__all__ = ["write_cfile"]
