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

## Basic Usage
Start the application with:
```bash
python main.py
```
This opens the GUI where you can create and customize plots across multiple tabs.

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

The script [`examples/combined_labels.py`](examples/combined_labels.py) demonstrates how to mix bold designations in the title with italic or upright symbols in axis labels.

Run the example with:

```bash
python examples/combined_labels.py
```

You will get a plot where the title displays bold symbols such as $\boldsymbol{F_x}$ and $\boldsymbol{\upalpha}$, while the axis labels show `$\mathit{t}$` and `$\upalpha$` without bold formatting.
