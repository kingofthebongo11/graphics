"""UI package providing graphical editors."""

__all__ = ["PlotEditor"]


def __getattr__(name):
    if name == "PlotEditor":
        from .plot_editor import PlotEditor as _PlotEditor

        return _PlotEditor
    raise AttributeError(name)

