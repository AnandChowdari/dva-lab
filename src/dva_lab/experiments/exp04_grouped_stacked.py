"""Experiment 4: Grouped and stacked bar charts."""

from typing import Any, Optional, Tuple
from .base import Experiment

NUMBER = 4
TITLE = "Grouped and Stacked Bar Charts"
CATEGORY = "Data Visualization (Python)"
AIM = "Write a Python program to Implement or create grouped and stacked bar charts."
DEPENDENCIES = ["matplotlib", "numpy"]

CONCEPT = """\
When comparing multiple sub-series across categories:
- Grouped Bar Charts (Clustered): Render bars for each series side-by-side by computing positional offsets \
(positions - width, positions, positions + width). Best for directly comparing individual series performance \
across categories.
- Stacked Bar Charts: Stack bars vertically on top of each other using the 'bottom' parameter in plt.bar(). \
Best for communicating aggregate total volume while displaying part-to-whole segment contributions.\
"""

CODE = """\
# ============================================================================
# Experiment 4: Grouped and Stacked Bar Charts
# Libraries: matplotlib, numpy
# ============================================================================

import matplotlib.pyplot as plt
import numpy as np

# Sample Data
regions = ['North', 'South', 'East', 'West']
product1 = [200, 220, 250, 190]
product2 = [150, 180, 200, 160]
product3 = [100, 130, 150, 120]
positions = np.arange(len(regions))
width = 0.25

# ----------------------------------------------------------------------------
# 1. Grouped Bar Chart
# ----------------------------------------------------------------------------
plt.figure(figsize=(6, 4))
plt.bar(positions - width, product1, width, label='Product 1', color='black')
plt.bar(positions,         product2, width, label='Product 2', color='orange')
plt.bar(positions + width, product3, width, label='Product 3', color='green')
plt.xticks(positions, regions)
plt.xlabel('Region')
plt.ylabel('Sales')
plt.title('Grouped Bar Chart of Sales by Region')
plt.legend()
plt.tight_layout()
plt.show()

# ----------------------------------------------------------------------------
# 2. Stacked Bar Chart
# ----------------------------------------------------------------------------
p1 = np.array(product1)
p2 = np.array(product2)
p3 = np.array(product3)

plt.figure(figsize=(6, 4))
plt.bar(positions, p1, label='Product 1', color='black')
plt.bar(positions, p2, bottom=p1, label='Product 2', color='orange')
plt.bar(positions, p3, bottom=p1 + p2, label='Product 3', color='green')
plt.xticks(positions, regions)
plt.xlabel('Region')
plt.ylabel('Sales')
plt.title('Stacked Bar Chart of Sales by Region')
plt.legend()
plt.tight_layout()
plt.show()
"""

EXPECTED_OUTPUT = """\
Expected Visual Output:
1. Figure 1 (Grouped Bar Chart):
   - 3 clustered bars per region (Black: Product 1, Orange: Product 2, Green: Product 3).
   - Clear visual comparison showing Product 1 leading across all regions.

2. Figure 2 (Stacked Bar Chart):
   - Single segmented column per region reaching cumulative height:
     * North: 450 (200 + 150 + 100)
     * South: 530 (220 + 180 + 130)
     * East: 600 (250 + 200 + 150)
     * West: 470 (190 + 160 + 120)
   - Colors stacked: Black on bottom, Orange in middle, Green on top.
"""

RESULT = (
    "Grouped and stacked bar charts were successfully implemented and visualized "
    "using Matplotlib and NumPy."
)

NOTES = """\
Usage Notes:
- Grouped charts require offset calculations (positions +/- width).
- Stacked charts require numpy arrays or cumulative sums passed to the `bottom` argument.\
"""


def run(show: bool = True, side_by_side: bool = False) -> Any:
    """Execute Experiment 4: Render grouped and stacked bar charts."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:
        raise ImportError(
            f"Missing required visualization dependencies: {exc}.\n"
            "Install with: pip install dva-lab[viz] or pip install matplotlib numpy"
        ) from exc

    regions = ["North", "South", "East", "West"]
    product1 = np.array([200, 220, 250, 190])
    product2 = np.array([150, 180, 200, 160])
    product3 = np.array([100, 130, 150, 120])
    positions = np.arange(len(regions))
    width = 0.25

    if side_by_side:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

        ax1.bar(positions - width, product1, width, label="Product 1", color="black")
        ax1.bar(positions, product2, width, label="Product 2", color="orange")
        ax1.bar(positions + width, product3, width, label="Product 3", color="green")
        ax1.set_xticks(positions)
        ax1.set_xticklabels(regions)
        ax1.set_xlabel("Region")
        ax1.set_ylabel("Sales")
        ax1.set_title("Grouped Bar Chart of Sales by Region")
        ax1.legend()
        ax1.grid(axis="y", linestyle="--", alpha=0.5)

        ax2.bar(positions, product1, label="Product 1", color="black")
        ax2.bar(positions, product2, bottom=product1, label="Product 2", color="orange")
        ax2.bar(positions, product3, bottom=product1 + product2, label="Product 3", color="green")
        ax2.set_xticks(positions)
        ax2.set_xticklabels(regions)
        ax2.set_xlabel("Region")
        ax2.set_ylabel("Sales")
        ax2.set_title("Stacked Bar Chart of Sales by Region")
        ax2.legend()
        ax2.grid(axis="y", linestyle="--", alpha=0.5)

        fig.tight_layout()
        if show:
            plt.show()
        return fig
    else:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.bar(positions - width, product1, width, label="Product 1", color="black")
        ax1.bar(positions, product2, width, label="Product 2", color="orange")
        ax1.bar(positions + width, product3, width, label="Product 3", color="green")
        ax1.set_xticks(positions)
        ax1.set_xticklabels(regions)
        ax1.set_xlabel("Region")
        ax1.set_ylabel("Sales")
        ax1.set_title("Grouped Bar Chart of Sales by Region")
        ax1.legend()
        ax1.grid(axis="y", linestyle="--", alpha=0.5)
        fig1.tight_layout()
        if show:
            plt.show()

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.bar(positions, product1, label="Product 1", color="black")
        ax2.bar(positions, product2, bottom=product1, label="Product 2", color="orange")
        ax2.bar(positions, product3, bottom=product1 + product2, label="Product 3", color="green")
        ax2.set_xticks(positions)
        ax2.set_xticklabels(regions)
        ax2.set_xlabel("Region")
        ax2.set_ylabel("Sales")
        ax2.set_title("Stacked Bar Chart of Sales by Region")
        ax2.legend()
        ax2.grid(axis="y", linestyle="--", alpha=0.5)
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
