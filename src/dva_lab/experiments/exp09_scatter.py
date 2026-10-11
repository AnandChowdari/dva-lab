"""Experiment 9: Scatter plot using sample data."""

from typing import Any, Optional
from .base import Experiment

NUMBER = 9
TITLE = "Scatter Plot Using Sample Data"
CATEGORY = "Data Visualization (Python)"
AIM = "Write a Python program to implement a Scatter Plot using sample data."
DEPENDENCIES = ["matplotlib", "numpy"]

CONCEPT = """\
A Scatter Plot maps pairs of continuous numerical measurements onto Cartesian coordinates (X, Y):
- Bivariate Analysis: Highlights correlation direction (positive, negative, independent), \
linearity, and strength of association between two features.
- Pattern Discovery: Readily exposes clusters, non-linear dependencies, heteroskedasticity, \
and anomalous outliers.
- Aesthetic tuning with alpha blending (alpha=0.7) and edge borders (edgecolor='black') prevents \
visual occlusion in dense clusters.\
"""

CODE = """\
# ============================================================================
# Experiment 9: Scatter Plot Using Sample Data
# Libraries: matplotlib, numpy
# ============================================================================

import matplotlib.pyplot as plt
import numpy as np

# Generate Bivariate Sample Data
np.random.seed(0)
x = np.random.normal(loc=50, scale=10, size=100)
y = np.random.normal(loc=60, scale=15, size=100)

# Render Scatter Plot
plt.figure(figsize=(6, 4))
plt.scatter(x, y, color='blue', alpha=0.7, edgecolor='black')
plt.title('Scatter Plot of Sample Data')
plt.xlabel('X Values')
plt.ylabel('Y Values')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
"""

EXPECTED_OUTPUT = """\
Expected Visual Output:
- Cartesian coordinate plot with 100 circular blue markers with black borders.
- X-axis centered at ~50 spanning roughly 25 to 75.
- Y-axis centered at ~60 spanning roughly 20 to 100.
- Point cloud exhibits roughly spherical distribution, characteristic of independent bivariate normal distributions.
"""

RESULT = (
    "A scatter plot of bivariate sample data was successfully created and visualized "
    "using Matplotlib and NumPy."
)

NOTES = """\
Usage Notes:
- Visualizes 100 points generated from two independent normal distributions.
- Alpha blending ensures points that overlap remain distinguishable.\
"""


def run(show: bool = True, seed: int = 0) -> Any:
    """Execute Experiment 9: Render scatter plot."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:
        raise ImportError(
            f"Missing required visualization dependencies: {exc}.\n"
            "Install with: pip install dva-lab[viz] or pip install matplotlib numpy"
        ) from exc

    np.random.seed(seed)
    x = np.random.normal(loc=50, scale=10, size=100)
    y = np.random.normal(loc=60, scale=15, size=100)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(x, y, color="blue", alpha=0.7, edgecolor="black")
    ax.set_title("Scatter Plot of Sample Data")
    ax.set_xlabel("X Values")
    ax.set_ylabel("Y Values")
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()

    if show:
        plt.show()
    return fig


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
