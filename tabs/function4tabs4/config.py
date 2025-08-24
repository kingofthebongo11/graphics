"""Конфигурация путей для четвёртой вкладки."""

from __future__ import annotations

from pathlib import Path

from .tree_schema import DEFAULT_TOPFOLDER

CFILE_NAME = ".cfile"
CURVES_DIR = Path(DEFAULT_TOPFOLDER)


def cfile_path(base: str | Path) -> Path:
    """Получить путь к ``.cfile`` относительно ``base``."""
    return Path(base) / CFILE_NAME


__all__ = ["CFILE_NAME", "CURVES_DIR", "cfile_path"]
