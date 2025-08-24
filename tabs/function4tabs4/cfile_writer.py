"""Запись набора команд в файл ``.cfile``."""

from __future__ import annotations

from pathlib import Path
import os


def write_cfile(commands: list[str], out_path: str | os.PathLike[str] | bytes) -> Path:
    """Записать ``commands`` в файл ``out_path``."""
    dest = Path(os.fsdecode(out_path))
    try:
        with dest.open("w", encoding="utf-8", newline="\r\n") as file:
            file.write("\n".join(commands) + "\n")
    except OSError as exc:
        raise RuntimeError(f"Не удалось записать файл {dest}") from exc
    return dest


__all__ = ["write_cfile"]
