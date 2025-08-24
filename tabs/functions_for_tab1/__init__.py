"""Пакет с функциями для первой вкладки.

Импортируется без немедленной загрузки тяжёлых зависимостей (например, PyQt),
поэтому реальные функции подтягиваются лениво при первом обращении."""

__all__ = ["update_curves", "generate_graph", "save_file", "last_graph"]


def update_curves(*args, **kwargs):  # pragma: no cover - простая обёртка
    from .curves import update_curves as _update_curves

    return _update_curves(*args, **kwargs)


def generate_graph(*args, **kwargs):  # pragma: no cover - простая обёртка
    from .plotting import generate_graph as _generate_graph

    return _generate_graph(*args, **kwargs)


def save_file(*args, **kwargs):  # pragma: no cover - простая обёртка
    from .plotting import save_file as _save_file

    return _save_file(*args, **kwargs)


def last_graph(*args, **kwargs):  # pragma: no cover - простая обёртка
    from .plotting import last_graph as _last_graph

    return _last_graph(*args, **kwargs)
