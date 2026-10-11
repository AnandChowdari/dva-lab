"""Experiment 6: Single and multiple variable density plots."""

from typing import Any, Optional
from .base import Experiment

NUMBER = 6
TITLE = "Single and Multiple Variable Density Plots"
CATEGORY = "Data Visualization (Python)"
AIM = "Write a Python program to implement density plot using single and multiple variable distribution."
DEPENDENCIES = ["matplotlib", "seaborn", "numpy"]

CONCEPT = """\
A Density Plot represents data distribution through Kernel Density Estimation (KDE):
- Unlike histograms, KDE creates a smooth, continuous probability density estimate, eliminating \
arbitrary bin-boundary artifacts.
- Single Variable Density Plot: Estimates the underlying probability distribution of a continuous \
variable, with area under the curve summing to 1.
- Multiple Variable Density Plot: Overlays distinct KDE curves with translucent fills to allow \
immediate comparison of mean locations, spread (variance), and multimodal tendencies across groups.\
"""

CODE = """\
# ============================================================================
# Experiment 6: Single and Multiple Variable Density Plots
# Libraries: matplotlib, seaborn, numpy
# ============================================================================

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ----------------------------------------------------------------------------
# 1. Density Plot - Single Variable
# ----------------------------------------------------------------------------
np.random.seed(0)
scores = np.random.normal(loc=75, scale=10, size=100)

plt.figure(figsize=(6, 4))
sns.kdeplot(scores, color='steelblue', fill=True)
plt.title('Density Plot of Test Scores (Single Variable)')
plt.xlabel('Test Scores')
plt.ylabel('Density')
plt.tight_layout()
plt.show()

# ----------------------------------------------------------------------------
# 2. Density Plot - Multiple Variables
# ----------------------------------------------------------------------------
np.random.seed(0)
maths = np.random.normal(loc=75, scale=10, size=100)
science = np.random.normal(loc=65, scale=12, size=100)

plt.figure(figsize=(6, 4))
sns.kdeplot(maths, color='steelblue', fill=True, label='Maths')
sns.kdeplot(science, color='orange', fill=True, label='Science')
plt.title('Density Plot of Test Scores (Multiple Variables)')
plt.xlabel('Test Scores')
plt.ylabel('Density')
plt.legend()
plt.tight_layout()
plt.show()
"""

EXPECTED_OUTPUT = """\
Expected Visual Output:
1. Figure 1 (Single Variable):
   - Smooth bell curve centered at x = 75 with steelblue filled area beneath.
   - Peak density ~0.04 near the mean.

2. Figure 2 (Multiple Variables):
   - Two overlapping KDE curves with semi-transparent fills:
     * Steelblue curve: Maths scores centered at ~75.
     * Orange curve: Science scores shifted left to ~65 with wider base reflecting higher variance.
"""

RESULT = (
    "Single-variable and multiple-variable density plots were successfully generated "
    "using Seaborn and Matplotlib."
)

NOTES = """\
Dependencies:
- Uses seaborn.kdeplot() with fill=True for filled area under the curve.
- Fixed seed (0) guarantees identical curves for academic verification.\
"""


def run(show: bool = True, side_by_side: bool = False) -> Any:
    """Execute Experiment 6: Render single and multi-variable density plots."""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        import numpy as np
    except ImportError as exc:
        raise ImportError(
            f"Missing required visualization dependencies: {exc}.\n"
            "Install with: pip install dva-lab[viz] or pip install matplotlib seaborn numpy"
        ) from exc

    np.random.seed(0)
    scores = np.random.normal(loc=75, scale=10, size=100)
    maths = np.random.normal(loc=75, scale=10, size=100)
    science = np.random.normal(loc=65, scale=12, size=100)

    if side_by_side:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

        sns.kdeplot(scores, color="steelblue", fill=True, ax=ax1)
        ax1.set_title("Density Plot of Test Scores (Single Variable)")
        ax1.set_xlabel("Test Scores")
        ax1.set_ylabel("Density")
        ax1.grid(True, linestyle="--", alpha=0.5)

        sns.kdeplot(maths, color="steelblue", fill=True, label="Maths", ax=ax2)
        sns.kdeplot(science, color="orange", fill=True, label="Science", ax=ax2)
        ax2.set_title("Density Plot of Test Scores (Multiple Variables)")
        ax2.set_xlabel("Test Scores")
        ax2.set_ylabel("Density")
        ax2.legend()
        ax2.grid(True, linestyle="--", alpha=0.5)

        fig.tight_layout()
        if show:
            plt.show()
        return fig
    else:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        sns.kdeplot(scores, color="steelblue", fill=True, ax=ax1)
        ax1.set_title("Density Plot of Test Scores (Single Variable)")
        ax1.set_xlabel("Test Scores")
        ax1.set_ylabel("Density")
        ax1.grid(True, linestyle="--", alpha=0.5)
        fig1.tight_layout()
        if show:
            plt.show()

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.kdeplot(maths, color="steelblue", fill=True, label="Maths", ax=ax2)
        sns.kdeplot(science, color="orange", fill=True, label="Science", ax=ax2)
        ax2.set_title("Density Plot of Test Scores (Multiple Variables)")
        ax2.set_xlabel("Test Scores")
        ax2.set_ylabel("Density")
        ax2.legend()
        ax2.grid(True, linestyle="--", alpha=0.5)
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
