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

## Supported Curve File Formats
- Custom frequency analysis format.
- Plain text files where each line contains two numbers: X and Y.
- LS-Dyna curve files.
- Excel or CSV tables (first two columns are treated as X and Y).
