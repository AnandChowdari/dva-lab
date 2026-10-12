# 📊 `dva-lab` — Data Visualization & Analytics Laboratory Library

[![PyPI Version](https://img.shields.io/pypi/v/dva-lab.svg)](https://pypi.org/project/dva-lab/)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Jupyter Compatible](https://img.shields.io/badge/Jupyter-Notebook%20%7C%20Lab%20%7C%20Colab-orange.svg)](https://jupyter.org/)
[![Tests](https://img.shields.io/badge/tests-74%20passed-brightgreen.svg)]()

> **Cloud-synchronized, personal code library and execution engine for Data Visualization and Analytics (DVA) experiments.**  
> Retrieve, study, and run all 12 DVA laboratory experiments seamlessly in **Jupyter Notebook**, **JupyterLab**, **Google Colab**, or the **Terminal** over HTTPS with `pip install dva-lab`.

---

## 📑 Table of Contents

- [1. Overview & Architecture](#1-overview--architecture)
- [2. Installation](#2-installation)
- [3. Quick Start Workflow](#3-quick-start-workflow)
- [4. Remote GitHub Cloud Code Storage](#4-remote-github-cloud-code-storage)
- [5. Jupyter Notebook & IPython Magics](#5-jupyter-notebook--ipython-magics)
- [6. Command-Line Interface (CLI)](#6-command-line-interface-cli)
- [7. Complete 12-Experiment Catalog](#7-complete-12-experiment-catalog)
- [8. Execution Guidelines](#8-execution-guidelines)
  - [SQL / OLAP Experiments (1 & 2)](#sql--olap-experiments-1--2)
  - [Python Visualization Experiments (3 to 9)](#python-visualization-experiments-3-to-9)
  - [Power BI & DAX Experiments (10 to 12)](#power-bi--dax-experiments-10-to-12)
- [9. Testing in a Clean Virtual Environment](#9-testing-in-a-clean-virtual-environment)
- [10. Publishing Guide (TestPyPI & Production PyPI)](#10-publishing-guide-testpypi--production-pypi)
- [11. License](#11-license)

---

## 1. Overview & Architecture

`dva-lab` decouples laboratory code management from local machine environments:
- **Zero Local Git Required**: Retrieves experiment files and metadata from GitHub over standard HTTPS.
- **Offline Resilient & Self-Contained**: Automatically falls back to bundled authoritative experiment definitions and datasets (`sales_data.csv`) if disconnected or offline.
- **Smart Caching**: In-memory caching and local disk caching (`~/.dva_lab/cache`) prevent redundant network requests and avoid API rate limits.
- **Direct Jupyter Cell Injection**: `%load_code <id>` replaces active notebook cell contents with clean code ready to run or edit.
- **Environment Aware**: Transparently differentiates standalone Python plots from external PostgreSQL database requirements and Microsoft Power BI Desktop reports.

```text
                    ┌──────────────────────────────────────────────┐
                    │               GitHub Storage                 │
                    │      github.com/AnandChowdari/dva-lab        │
                    │                                              │
                    │  codes/                                      │
                    │    ├── 01_olap.sql                           │
                    │    ├── 02_star_schema.sql                    │
                    │    ├── 03_bar_charts.py                      │
                    │    └── ... (12 experiments)                  │
                    │  index.json (Catalog metadata)               │
                    └──────────────────────┬───────────────────────┘
                                           │
                                           │ HTTPS (raw.githubusercontent.com)
                                           ▼
                    ┌──────────────────────────────────────────────┐
                    │             dva-lab (Package)                │
                    │           Import: import dva_lab             │
                    │     (with intelligent offline fallback)      │
                    └──────────────────────┬───────────────────────┘
                                           │
                                     pip install
                                           │
                ┌──────────────────────────┼──────────────────────────┐
                ▼                          ▼                          ▼
          Google Colab              Jupyter Notebook           Command Line (CLI)
      %pip install dva-lab        import dva_lab as dva        dva-lab get 3 -o exp3.py
      dva.run_experiment(3)       %load_code 3                 dva-lab list
```

---

## 2. Installation

### From PyPI (Production)
```bash
pip install dva-lab
```

In Jupyter Notebook or Google Colab:
```python
%pip install dva-lab
```

### From TestPyPI (Staging)
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dva-lab
```

### From Source (Local Development)
```bash
git clone https://github.com/AnandChowdari/dva-lab.git
cd dva-lab
pip install -e .
```

---

## 3. Quick Start Workflow

```python
from dva_lab import configure, list_experiments, get_code, show_experiment, run_experiment

# 1. Configure the remote GitHub repository (defaults to AnandChowdari/dva-lab)
configure(username="AnandChowdari", repository="dva-lab")

# 2. List all 12 experiments in an interactive table
list_experiments()

# 3. Retrieve raw source code over HTTPS without Git
code = get_code(1)
print(code)

# 4. Display complete laboratory manual with theoretical concept & notes
show_experiment(1)

# 5. Run Python visualization experiment directly inline
run_experiment(3)
```

---

## 4. Remote GitHub Cloud Code Storage

You can point `dva-lab` to your own GitHub fork or customized code repository:

```python
import dva_lab

# Configure dynamically in Python
dva_lab.configure(
    username="YOUR_GITHUB_USERNAME",
    repository="YOUR_DVA_REPOSITORY",
    branch="main",          # Optional, defaults to "main"
    timeout=10.0,           # Optional network timeout in seconds
    persist=True            # Writes to ~/.dva_lab/config.json for future sessions
)
```

### Environment Variables
You can also set environment variables without modifying code:
- `DVA_GITHUB_USER` : GitHub username or organization (e.g. `AnandChowdari`)
- `DVA_GITHUB_REPO` : Repository name (e.g. `dva-lab`)
- `DVA_GITHUB_BRANCH` : Git branch (e.g. `main`)
- `DVA_TIMEOUT` : Network timeout in seconds

---

## 5. Jupyter Notebook & IPython Magics

When `dva_lab` is imported, it automatically registers IPython line magics:

| Magic Command | Description | Example |
|---|---|---|
| `%load_code <id>` | Injects code directly into the active cell (replaces magic cell) | `%load_code 3` |
| `%show_experiment <id>` | Displays rich Markdown documentation with badges | `%show_experiment 1` |
| `%list_experiments` | Renders the HTML table of all 12 experiments | `%list_experiments` |
| `%run_experiment <id>` | Executes the experiment inline | `%run_experiment 3` |

You can also load explicitly:
```python
%load_ext dva_lab
```

---

## 6. Command-Line Interface (CLI)

`dva-lab` installs a terminal command for rapid inspection and exporting:

```bash
# List all experiments
dva-lab list

# Display documentation for Experiment 1
dva-lab show 1

# Print code to terminal
dva-lab get 3

# Download and save code to a local file
dva-lab get 3 --output exp03_bars.py

# Search experiments by keyword
dva-lab search histogram

# Check or update GitHub configuration
dva-lab config --username AnandChowdari --repository dva-lab --persist

# Display package information
dva-lab info
```

---

## 7. Complete 12-Experiment Catalog

| # | Title | Environment / Type | Methodology & Dependencies | Focus |
|:---:|---|---|---|---|
| **1** | OLAP Operations Using Materialized Views | `PostgreSQL 12+` (SQL) | PostgreSQL, Materialized Views, CUBE | Roll Up, Slice, Dice, Pivot |
| **2** | OLAP Operations Based on Star Schema | `PostgreSQL 12+` (SQL) | Fact & Dimension tables, CUBE | Star schema joins, Drill Down |
| **3** | Vertical and Horizontal Bar Charts | `Python 3.10+` | Matplotlib, NumPy | `plt.bar`, `plt.barh`, categorical comparison |
| **4** | Grouped and Stacked Bar Charts | `Python 3.10+` | Matplotlib, NumPy | Clustered offsets, stacked bottoms |
| **5** | Single & Multiple Variable Histograms | `Python 3.10+` | Matplotlib, NumPy | Frequency bins, transparency overlays |
| **6** | Single & Multiple Variable Density Plots | `Python 3.10+` | Seaborn, Matplotlib | KDE probability curves (`sns.kdeplot`) |
| **7** | Empirical Cumulative Distribution Function | `Python 3.10+` | Statsmodels, Matplotlib | Non-parametric ECDF step function |
| **8** | Q-Q Plot to Compare Two Datasets | `Python 3.10+` | SciPy, Matplotlib | Normal probability quantiles (`probplot`) |
| **9** | Scatter Plot Using Sample Data | `Python 3.10+` | Matplotlib, NumPy | Bivariate correlation, alpha blending |
| **10** | Power BI Sales Data Visualization | `Power BI Desktop` | Power BI Desktop, `sales_data.csv` | Clustered column, Pie, Line, Slicers |
| **11** | Power BI Calculations & DAX Measures | `Power BI Desktop` | DAX, Power BI Desktop | `Total Cost`, `Profit`, `CALCULATE`, `ALL` |
| **12** | Power BI Conditional & Logical Analysis | `Power BI Desktop` | DAX, Power BI Desktop | `IF`, `AND`, `OR`, Dynamic tiers |

---

## 8. Execution Guidelines

### SQL / OLAP Experiments (1 & 2)
Experiments 1 and 2 define complete PostgreSQL DDL and OLAP queries.
- **Safety Guarantee**: Calling `dva_lab.run_experiment(1)` or `dva_lab.exp1()` **never** alters an unconfigured database. It displays the verified SQL script and step-by-step instructions.
- **Live Database Execution**: If you have an active database connection (e.g. `psycopg2` or `SQLAlchemy`), pass it directly:
  ```python
  dva_lab.run_experiment(1, connection=your_db_connection)
  ```

### Python Visualization Experiments (3 to 9)
All 7 Python plotting experiments run directly in Jupyter or Python scripts:
- Fully compatible with inline rendering (`%matplotlib inline`).
- Deterministic synthetic distributions (`np.random.seed(0)`).
- Execute with:
  ```python
  dva_lab.run_experiment(3)  # or dva_lab.exp3()
  ```

### Power BI & DAX Experiments (10 to 12)
Power BI Desktop is a Windows visual application. `dva-lab` provides:
- Step-by-step instructions for fields, axes, and visual configurations.
- Exact DAX formulas for calculated columns and dynamic measures.
- Bundled CSV data accessible via `dva_lab.load_sales_data()`.
- Built-in pandas simulation verifying all DAX calculations in pure Python.

---

## 9. Testing in a Clean Virtual Environment

To build distributions and verify functionality in an isolated virtual environment:

### Step 1: Run the Complete Test Suite
```bash
pytest -v
```
*(All 74 tests pass across registry, execution, CLI, configuration, and remote retrieval).*

### Step 2: Build Wheel and Source Distribution
```bash
python -m build
```
This generates:
- `dist/dva_lab-0.2.0-py3-none-any.whl`
- `dist/dva_lab-0.2.0.tar.gz`

### Step 3: Verify in Clean Virtualenv
```bash
# Create isolated environment
python -m venv .test_venv

# Activate environment (Windows PowerShell)
.test_venv\Scripts\Activate.ps1
# (or macOS/Linux: source .test_venv/bin/activate)

# Install newly built wheel
pip install dist/dva_lab-0.2.0-py3-none-any.whl

# Test imports and execution
python -c "import dva_lab; print(dva_lab.__version__); dva_lab.configure(username='AnandChowdari', repository='dva-lab'); print(dva_lab.get_code(1)[:80]); dva_lab.list_experiments()"

# Test CLI
dva-lab list
dva-lab show 3

# Deactivate and remove test venv
deactivate
Remove-Item -Recurse -Force .test_venv
```

---

## 10. Publishing Guide (TestPyPI & Production PyPI)

### Prerequisites
Install Twine:
```bash
pip install twine
```

### Staging: Publish to TestPyPI
1. Upload to TestPyPI:
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```
   *(When prompted, enter `__token__` as username and your TestPyPI API token as password).*

2. Verify TestPyPI installation in a fresh environment:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ dva-lab
   ```

3. Test imports:
   ```python
   import dva_lab
   print(dva_lab.__version__)
   ```

### Production: Publish to PyPI
1. Upload to Production PyPI:
   ```bash
   python -m twine upload dist/*
   ```
   *(When prompted, enter `__token__` as username and your PyPI API token as password).*

2. Verify Production installation:
   ```bash
   pip install --upgrade dva-lab
   ```

> [!NOTE]
> Never commit or hardcode API tokens into your Git repository. Always use environment variables (`TWINE_PASSWORD`) or enter them securely via interactive terminal prompt.

---

## 11. License

This project is licensed under the [MIT License](LICENSE).
