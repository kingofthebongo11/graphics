"""Генерация команды для одной кривой."""

from __future__ import annotations

from typing import Any, Dict

from .naming import safe_name


def build_command(name: str, props: Dict[str, Any]) -> str:
    """Сформировать команду обработки одной кривой."""
    safe = safe_name(name)
    parts = [f"--{k}={v}" for k, v in sorted(props.items())]
    return " ".join([safe] + parts)


__all__ = ["build_command"]
