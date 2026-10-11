"""Experiment 8: Q-Q plot to compare datasets."""

from typing import Any, Optional
from .base import Experiment

NUMBER = 8
TITLE = "Q-Q Plot to Compare Datasets"
CATEGORY = "Data Visualization (Python)"
AIM = "Write a Python program to implement a Q-Q (quantile-quantile) plot to compare two datasets."
DEPENDENCIES = ["matplotlib", "numpy", "scipy"]

CONCEPT = """\
A Quantile-Quantile (Q-Q) plot is a graphical diagnostic tool that plots quantiles of sample data \
against theoretical reference quantiles (typically standard normal N(0, 1)):
- Linearity: If the sample follows the theoretical distribution, points fall closely along a straight 45-degree reference line.
- Slope & Intercept: The slope of the reference line corresponds to sample standard deviation, \
while the intercept corresponds to the sample mean.
- Curvature & Tail Diagnostics: Curvature at extremes reveals distribution characteristics \
such as fat/heavy tails, skewness, or bounded support.\
"""

CODE = """\
# ============================================================================
# Experiment 8: Q-Q Plot to Compare Two Datasets
# Libraries: matplotlib, numpy, scipy
# ============================================================================

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# Generate Two Normal Datasets with Different Means and Variances
np.random.seed(0)
data1 = np.random.normal(0, 1, 1000)      # Mean=0, Std=1
data2 = np.random.normal(1, 1.5, 1000)    # Mean=1, Std=1.5

# Render Q-Q Plot Against Theoretical Normal Quantiles
plt.figure(figsize=(6, 4))
stats.probplot(data1, dist="norm", plot=plt)
stats.probplot(data2, dist="norm", plot=plt)
plt.title('Q-Q Plot to Compare Two Datasets')
plt.xlabel('Theoretical Quantiles')
plt.ylabel('Sample Quantiles')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
"""

EXPECTED_OUTPUT = """\
Expected Visual Output:
- Two overlaid probability plot series against Theoretical Quantiles (spanning approx -3.5 to +3.5).
- Blue scatter points with red best-fit reference lines for each dataset.
- Dataset 1 (N(0, 1)) aligns with a slope of 1 passing through origin.
- Dataset 2 (N(1, 1.5)) displays a steeper slope (~1.5) shifted upward with intercept at y = 1.
"""

RESULT = (
    "A Q-Q plot comparing two datasets was successfully generated and analyzed "
    "using SciPy stats and Matplotlib."
)

NOTES = """\
Usage Notes:
- Utilizes `scipy.stats.probplot(..., dist="norm", plot=plt)` to compute theoretical quantiles.
- Demonstrates how mean shift alters intercept and standard deviation alters slope.\
"""


def run(show: bool = True, seed: int = 0) -> Any:
    """Execute Experiment 8: Compute and plot Q-Q plot."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import scipy.stats as stats
    except ImportError as exc:
        raise ImportError(
            f"Missing required visualization dependencies: {exc}.\n"
            "Install with: pip install dva-lab[viz] or pip install matplotlib numpy scipy"
        ) from exc

    np.random.seed(seed)
    data1 = np.random.normal(0, 1, 1000)
    data2 = np.random.normal(1, 1.5, 1000)

    fig, ax = plt.subplots(figsize=(6, 4))
    stats.probplot(data1, dist="norm", plot=ax)
    stats.probplot(data2, dist="norm", plot=ax)
    ax.set_title("Q-Q Plot to Compare Two Datasets")
    ax.set_xlabel("Theoretical Quantiles")
    ax.set_ylabel("Sample Quantiles")
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
