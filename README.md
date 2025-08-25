# Graphics Data Visualization Tool

## Project Purpose
This project provides a Tkinter-based graphical interface for creating and analyzing plots. Users can configure axes, preview graphs, and save results, all from an intuitive multi-tabbed window built with `matplotlib` and `openpyxl` for working with data files.

## Setup
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd graphics
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

## Dependency Installation
Install the required Python packages:
```bash
pip install matplotlib openpyxl numpy
```

If you plan to use LaTeX rendering for Greek letters and bold symbols,
install additional TeX packages (Debian/Ubuntu example):

```bash
sudo apt-get install texlive-latex-extra texlive-fonts-extra texlive-lang-cyrillic
```

## Basic Usage
Start the application with:
```bash
python main.py
```
This opens the GUI where you can create and customize plots across multiple tabs.

## Вкладка 4

В четвёртой вкладке можно управлять деревом расчётных кривых и путями файлов для отчёта. Поддерживаются следующие форматы:

- `.json` — сохранение и загрузка структуры дерева; файл содержит список
  узлов с именем пользователя, типом сущности и анализами с
  идентификаторами файлов;
- `.cfile` — генерация набора команд;
- `.docx` — сборка отчёта с кривыми.

При сканировании каталога кривых имена топ-папок не очищаются от числовых
префиксов. Поэтому каталоги `01-проект` и `02-проект` будут обработаны
независимо. Для подпапок анализов префикс по-прежнему отбрасывается
(`10-static` → `static`).

При генерации C-файла анализы могут быть пронумерованы. Числовой префикс
(`1-static`, `2-dynamic` и т.п.) сохраняется в пути, но для подписи
используется исходное название анализа.

Новый диалог добавления секций позволяет формировать вложенную структуру: кнопка «+» в любой строке открывает окно выбора типа секции, а у созданных элементов появляется собственная «+» для добавления дочерних уровней.

![Диалог добавления секций](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZAAAADICAIAAABJdyC1AAAIeklEQVR4nO3dP2ij9R/A8e9Tcna4wlUoUgidLXURhIpQ4bZeh2spV3Q5ORcpFJ10dT5wcRADDhXLgYtFjuINOsWjSLjdCuIghiJUChXEDsHGIT+Kv1OfekmfJ/k8eb2m+9JcnudJwjv5fvPnybrdbgKIYGLYOwDwXwkWEIZgAWEIFhCGYAFhCBYQhmABYQgWEIZgAWHU8v+cZVk5+wHQk/P1mwuClf+fAS5X/oskU0IgDMECwhAsIAzBAsIQLCAMwQLCECwgDMECwhAsIAzBAsIQLCCMi79LmCPLsrW1tVqt1ul09vb2UkqjMOx9+bG4ffPlShiWgYK1uLi4srKyubm5vb19dHR0dnY2CsOi9+0ybnagHwMFa25ubnJystVq1ev1er2eUhqRYdH7BgxHN1f+BW7dutXpdFZXV3v/HpFh0fuWf4sBg8hvTtbNXZHJsrwLbGxsLC8vz8zM1Gq1nZ2dlNIoDHd3dwvdt971A0XIb85A7xK22+3T09P19fV2u314eDgiw6L3bZBbDBjEQGtYjx49mp2dffjwYafTabVaKaURGRa9b8BQDBSs/OnkcI3yvgH98cFRIAzBAsIQLCAMwQLCECwgDMECwhAsIAzBAsIQLCCMgT7pni/LsuKunHL4wgAjpcBgJQ/34DzlMGpMCYEwBAsIQ7CAMIpdw6LCBlzhsr5JHwSL/vUdHcv59KfKU8KTk5PXX3/92rVrw94R4HKU9wqrtLOunj/t37x585VXXrl//35pxwgUqrxglXbW1fMtfvbZZ7Ozs++++25pxwgUqrxglXnW1Z7Z2dnSjo5z09PTJycnw94LqqnUNazbt2/fvXv3xo0bRQ+BShroRKoXXPX//9/Szrr62IlOPeH3Lf/e//tft7a2Dg4O9vf3l5aWFhYWGo1Gf9fMOCvwRKpPpOQTqVK+RqPRbDanpqaazWZOraBv5a1hlXnWVaCSypsSEs6TTgkv65oZZ6MyJQQYkGABYQgWEIZgAWEIFhCGYAFhCBYQhmABYQgWEIafSKZ/fumYkgkWffLdGspnSgiEIVhAGIIFhFHsGpZFWeASFRgsi7LA5TIlBMIQLCAMwQLCECwgDMECwhAsIAzBAsIQLCCMEf21Bh+RrwCfHObSjWiwkod7cJ5yKIIpIRCGYAFhCBYQxuiuYVFhA65wWd8cW4LFcPQdHcv548yU8J99/PHHL7/88vPPP//VV18Ne1+A/4nxCivLsrW1tVqt1ul09vb2UkoFDXtP+7/88svOzs7XX3/9/fffr6+vf/fdd0M8duBcjGAtLi6urKxsbm5ub28fHR2dnZ0VNOxt7vj4+M0335yYmJibmzs+Ph7usQPnYgRrbm5ucnKy1WrV6/V6vZ5SKm6YUpqfn5+fn08p7e7u3rx5c0gHPY6mp6dPTk6GvReMsG6uCy9QkMe2e+vWrU6ns7q62vt3ccO/bvSHH3547rnnjo6OSjrmasl/5PzbX69duzbgNRNd/v2bdXPfrMmyCy5QkMe2u7Gxsby8PDMzU6vVdnZ2UkoFDXd3d3tb/O23365fv/7hhx+++OKLpR99FeQ/cv7+162trYODg/39/aWlpYWFhUaj0d81E13+/RvjXcJ2u316erq+vt5utw8PD4sb9jbX7Xbv3Lnz9ttvq1VpGo1Gs9mcmppqNps5tWLMxVjDevTo0ezs7MOHDzudTqvVSikVN0wpffLJJ19++eXx8fFHH300NTX1xRdfDOvAgb+KMSUknCedEl7WNRNdFaaEAEmwgEAECwhDsIAwBAsIQ7CAMAQLCEOwgDAECwgjxldzqB6/dEwfBIsh8N0a+mNKCIQhWEAYggWEMbprWBZlgceMaLAsygJ/Z0oIhCFYQBiCBYQhWEAYggWEIVhAGIIFhCFYQBgj+sHRQfiIfAX45DD/qILBSh7uwXnK4d+YEgJhCBYQhmABYVRzDYsKG3CFy/pmaIJFPH1Hx3J+dKaEl+z3339/9dVXr1+//sILLzx48GDYuwOVkuU/WWXZBRcYQY/tc5Zla2trtVqt0+ns7e2llAoa9jb63nvvTUxMvPPOOz///PNLL730448/DuEmCC7/UTfIYzLi43nc5N9H1Z8SLi4urqysbG5ubm9vHx0dnZ2dFTTsbe6NN964evVqSunbb7+9cuXKUA8dqqb6wZqbm5ucnGy1WvV6vV6vp5SKG6aUnn766ZTSa6+99vnnn/dehVGO6enpk5OTYe8FxRqLNazbt2/fvXv3xo0bRQ/P3bt379NPP93Z2Sn0uGDcVH8Na2NjY3l5eWZmplar9QpS0HB3dzel9NZbb73//vu1Wu2PP/545plnjo+Ph3EbxPaka1hbW1sHBwf7+/tLS0sLCwuNRqO/a2YU5N9H1X+F1W63T09P19fX2+324eFhccPe5n799df79++nlL755ptnn312mEc+NhqNRrPZnJqaajabObWiAqr/CivLstXV1StXrpy/tVfQsLfRn3766c6dO2dnZ0899dQHH3wwPz8/jNsgtv7eJfwva1gRH8/j5oJ7v/LBIhwfaxhn4z4lBCpDsIAwBAsIQ7CAMAQLCEOwgDAECwhDsIAwBAsIo/o/L0P1+KXjsSVYBOO7NePMlBAIQ7CAMAQLCKOaa1gWZaGSKhgsi7JQVaaEQBiCBYQhWEAYggWEIVhAGIIFhCFYQBiCBYQhWEAYggWEIVhAGIIFhCFYQBiCBYQhWEAYggWEIVhAGIIFhCFYQBiCBYQhWEAYggWEIVhAGIIFhCFYQBiCBYQhWEAYggWEIVhAGIIFhCFYQBiCBYQhWEAYggWEIVhAGIIFhCFYQBiCBYRRu/ASWZaVsB8AF8q63e6w9wHgPzElBMIQLCAMwQLCECwgDMECwhAsIAzBAsIQLCCMPwE25qH7YqgP0gAAAABJRU5ErkJggg==)

Полученные файлы сохраняются в выбранные пользователем места:

- путь для `.json` задаётся в диалоге сохранения;
- `.cfile` и отчёт `.docx` сохраняются в каталоге, указанном в интерфейсе;
- если папка не выбрана, файлы создаются рядом с исходным проектом.

## Форматирование подписей и обозначений

Для заголовков графиков и подписей осей можно:

- использовать `format_signature` из модуля `tabs.title_utils`, который
  возвращает строку, готовую к передаче в Matplotlib;
- напрямую писать LaTeX‑строки (например, `r'Угол $\upalpha$'`).

Функция `format_signature` переводит латинские буквы в курсив
(`\mathit{}`), заменяет греческие символы на команды пакета `upgreek` и
корректно обрабатывает индексы/степени. Параметр `bold=True` делает
текстовые части жирными и оборачивает обозначения в `\boldsymbol{}`.
Сегментный API (`split_signature`/`join_segments`) устарел и не
рекомендуется к использованию.

Примеры:

- `format_signature('Момент M_x', bold=True)` → «\textbf{Момент }
  $\boldsymbol{\mathit{M}_{\mathit{x}}}$»
- `format_signature('Угол α', bold=False)` → «Угол $\upalpha$»
- `format_signature('Напряжение σ_{max}', bold=False)` →
  «Напряжение $\upsigma_{\mathit{max}}$»

### Пример использования с Matplotlib

```python
import matplotlib.pyplot as plt
from settings import configure_matplotlib
from tabs.title_utils import format_signature

configure_matplotlib()

fig, ax = plt.subplots()
ax.set_title(format_signature('Момент M_x', bold=True))
ax.set_xlabel(r'Угол $\upalpha$')
ax.set_ylabel(format_signature('Напряжение σ_{max}', bold=False))
plt.show()
```

## Axis Units
The axis dimension selectors support both SI units and engineering units based on kilogram-force and ton-force. For forces you can choose units like `kgf` and `tf`, while stress values may be expressed in standard units such as `Pa`, `kPa`, `MPa`, combinations of force (`N`, `kN`, `MN`) and area (`mm²`, `cm²`, `m²`), or engineering units like `kgf/mm²`, `kgf/cm²`, `kgf/m²`, `tf/cm²`, and `tf/m²`.

## Supported Curve File Formats
- Custom frequency analysis format.
- Plain text files where each line contains two numbers: X and Y.
- LS-Dyna curve files. The first lines are checked for markers like
  `LS-DYNA` or `*KEYWORD`; if they are absent, the user is notified that
  the file is not a valid LS-DYNA curve.
- Excel or CSV tables (first two columns are treated as X and Y).

## Example: Combined Labels

The script [`examples/combined_labels.py`](examples/combined_labels.py) demonstrates how to mix explicit LaTeX expressions in the title with auto‑formatted symbols in axis labels.

Run the example with:

```bash
python examples/combined_labels.py
```

You will get a plot where the title displays bold symbols such as $\boldsymbol{\mathit{F}_{\mathit{x}}}$ and $\boldsymbol{\upalpha}$, while the axis labels show `$\mathit{t}$` and `$\upalpha$` without bold formatting.
