import sys
from pathlib import Path

import matplotlib.pyplot as plt

# Пример демонстрирует использование нового API ``split_signature``,
# возвращающего список сегментов для последующей отрисовки.
# Ensure project root is on sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from tabs.title_utils import split_signature


def join_segments(parts):
    """Объединить сегменты ``split_signature`` в строку."""

    return "".join(f"${frag}$" if is_latex else frag for frag, is_latex in parts)

x = [0, 1, 2, 3]
y = [0, 1, 4, 9]

fig, ax = plt.subplots()
ax.plot(x, y)

ax.set_title(join_segments(split_signature("Сила F_x при угле α", bold=True)))
ax.set_xlabel(join_segments(split_signature("Время t, с", bold=False)))
ax.set_ylabel(join_segments(split_signature("Угол α, рад", bold=False)))

plt.show()
