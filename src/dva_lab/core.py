"""Core public API functions and Jupyter display utilities for dva_lab."""

import sys
from typing import Any, Optional, Dict
from .registry import registry, ExperimentList
from .experiments.base import Experiment


def is_jupyter() -> bool:
    """Check if the code is executing inside an interactive Jupyter / IPython environment."""
    try:
        from IPython import get_ipython
        ip = get_ipython()
        if ip is None:
            return False
        # Running in IPython shell, notebook, lab, or Colab
        if "IPKernelApp" in ip.config or "google.colab" in str(type(ip)):
            return True
        return hasattr(ip, "kernel")
    except Exception:
        return False


def list_experiments() -> ExperimentList:
    """List all 12 DVA laboratory experiments.

    In Jupyter Notebooks, renders a styled table with experiment numbers, titles,
    categories, and aims. Outside Jupyter, returns a formatted text table.
    Can also be converted to a pandas DataFrame via `.to_dataframe()`.
    """
    return registry.all()


def show_experiment(number: int) -> str:
    """Display the aim, concept, source code, dependencies, and expected output.

    Renders styled Markdown in Jupyter Notebook / Colab, or prints formatted text
    in standard terminal environments.

    Args:
        number: Experiment index from 1 to 12.

    Returns:
        The markdown formatted text representation.

    Raises:
        ValueError: If number is not an integer between 1 and 12.
    """
    exp = registry.get(number)

    # Format code fence according to category
    lang = "sql" if "SQL" in exp.category else ("python" if "Python" in exp.category else "text")

    dep_badges = ", ".join(f"`{d}`" for d in exp.dependencies)

    md = f"""# Experiment {exp.number}: {exp.title}

> **Category**: {exp.category}  
> **Required Dependencies**: {dep_badges}

---

### Aim
{exp.aim}

### Concept & Methodology
{exp.concept}

### Complete Source Code
```{lang}
{exp.code.strip()}
```

### Expected Output
```text
{exp.expected_output.strip()}
```

### Result Statement
*{exp.result}*

---
### Execution Notes & Instructions
{exp.notes}
"""

    if is_jupyter():
        try:
            from IPython.display import display, Markdown
            display(Markdown(md))
            return md
        except Exception:
            pass

    print(md)
    return md


def get_code(number: int) -> str:
    """Return the raw, complete source code for an experiment as a string.

    Suitable for copying, programmatic inspection, or saving to a file.

    Args:
        number: Experiment index from 1 to 12.

    Returns:
        The complete source code as a string.

    Raises:
        ValueError: If number is not an integer between 1 and 12.
    """
    exp = registry.get(number)
    return exp.code


def run_experiment(number: int, **kwargs) -> Any:
    """Execute a compatible experiment or display its execution instructions.

    - Experiments 3 to 9 (Python): Renders inline Matplotlib/Seaborn plots in Jupyter.
    - Experiments 1 and 2 (SQL): Displays PostgreSQL scripts & instructions (safe execution).
    - Experiments 10 to 12 (Power BI): Displays report construction guide & DAX analysis.

    Args:
        number: Experiment index from 1 to 12.
        **kwargs: Optional keyword arguments passed to the experiment runner
                  (e.g., show=True, side_by_side=True, connection=conn).

    Returns:
        The result of the experiment runner (figures for Python, script for SQL/Power BI).

    Raises:
        ValueError: If number is not an integer between 1 and 12.
    """
    exp = registry.get(number)
    return exp.run(**kwargs)


# ----------------------------------------------------------------------------
# Shortcut Functions (exp1 through exp12)
# ----------------------------------------------------------------------------

def exp1(**kwargs) -> Any:
    """Shortcut: Experiment 1 - OLAP operations using materialized views (PostgreSQL)."""
    return run_experiment(1, **kwargs)


def exp2(**kwargs) -> Any:
    """Shortcut: Experiment 2 - OLAP operations using Star schema materialized views (PostgreSQL)."""
    return run_experiment(2, **kwargs)


def exp3(**kwargs) -> Any:
    """Shortcut: Experiment 3 - Vertical and horizontal bar charts (Python)."""
    return run_experiment(3, **kwargs)


def exp4(**kwargs) -> Any:
    """Shortcut: Experiment 4 - Grouped and stacked bar charts (Python)."""
    return run_experiment(4, **kwargs)


def exp5(**kwargs) -> Any:
    """Shortcut: Experiment 5 - Single and multiple variable histograms (Python)."""
    return run_experiment(5, **kwargs)


def exp6(**kwargs) -> Any:
    """Shortcut: Experiment 6 - Single and multiple variable density plots (Python)."""
    return run_experiment(6, **kwargs)


def exp7(**kwargs) -> Any:
    """Shortcut: Experiment 7 - Empirical Cumulative Distribution Function (ECDF) plot (Python)."""
    return run_experiment(7, **kwargs)


def exp8(**kwargs) -> Any:
    """Shortcut: Experiment 8 - Q-Q plot to compare two datasets (Python)."""
    return run_experiment(8, **kwargs)


def exp9(**kwargs) -> Any:
    """Shortcut: Experiment 9 - Scatter plot using sample data (Python)."""
    return run_experiment(9, **kwargs)


def exp10(**kwargs) -> Any:
    """Shortcut: Experiment 10 - Power BI sales data visualization."""
    return run_experiment(10, **kwargs)


def exp11(**kwargs) -> Any:
    """Shortcut: Experiment 11 - Power BI sales calculations and DAX measures."""
    return run_experiment(11, **kwargs)


def exp12(**kwargs) -> Any:
    """Shortcut: Experiment 12 - Power BI conditional & logical analysis (IF, AND, OR)."""
    return run_experiment(12, **kwargs)


def about() -> None:
    """Display library overview, version, and quick reference guide."""
    from . import __version__
    text = f"""
================================================================================
dva-lab (v{__version__}) - Data Visualization and Analytics Laboratory Library
================================================================================
A self-contained Python package empowering students to retrieve, display, and
execute Data Visualization and Analytics (DVA) experiments inside Jupyter Notebook.

Public API:
  - dva_lab.list_experiments()     : List all 12 experiments with metadata
  - dva_lab.show_experiment(n)     : Display full experiment guide in Markdown
  - dva_lab.get_code(n)            : Retrieve raw source code as a string
  - dva_lab.run_experiment(n)      : Execute Python plots or show SQL/Power BI guides
  - dva_lab.exp1() ... exp12()     : Fast convenience shortcuts
  - dva_lab.load_sales_data()      : Load bundled sales_data.csv as DataFrame
  - dva_lab.about()                : Show this help guide

Experiments Catalog:
  [SQL / OLAP]
    1. OLAP Operations Using Materialized Views
    2. OLAP Operations Using Materialized Views (Star Schema)
  [Python Visualizations]
    3. Vertical and Horizontal Bar Charts
    4. Grouped and Stacked Bar Charts
    5. Single and Multiple Variable Histograms
    6. Single and Multiple Variable Density Plots
    7. Empirical Cumulative Distribution Function (ECDF) Plot
    8. Q-Q Plot to Compare Two Datasets
    9. Scatter Plot Using Sample Data
  [Power BI & DAX]
    10. Power BI Sales Data Visualization
    11. Power BI Sales Calculations and DAX Measures
    12. Power BI Conditional and Logical Analysis (IF, AND, OR)

Repository: https://github.com/YOUR-USERNAME/dva-lab.git
Authoritative Reference: DVA Lab Record
================================================================================
"""
    if is_jupyter():
        try:
            from IPython.display import display, Markdown
            display(Markdown(f"```text{text}```"))
            return
        except Exception:
            pass
    print(text)


help = about
