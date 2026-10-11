"""Experiment 5: Single and multiple variable histograms."""

from typing import Any, Optional
from .base import Experiment

NUMBER = 5
TITLE = "Single and Multiple Variable Histograms"
CATEGORY = "Data Visualization (Python)"
AIM = "Write a Python program to Implement histogram using single and multiple variable distribution."
DEPENDENCIES = ["matplotlib", "numpy"]

CONCEPT = """\
Histograms group continuous numerical data into consecutive, non-overlapping intervals (bins) \
and plot the frequency count of data points inside each bin:
- Single Variable Histogram: Displays the empirical probability distribution, symmetry, modality, \
and dispersion of a single feature (e.g., student exam scores).
- Multiple Variable Histogram: Compares two or more distributions on the same axis scale using \
overlapping semi-transparent bins (alpha=0.6) and a distinct legend (e.g., Maths vs. Science).\
"""

CODE = """\
# ============================================================================
# Experiment 5: Single and Multiple Variable Histograms
# Libraries: matplotlib, numpy
# Note: Fixed typos in lab manual ('Import' -> 'import', separated title/xlabel lines)
# ============================================================================

import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------------
# 1. Histogram - Single Variable
# ----------------------------------------------------------------------------
np.random.seed(0)
scores = np.random.normal(loc=75, scale=10, size=100)

plt.figure(figsize=(6, 4))
plt.hist(scores, bins=8, color='steelblue', edgecolor='black')
plt.title('Histogram of Test Scores (Single Variable)')
plt.xlabel('Test Scores')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()

# ----------------------------------------------------------------------------
# 2. Histogram - Multiple Variables
# ----------------------------------------------------------------------------
np.random.seed(0)
maths = np.random.normal(loc=75, scale=10, size=100)
science = np.random.normal(loc=65, scale=12, size=100)

plt.figure(figsize=(6, 4))
plt.hist(maths, bins=8, alpha=0.6, color='steelblue', edgecolor='black', label='Maths')
plt.hist(science, bins=8, alpha=0.6, color='orange', edgecolor='black', label='Science')
plt.title('Histogram of Test Scores (Multiple Variables)')
plt.xlabel('Test Scores')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.show()
"""

EXPECTED_OUTPUT = """\
Expected Visual Output:
1. Figure 1 (Single Variable):
   - Bell-shaped histogram centered around 75 with 8 bins spanning ~50 to ~100.
   - Frequency peaks near 70-80 with ~25-30 counts.

2. Figure 2 (Multiple Variables):
   - Overlapping bins: Steelblue (Maths, mean ~75) and Orange (Science, mean ~65).
   - Visual shift demonstrates Science scores have a lower mean and wider variance.
"""

RESULT = (
    "Single-variable and multiple-variable histograms were successfully implemented "
    "and plotted using Matplotlib."
)

NOTES = """\
Lab Record Corrections:
1. Fixed syntax error where 'Import' was capitalized in the manual.
2. Fixed run-on line where `plt.title(...)` and `plt.xlabel(...)` were merged on page 17.
3. Random seed is set to 0 for reproducible synthetic distributions.\
"""


def run(show: bool = True, side_by_side: bool = False) -> Any:
    """Execute Experiment 5: Render single and multi-variable histograms."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as exc:
        raise ImportError(
            f"Missing required visualization dependencies: {exc}.\n"
            "Install with: pip install dva-lab[viz] or pip install matplotlib numpy"
        ) from exc

    np.random.seed(0)
    scores = np.random.normal(loc=75, scale=10, size=100)
    maths = np.random.normal(loc=75, scale=10, size=100)
    science = np.random.normal(loc=65, scale=12, size=100)

    if side_by_side:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

        ax1.hist(scores, bins=8, color="steelblue", edgecolor="black")
        ax1.set_title("Histogram of Test Scores (Single Variable)")
        ax1.set_xlabel("Test Scores")
        ax1.set_ylabel("Frequency")
        ax1.grid(axis="y", linestyle="--", alpha=0.5)

        ax2.hist(maths, bins=8, alpha=0.6, color="steelblue", edgecolor="black", label="Maths")
        ax2.hist(science, bins=8, alpha=0.6, color="orange", edgecolor="black", label="Science")
        ax2.set_title("Histogram of Test Scores (Multiple Variables)")
        ax2.set_xlabel("Test Scores")
        ax2.set_ylabel("Frequency")
        ax2.legend()
        ax2.grid(axis="y", linestyle="--", alpha=0.5)

        fig.tight_layout()
        if show:
            plt.show()
        return fig
    else:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        ax1.hist(scores, bins=8, color="steelblue", edgecolor="black")
        ax1.set_title("Histogram of Test Scores (Single Variable)")
        ax1.set_xlabel("Test Scores")
        ax1.set_ylabel("Frequency")
        ax1.grid(axis="y", linestyle="--", alpha=0.5)
        fig1.tight_layout()
        if show:
            plt.show()

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.hist(maths, bins=8, alpha=0.6, color="steelblue", edgecolor="black", label="Maths")
        ax2.hist(science, bins=8, alpha=0.6, color="orange", edgecolor="black", label="Science")
        ax2.set_title("Histogram of Test Scores (Multiple Variables)")
        ax2.set_xlabel("Test Scores")
        ax2.set_ylabel("Frequency")
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
