import sys
from pathlib import Path

import matplotlib.pyplot as plt

# Пример комбинирует явные LaTeX-строки в заголовке с
# автоматическим форматированием подписей осей через ``format_signature``.
# Ensure project root is on sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from tabs.title_utils import format_signature

x = [0, 1, 2, 3]
y = [0, 1, 4, 9]

fig, ax = plt.subplots()
ax.plot(x, y)

ax.set_title(r"Сила $\boldsymbol{\mathit{F}_{\mathit{x}}}$ при угле $\boldsymbol{\upalpha}$")
ax.set_xlabel(format_signature("Время t, с", bold=False))
ax.set_ylabel(format_signature("Угол α, рад", bold=False))

plt.show()
