# 📊 `dva-lab` — Data Visualization & Analytics Laboratory Library

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Jupyter Compatible](https://img.shields.io/badge/Jupyter-Notebook%20%7C%20Lab%20%7C%20Colab-orange.svg)](https://jupyter.org/)
[![Tests](https://img.shields.io/badge/tests-59%20passed-brightgreen.svg)]()

**`dva-lab`** is an installable, self-contained Python library engineered for university students and educators. It enables students to retrieve, display, study, and execute all 12 Data Visualization and Analytics (DVA) laboratory experiments directly inside **Jupyter Notebook**, **JupyterLab**, or **Google Colab**.

The package stores the complete, authoritative source code, schemas, and datasets locally within the library. It does not depend on fetching code from the internet during runtime.

---

## 📑 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
  - [Google Colab & Jupyter Notebook](#google-colab--jupyter-notebook)
  - [Local Development & Pip](#local-development--pip)
  - [Optional Dependency Sets](#optional-dependency-sets)
- [Quick Start](#-quick-start)
- [Complete Experiment Catalog](#-complete-experiment-catalog)
- [Public API Reference](#-public-api-reference)
- [Experiment Execution Guidelines](#-experiment-execution-guidelines)
  - [SQL & OLAP Experiments (Exp 1 & 2)](#1-sql--olap-experiments-experiments-1-and-2)
  - [Python Plotting Experiments (Exp 3 to 9)](#2-python-plotting-experiments-experiments-3-to-9)
  - [Power BI & DAX Experiments (Exp 10 to 12)](#3-power-bi--dax-experiments-experiments-10-to-12)
- [Updating & Uninstalling](#-updating--uninstalling)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Features

- **Jupyter-Native Experience**: Seamless inline rendering of Matplotlib/Seaborn plots and rich HTML/Markdown experiment guides.
- **Self-Contained & Deterministic**: Bundles all source code, SQL definitions, Power BI DAX expressions, and sample datasets (`sales_data.csv`).
- **Reproducible Seeds**: Synthetic distributions use fixed random seeds (`seed=0`) matching laboratory manual benchmarks.
- **Safe & Non-Destructive**: Never connects to an unknown database without explicit authorization and never attempts mock Power BI execution.
- **Convenient Shortcuts**: Direct function handles (`dva_lab.exp1()` through `dva_lab.exp12()`) for fast classroom access.
- **Lightweight Core**: Base install contains zero compulsory heavy dependencies with lazy imports for plotting engines.

---

## 📦 Installation

### Google Colab & Jupyter Notebook

Paste and execute directly in a notebook cell:

```python
# Install directly from GitHub with visualization dependencies
%pip install "git+https://github.com/AnandChowdari/dva-lab.git#egg=dva-lab[viz]"
```

*Note: Replace `AnandChowdari` with your GitHub username or organization repository URL.*

### Local Development & Pip

#### Windows (PowerShell):
```powershell
git clone https://github.com/AnandChowdari/dva-lab.git
cd dva-lab
pip install -e .[viz]
```

#### macOS / Linux:
```bash
git clone https://github.com/AnandChowdari/dva-lab.git
cd dva-lab
pip install -e ".[viz]"
```

### Optional Dependency Sets

| Group | Install Command | Included Packages | Purpose |
|---|---|---|---|
| **Base** | `pip install git+https://github.com/AnandChowdari/dva-lab.git` | Pure Python core | Code retrieval, schema inspection, CLI list |
| **`viz`** | `pip install "dva-lab[viz]"` | `matplotlib`, `numpy`, `seaborn`, `scipy`, `statsmodels` | Plotting experiments (Exp 3–9) |
| **`full`** | `pip install "dva-lab[full]"` | `viz` + `pandas` + `ipython` | Full workbook with simulations & dataset tools |
| **`test`** | `pip install "dva-lab[test]"` | `viz` + `pandas` + `pytest` | Running the test suite locally |

---

## ⚡ Quick Start

```python
import dva_lab

# 1. Discover all registered experiments
dva_lab.list_experiments()

# 2. Display formatted Markdown manual for Experiment 3
dva_lab.show_experiment(3)

# 3. Retrieve raw source code as a string
code = dva_lab.get_code(3)
print(code)

# 4. Execute experiment and render plots inline
dva_lab.exp3()
```

---

## 📚 Complete Experiment Catalog

| # | Title | Category | Methodology / Tools | Focus |
|:---:|---|---|---|---|
| **1** | OLAP Operations Using Materialized Views | `OLAP & SQL` | PostgreSQL 12+, CUBE | Materialized view, Roll Up, Slice, Dice, Pivot |
| **2** | OLAP Operations Based on Star Schema | `OLAP & SQL` | PostgreSQL 12+, CUBE | Fact & dimension joins, Drill Down, Hierarchy |
| **3** | Vertical and Horizontal Bar Charts | `Python Visualization` | Matplotlib, NumPy | `plt.bar`, `plt.barh`, categorical comparison |
| **4** | Grouped and Stacked Bar Charts | `Python Visualization` | Matplotlib, NumPy | Positional offsets, stacked `bottom` vectors |
| **5** | Single & Multiple Variable Histograms | `Python Visualization` | Matplotlib, NumPy | Bin frequency, alpha transparency, normal distributions |
| **6** | Single & Multiple Variable Density Plots | `Python Visualization` | Seaborn, Matplotlib | Kernel Density Estimation (`sns.kdeplot`), area fills |
| **7** | Empirical Cumulative Distribution Function | `Python Visualization` | Statsmodels, Matplotlib | Non-parametric ECDF step function (`sm.distributions.ECDF`) |
| **8** | Q-Q Plot to Compare Datasets | `Python Visualization` | SciPy, Matplotlib | Normal probability quantiles (`stats.probplot`) |
| **9** | Scatter Plot Using Sample Data | `Python Visualization` | Matplotlib, NumPy | Bivariate scatter points, alpha blending, correlation |
| **10** | Power BI Sales Data Visualization | `Power BI` | Power BI Desktop, CSV | Column, Pie, Line, Card, Slicer dashboard |
| **11** | Power BI Calculations & DAX Measures | `Power BI` | DAX, Power BI Desktop | `Total Cost`, `Profit`, `CALCULATE`, `ALL`, percentages |
| **12** | Power BI Conditional & Logical Analysis | `Power BI` | DAX, Power BI Desktop | `IF`, `AND`, `OR`, `COUNTROWS`, dynamic sales tiers |

---

## 🛠 Public API Reference

### `dva_lab.list_experiments()`
Returns a rich `ExperimentList` containing all 12 experiments.
- **In Jupyter**: Automatically renders a styled HTML table with badges.
- **In Terminal**: Displays an aligned text summary.
- **Convert to DataFrame**: `dva_lab.list_experiments().to_dataframe()`

### `dva_lab.show_experiment(number: int)`
Displays the complete laboratory manual for the experiment:
- Experiment Aim
- Theoretical Concept & Pedagogical Context
- Complete, Corrected Input Code
- Expected Visual Output or Result Table
- Result Statement
- Execution Notes & Errata

### `dva_lab.get_code(number: int) -> str`
Returns the exact, clean source code string for inspection or programmatic export:
```python
with open("exp03.py", "w") as f:
    f.write(dva_lab.get_code(3))
```

### `dva_lab.run_experiment(number: int, **kwargs)`
Executes the specified experiment:
- For Python experiments (3–9): Renders plots inline.
- Optional arguments:
  - `show=True`: Call `plt.show()` inline.
  - `side_by_side=True`: For multi-plot experiments (3, 4, 5, 6), combines subplots horizontally.

### Convenience Shortcuts (`dva_lab.exp1()` ... `dva_lab.exp12()`)
One-line helper functions to immediately access any experiment:
```python
dva_lab.exp1()   # Shows PostgreSQL SQL queries and setup guide
dva_lab.exp3()   # Plots vertical and horizontal bar charts
dva_lab.exp10()  # Shows Power BI visual setup guide and previews dataset
```

### `dva_lab.load_sales_data() -> pd.DataFrame`
Loads and returns the authoritative 10-record `sales_data.csv` used in Experiments 10–12 as a pandas DataFrame:
```python
df = dva_lab.load_sales_data()
print(df.head())
```

### `dva_lab.about()` / `dva_lab.help()`
Prints library version, repository information, and API guide.

---

## 🔬 Experiment Execution Guidelines

### 1. SQL & OLAP Experiments (Experiments 1 and 2)
Experiments 1 and 2 define complete PostgreSQL scripts including DDL (`CREATE TABLE`), sample `INSERT` records, materialized views with `GROUP BY CUBE`, and OLAP queries (`Roll Up`, `Drill Down`, `Slice`, `Dice`, `Pivot`).

- **Safety Guarantee**: Calling `dva_lab.run_experiment(1)` or `dva_lab.exp1()` **never** executes SQL against an unconfigured server.
- **Live Execution**: If you have an active PostgreSQL connection (e.g. `psycopg2` or `SQLAlchemy`), pass it explicitly:
  ```python
  dva_lab.run_experiment(1, connection=your_db_connection)
  ```

### 2. Python Plotting Experiments (Experiments 3 to 9)
All Python experiments run locally using Matplotlib, Seaborn, Statsmodels, and SciPy.
- Fully compatible with Jupyter `%matplotlib inline` backend.
- Deterministic synthetic data generated with `np.random.seed(0)`.
- Support individual sequential plots or combined views (`side_by_side=True`).

### 3. Power BI & DAX Experiments (Experiments 10 to 12)
Power BI Desktop reports are interactive Windows visual applications. `dva-lab` provides:
- Complete step-by-step instructions for fields, axes, and visual types.
- Exact DAX measures and calculated column formulas.
- Bundled CSV data via `dva_lab.load_sales_data()`.
- Built-in Python validation simulation reproducing the DAX calculations directly in pandas:
  ```python
  from dva_lab.experiments.exp11_powerbi_dax import simulate_in_python
  print(simulate_in_python())
  ```

---

## 🔄 Updating & Uninstalling

### Update to Latest Version
```python
%pip install --upgrade --force-reinstall git+https://github.com/AnandChowdari/dva-lab.git
```

### Uninstall
```python
%pip uninstall dva-lab -y
```

---

## 🧪 Testing

The library comes with a complete test suite covering 100% of registry lookups, code snippets, headless plotting rendering, and DAX simulations:

```bash
pytest -v
```

---

## 🤝 Contributing

1. Fork the repository on GitHub.
2. Clone your fork and create a feature branch (`git checkout -b feature/new-experiment`).
3. Add or update experiment files in `src/dva_lab/experiments/`.
4. Ensure all tests pass: `pytest`.
5. Submit a Pull Request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
