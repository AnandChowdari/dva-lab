"""Core public API functions, remote GitHub retrieval, and Jupyter display utilities for dva_lab."""

import sys
from typing import Any, Optional, Dict, List, Union

from .config import configure, get_config, reset_config
from .client import get_client
from .registry import registry, ExperimentList
from .experiments.base import Experiment
from .exceptions import (
    DVALabError,
    ExperimentNotFoundError,
    RepositoryNotFoundError,
    RemoteFetchError,
)


def safe_print(text: str) -> None:
    """Print text safely across different OS encodings (including Windows cp1252)."""
    try:
        print(text)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", "utf-8") or "utf-8"
        print(text.encode(encoding, errors="replace").decode(encoding))


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


class CodeString(str):
    """String subclass that renders with syntax highlighting in Jupyter Notebook."""

    def __new__(cls, content: str, language: str = "python"):
        obj = super().__new__(cls, content)
        obj.language = language
        return obj

    def _repr_markdown_(self) -> str:
        """Render syntax-highlighted code block in Jupyter."""
        return f"```{self.language}\n{self}\n```"

    def __repr__(self) -> str:
        return str(self)


def get_info(number: Union[int, str], refresh: bool = False) -> Dict[str, Any]:
    """Retrieve full metadata for an experiment as a dictionary.

    Args:
        number: Experiment identifier (1 to 12).
        refresh: If True, forces refreshing remote catalog from GitHub.

    Returns:
        Dictionary containing experiment metadata.
    """
    client = get_client()
    try:
        _, entry = client.resolve_experiment(number, refresh=refresh)
        return entry
    except Exception:
        # Fallback to local registry
        try:
            num = int(str(number).strip())
            return registry.get(num).to_dict()
        except Exception:
            raise ExperimentNotFoundError(number)


def search(query: str, refresh: bool = False) -> List[Dict[str, Any]]:
    """Search registered experiments matching a query keyword.

    Args:
        query: Search term (case-insensitive substring match).
        refresh: If True, forces refreshing catalog from GitHub.

    Returns:
        List of matching experiment metadata dictionaries.
    """
    client = get_client()
    try:
        index = client.fetch_index(refresh=refresh)
        entries = list(index.values())
    except Exception:
        entries = [exp.to_dict() for exp in registry.all()]

    q = query.strip().lower()
    matches = []
    for item in entries:
        title = item.get("title", "").lower()
        desc = item.get("description", item.get("aim", "")).lower()
        cat = item.get("category", "").lower()
        tags = [t.lower() for t in item.get("tags", [])]

        if q in title or q in desc or q in cat or any(q in t for t in tags):
            matches.append(item)
    return matches


def list_experiments(refresh: bool = False) -> ExperimentList:
    """List all 12 DVA laboratory experiments.

    In Jupyter Notebooks, renders a styled table with experiment numbers, titles,
    categories, and aims. Outside Jupyter, returns a formatted text table.
    Can also be converted to a pandas DataFrame via `.to_dataframe()`.

    Args:
        refresh: If True, forces refreshing catalog from GitHub.
    """
    return registry.all()


def get_code(
    number: Union[int, str],
    refresh: bool = False,
    cache: bool = True,
    remote: bool = True,
) -> CodeString:
    """Retrieve the raw source code for an experiment.

    Attempts to fetch the latest version from the configured GitHub repository
    over HTTPS without requiring Git. If offline or remote fetch fails,
    seamlessly falls back to the bundled authoritative source code.

    Args:
        number: Experiment index from 1 to 12.
        refresh: Force fresh download from GitHub, bypassing cache.
        cache: Cache retrieved code locally.
        remote: Allow fetching from remote GitHub.

    Returns:
        CodeString containing the complete source code.

    Raises:
        ExperimentNotFoundError: If the experiment number is invalid.
    """
    client = get_client()
    config = client.config
    int_id: Optional[int] = None
    try:
        int_id = int(str(number).strip())
    except ValueError:
        pass

    # Attempt remote fetch if enabled
    if remote:
        try:
            _, entry = client.resolve_experiment(number, refresh=refresh)
            file_path = entry.get("file")
            lang = entry.get("language", "python")
            if file_path:
                source = client.fetch_code(file_path, refresh=refresh, cache=cache)
                return CodeString(source, language=lang)
        except Exception:
            if not config.offline_fallback:
                raise

    # Fallback to local registry
    if int_id is not None and 1 <= int_id <= 12:
        exp = registry.get(int_id)
        lang = "sql" if "SQL" in exp.category else ("python" if "Python" in exp.category else "text")
        return CodeString(exp.code, language=lang)

    raise ExperimentNotFoundError(number)


def show_code(number: Union[int, str], refresh: bool = False) -> CodeString:
    """Display the raw source code for an experiment with syntax highlighting.

    Args:
        number: Experiment index from 1 to 12.
        refresh: Force fresh download from GitHub.

    Returns:
        CodeString for copying or programmatic use.
    """
    code_str = get_code(number, refresh=refresh)
    if is_jupyter():
        try:
            from IPython.display import display, Markdown
            display(Markdown(f"```{code_str.language}\n{code_str}\n```"))
            return code_str
        except Exception:
            pass
    print(code_str)
    return code_str


def show_experiment(number: Union[int, str], refresh: bool = False) -> str:
    """Display the aim, concept, source code, dependencies, and expected output.

    Renders styled Markdown in Jupyter Notebook / Colab, or prints formatted text
    in standard terminal environments.

    Args:
        number: Experiment index from 1 to 12.
        refresh: Force fresh download from GitHub.

    Returns:
        The markdown formatted text representation.

    Raises:
        ExperimentNotFoundError: If number is not an integer between 1 and 12.
    """
    int_id: int
    try:
        int_id = int(str(number).strip())
    except ValueError:
        raise ExperimentNotFoundError(number)

    if int_id < 1 or int_id > 12:
        raise ExperimentNotFoundError(number)

    exp = registry.get(int_id)

    # Format code fence according to category
    lang = "sql" if "SQL" in exp.category else ("python" if "Python" in exp.category else "text")
    dep_badges = ", ".join(f"`{d}`" for d in exp.dependencies)

    # Environment notice badge
    if "SQL" in exp.category:
        env_notice = "> **Environment Requirement**: Requires an external **PostgreSQL 12+** server."
    elif "Power BI" in exp.category:
        env_notice = "> **Environment Requirement**: Requires **Microsoft Power BI Desktop** (Windows)."
    else:
        env_notice = "> **Environment Requirement**: Pure **Python** (runs directly in Jupyter / Colab)."

    md = f"""# Experiment {exp.number}: {exp.title}

> **Category**: {exp.category}  
> **Required Dependencies**: {dep_badges}  
{env_notice}

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

    safe_print(md)
    return md


def run_experiment(number: int, **kwargs) -> Any:
    """Execute a compatible experiment or display its execution instructions.

    Clearly distinguishes between:
    - Experiments 3 to 9 (Pure Python): Renders inline Matplotlib/Seaborn plots in Jupyter.
    - Experiments 1 and 2 (SQL / OLAP): Requires PostgreSQL 12+. Displays setup guide & queries.
      (Pass `connection=your_db_connection` to execute live queries).
    - Experiments 10 to 12 (Power BI): Requires Power BI Desktop. Displays visual instructions,
      DAX measures, previews sales data, and runs Python DAX simulations.

    Special Arguments:
        code=True (or show_code=True): Display and return source code instead of running.

    Args:
        number: Experiment index from 1 to 12.
        **kwargs: Optional keyword arguments passed to the experiment runner.

    Returns:
        The result of the experiment runner (figures for Python, script for SQL/Power BI).

    Raises:
        ExperimentNotFoundError: If number is not an integer between 1 and 12.
    """
    if kwargs.get("code") or kwargs.get("show_code"):
        return show_code(number)

    int_id: int
    try:
        int_id = int(str(number).strip())
    except ValueError:
        raise ExperimentNotFoundError(number)

    if int_id < 1 or int_id > 12:
        raise ExperimentNotFoundError(number)

    exp = registry.get(int_id)

    # Informative console headers distinguishing execution categories
    if int_id in (1, 2):
        print(f"\n[DVA Lab - SQL Experiment {int_id}: {exp.title}]")
        print("Note: This experiment defines PostgreSQL DDL & OLAP queries.")
        print("For safe execution, displaying SQL queries and execution instructions.")
        print("To run against a live database: dva_lab.run_experiment(number, connection=conn)\n")
    elif int_id in (10, 11, 12):
        print(f"\n[DVA Lab - Power BI Experiment {int_id}: {exp.title}]")
        print("Note: This experiment is designed for Microsoft Power BI Desktop.")
        print("Displaying dashboard setup guide, DAX formulas, and dataset simulation.\n")

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


# ----------------------------------------------------------------------------
# Code-only Shortcuts (code1 through code12 and code())
# ----------------------------------------------------------------------------

code = show_code


def code1() -> CodeString:
    """Shortcut: Print and return source code for Experiment 1 (PostgreSQL OLAP)."""
    return show_code(1)


def code2() -> CodeString:
    """Shortcut: Print and return source code for Experiment 2 (Star Schema OLAP)."""
    return show_code(2)


def code3() -> CodeString:
    """Shortcut: Print and return source code for Experiment 3 (Vertical & Horizontal Bar Charts)."""
    return show_code(3)


def code4() -> CodeString:
    """Shortcut: Print and return source code for Experiment 4 (Grouped & Stacked Bar Charts)."""
    return show_code(4)


def code5() -> CodeString:
    """Shortcut: Print and return source code for Experiment 5 (Single & Multi-Variable Histograms)."""
    return show_code(5)


def code6() -> CodeString:
    """Shortcut: Print and return source code for Experiment 6 (Single & Multi-Variable Density Plots)."""
    return show_code(6)


def code7() -> CodeString:
    """Shortcut: Print and return source code for Experiment 7 (ECDF Plot)."""
    return show_code(7)


def code8() -> CodeString:
    """Shortcut: Print and return source code for Experiment 8 (Q-Q Plot)."""
    return show_code(8)


def code9() -> CodeString:
    """Shortcut: Print and return source code for Experiment 9 (Scatter Plot)."""
    return show_code(9)


def code10() -> CodeString:
    """Shortcut: Print and return source code / procedure for Experiment 10 (Power BI Sales Visuals)."""
    return show_code(10)


def code11() -> CodeString:
    """Shortcut: Print and return source code / DAX for Experiment 11 (Power BI DAX Measures)."""
    return show_code(11)


def code12() -> CodeString:
    """Shortcut: Print and return source code / DAX for Experiment 12 (Power BI Logic IF/AND/OR)."""
    return show_code(12)


def about() -> None:
    """Display library overview, version, configuration, and quick reference guide."""
    from . import __version__
    cfg = get_config()
    text = f"""
================================================================================
dva-lab (v{__version__}) - Data Visualization and Analytics Laboratory Library
================================================================================
A Python package for retrieving, displaying, and executing Data Visualization
and Analytics (DVA) experiments inside Jupyter Notebook or standalone scripts.

Connected GitHub Repository:
  User / Org : {cfg.username}
  Repository : {cfg.repository}
  Branch     : {cfg.branch}
  Raw HTTPS  : https://raw.githubusercontent.com/{cfg.username}/{cfg.repository}/{cfg.branch}/

Public API:
  - dva_lab.configure(user, repo)  : Point to custom GitHub repository
  - dva_lab.list_experiments()     : List all 12 experiments with metadata
  - dva_lab.show_experiment(n)     : Display full experiment manual in Markdown
  - dva_lab.get_code(n)            : Fetch source code from GitHub over HTTPS
  - dva_lab.run_experiment(n)      : Execute Python plots or show SQL/Power BI guides
  - dva_lab.search(query)          : Search experiments by topic, tool, or keyword
  - dva_lab.exp1() ... exp12()     : Fast convenience shortcuts
  - dva_lab.load_sales_data()      : Load bundled sales_data.csv as DataFrame
  - dva_lab.about()                : Show this help guide

Jupyter Magics:
  - %load_code <id>                : Inject experiment code directly into active cell
  - %show_experiment <id>          : Render markdown guide in notebook
  - %run_experiment <id>           : Run experiment directly

Experiments Catalog:
  [SQL / OLAP - Requires PostgreSQL 12+]
    1. OLAP Operations Using Materialized Views
    2. OLAP Operations Using Materialized Views (Star Schema)
  [Python Visualizations - Direct execution]
    3. Vertical and Horizontal Bar Charts
    4. Grouped and Stacked Bar Charts
    5. Single and Multiple Variable Histograms
    6. Single and Multiple Variable Density Plots
    7. Empirical Cumulative Distribution Function (ECDF) Plot
    8. Q-Q Plot to Compare Two Datasets
    9. Scatter Plot Using Sample Data
  [Power BI & DAX - Requires Power BI Desktop]
    10. Power BI Sales Data Visualization
    11. Power BI Sales Calculations and DAX Measures
    12. Power BI Conditional and Logical Analysis (IF, AND, OR)

Repository: https://github.com/{cfg.username}/{cfg.repository}
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
