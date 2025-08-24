"""Кодирование и декодирование пути верхней папки."""

from __future__ import annotations

import base64
from pathlib import Path


def encode_topfolder(path: Path) -> str:
    """Закодировать путь папки в безопасную строку."""
    return base64.urlsafe_b64encode(str(path).encode("utf-8")).decode("ascii")


def decode_topfolder(token: str) -> Path:
    """Восстановить путь папки из строки."""
    return Path(base64.urlsafe_b64decode(token.encode("ascii")).decode("utf-8"))


__all__ = ["encode_topfolder", "decode_topfolder"]
