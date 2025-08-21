"""Модули вкладок графического интерфейса."""

# Импортируем функции создания вкладок лениво, чтобы избежать зависимости
# от графических библиотек при простом импорте пакета ``tabs``.

__all__ = ["create_tab1", "create_tab2", "create_tab3"]


def create_tab1(*args, **kwargs):  # pragma: no cover - простая обёртка
    from .tab1 import create_tab1 as _create_tab1

    return _create_tab1(*args, **kwargs)


def create_tab2(*args, **kwargs):  # pragma: no cover - простая обёртка
    from .tab2 import create_tab2 as _create_tab2

    return _create_tab2(*args, **kwargs)


def create_tab3(*args, **kwargs):  # pragma: no cover - простая обёртка
    from .tab3 import create_tab3 as _create_tab3

    return _create_tab3(*args, **kwargs)
