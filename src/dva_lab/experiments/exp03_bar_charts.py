"""Experiment 3: Vertical and horizontal bar charts."""

from typing import Any, Optional, Tuple
from .base import Experiment

NUMBER = 3
TITLE = "Vertical and Horizontal Bar Charts"
CATEGORY = "Data Visualization (Python)"
AIM = "Write a Python program to Implement or create horizontal and vertical bar charts."
DEPENDENCIES = ["matplotlib", "numpy"]

CONCEPT = """\
Bar charts are fundamental visualization tools for comparing numerical values across categorical groups:
- Vertical Bar Charts (Column Charts): Plot categories along the horizontal X-axis and metric values \
along the vertical Y-axis. Ideal when category labels are concise and chronological or natural sequences exist.
- Horizontal Bar Charts: Plot categories along the vertical Y-axis and values along the horizontal X-axis. \
Highly effective when category names are lengthy, preventing cramped or overlapping axis labels.\
"""

CODE = """\
# ============================================================================
# Experiment 3: Vertical and Horizontal Bar Charts
# Libraries: matplotlib, numpy
# ============================================================================

import matplotlib.pyplot as plt
import numpy as np

# Sample Data
regions = ['North', 'South', 'East', 'West']
sales = [200, 220, 250, 190]
positions = np.arange(len(regions))

# ----------------------------------------------------------------------------
# 1. Vertical Bar Chart
# ----------------------------------------------------------------------------
plt.figure(figsize=(6, 4))
plt.bar(positions, sales, color='steelblue')
plt.xticks(positions, regions)
plt.xlabel('Region')
plt.ylabel('Sales')
plt.title('Vertical Bar Chart of Sales by Region')
plt.tight_layout()
plt.show()

# ----------------------------------------------------------------------------
# 2. Horizontal Bar Chart
# ----------------------------------------------------------------------------
plt.figure(figsize=(6, 4))
plt.barh(positions, sales, color='steelblue')
plt.yticks(positions, regions)
plt.xlabel('Sales')
plt.ylabel('Region')
plt.title('Horizontal Bar Chart of Sales by Region')
plt.tight_layout()
plt.show()
"""

EXPECTED_OUTPUT = """\
Expected Visual Output:
1. Figure 1 (Vertical Bar Chart):
   - X-axis: Regions ['North', 'South', 'East', 'West']
   - Y-axis: Sales values (190 to 250)
   - Steelblue vertical rectangular bars showing East as highest (250) and West as lowest (190).

2. Figure 2 (Horizontal Bar Chart):
   - Y-axis: Regions ['North', 'South', 'East', 'West']
   - X-axis: Sales values (0 to 250)
   - Steelblue horizontal rectangular bars extending to the right.
"""

RESULT = (
    "Vertical and horizontal bar charts were successfully plotted and compared "
    "using Matplotlib and NumPy."
)

NOTES = """\
Usage Notes:
- Calls matplotlib.pyplot and numpy.
- In Jupyter Notebooks, figures are rendered inline automatically.
- Both individual plots and a combined side-by-side view are supported.\
"""


def run(show: bool = True, side_by_side: bool = False) -> Any:
    """Execute Experiment 3: Render vertical and horizontal bar charts."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:
        raise ImportError(
            f"Missing required visualization dependencies: {exc}.\n"
            "Install with: pip install dva-lab[viz] or pip install matplotlib numpy"
        ) from exc

    regions = ["North", "South", "East", "West"]
    sales = [200, 220, 250, 190]
    positions = np.arange(len(regions))

    if side_by_side:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

        ax1.bar(positions, sales, color="steelblue", edgecolor="#222222", linewidth=0.8)
        ax1.set_xticks(positions)
        ax1.set_xticklabels(regions)
        ax1.set_xlabel("Region")
        ax1.set_ylabel("Sales")
        ax1.set_title("Vertical Bar Chart of Sales by Region")
        ax1.grid(axis="y", linestyle="--", alpha=0.5)

        ax2.barh(positions, sales, color="steelblue", edgecolor="#222222", linewidth=0.8)
        ax2.set_yticks(positions)
        ax2.set_yticklabels(regions)
        ax2.set_xlabel("Sales")
        ax2.set_ylabel("Region")
        ax2.set_title("Horizontal Bar Chart of Sales by Region")
        ax2.grid(axis="x", linestyle="--", alpha=0.5)

        fig.tight_layout()
        if show:
            plt.show()
        return fig
    else:
        # Generate sequentially matching lab manual
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.bar(positions, sales, color="steelblue", edgecolor="#222222", linewidth=0.8)
        ax1.set_xticks(positions)
        ax1.set_xticklabels(regions)
        ax1.set_xlabel("Region")
        ax1.set_ylabel("Sales")
        ax1.set_title("Vertical Bar Chart of Sales by Region")
        ax1.grid(axis="y", linestyle="--", alpha=0.5)
        fig1.tight_layout()
        if show:
            plt.show()

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.barh(positions, sales, color="steelblue", edgecolor="#222222", linewidth=0.8)
        ax2.set_yticks(positions)
        ax2.set_yticklabels(regions)
        ax2.set_xlabel("Sales")
        ax2.set_ylabel("Region")
        ax2.set_title("Horizontal Bar Chart of Sales by Region")
        ax2.grid(axis="x", linestyle="--", alpha=0.5)
        fig2.tight_layout()
        if show:
            plt.show()

        return fig1, fig2


def get_experiment() -> Experiment:
    """Create and return the Experiment instance."""
    return Experiment(
        number=NUMBER,
        title=TITLE,
        category=CATEGORY,
        aim=AIM,
        concept=CONCEPT,
        code=CODE,
        dependencies=DEPENDENCIES,
        expected_output=EXPECTED_OUTPUT,
        result=RESULT,
        notes=NOTES,
        run_func=run,
    )
