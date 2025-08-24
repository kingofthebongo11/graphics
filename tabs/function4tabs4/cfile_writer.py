"""Запись набора команд в файл ``.cfile``."""

from __future__ import annotations

from pathlib import Path


def write_cfile(commands: list[str], out_path: Path) -> Path:
    """Записать ``commands`` в файл ``out_path``."""
    out_path = Path(out_path).resolve()
    try:
        with out_path.open("w", encoding="utf-8", newline="\r\n") as file:
            file.write("\n".join(commands) + "\n")
    except OSError as exc:
        raise RuntimeError(f"Не удалось записать файл {out_path}") from exc
    return out_path


__all__ = ["write_cfile"]
