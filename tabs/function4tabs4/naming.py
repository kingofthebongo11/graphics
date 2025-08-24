"""Утилиты для безопасных имён файлов и путей."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

_SAFE_CHARS_RE = re.compile(r"[^A-Za-z0-9_.\-А-Яа-яЁё]")


def safe_name(name: str, replacement: str = "_") -> str:
    """Преобразовать строку в безопасное имя файла."""
    cleaned = _SAFE_CHARS_RE.sub(replacement, name).strip()
    return cleaned or "untitled"


def join_path(base: Path, *parts: Iterable[str]) -> Path:
    """Собрать путь из частей, делая каждую часть безопасной."""
    safe_parts = [safe_name(str(p)) for p in parts]
    return base.joinpath(*safe_parts)


__all__ = ["safe_name", "join_path"]
