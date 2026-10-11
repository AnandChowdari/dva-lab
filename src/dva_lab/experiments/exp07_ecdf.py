"""Experiment 7: Empirical Cumulative Distribution Function (ECDF) plot."""

from typing import Any, Optional
from .base import Experiment

NUMBER = 7
TITLE = "Empirical Cumulative Distribution Function (ECDF) Plot"
CATEGORY = "Data Visualization (Python)"
AIM = "Write a Python program to implement an Empirical Cumulative Distribution Function (ECDF) plot."
DEPENDENCIES = ["matplotlib", "numpy", "statsmodels"]

CONCEPT = """\
The Empirical Cumulative Distribution Function (ECDF) is a fundamental non-parametric statistic \
estimating the underlying cumulative distribution function (CDF):
- For a sample of size n, F_n(x) computes the proportion of observations less than or equal to x:
  F_n(x) = (1 / n) * sum(I(x_i <= x))
- Advantage: Requires zero tuning parameters (no bin width or bandwidth choices like histograms/KDE), \
making it completely objective and resistant to bias.
- Plotted as a monotonic step function ranging from 0 to 1.\
"""

CODE = """\
# ============================================================================
# Experiment 7: Empirical Cumulative Distribution Function (ECDF) Plot
# Libraries: matplotlib, numpy, statsmodels
# ============================================================================

import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# Generate Reproducible Sample Data
np.random.seed(0)
data = np.random.normal(0, 1, 100)

# Compute ECDF Using Statsmodels
ecdf = sm.distributions.ECDF(data)
x = np.linspace(min(data), max(data), num=200)
y = ecdf(x)

# Plot ECDF as Step Function
plt.figure(figsize=(6, 4))
plt.step(x, y, color='steelblue', where='post', linewidth=1.5)
plt.xlabel('X-axis Label')
plt.ylabel('ECDF')
plt.title('Empirical Cumulative Distribution Function (ECDF)')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
"""

EXPECTED_OUTPUT = """\
Expected Visual Output:
- Monotonically increasing S-shaped step curve starting near (x ~ -2.5, y = 0) and plateauing at (x ~ 2.5, y = 1.0).
- At x = 0 (the mean of standard normal), the ECDF value is approximately 0.50.
- Grid lines enabled across both axes.
"""

RESULT = (
    "The Empirical Cumulative Distribution Function (ECDF) plot was successfully "
    "computed using statsmodels and rendered with Matplotlib."
)

NOTES = """\
Usage Notes:
- Requires statsmodels.api.distributions.ECDF.
- Plotted via plt.step() to reflect the exact discrete step nature of empirical cumulative probabilities.\
"""


def run(show: bool = True, seed: int = 0) -> Any:
    """Execute Experiment 7: Compute and plot ECDF."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import statsmodels.api as sm
    except ImportError as exc:
        raise ImportError(
            f"Missing required visualization dependencies: {exc}.\n"
            "Install with: pip install dva-lab[viz] or pip install matplotlib numpy statsmodels"
        ) from exc

    np.random.seed(seed)
    data = np.random.normal(0, 1, 100)
    ecdf = sm.distributions.ECDF(data)
    x = np.linspace(min(data), max(data), num=200)
    y = ecdf(x)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.step(x, y, color="steelblue", where="post", linewidth=1.5)
    ax.set_xlabel("X-axis Label")
    ax.set_ylabel("ECDF")
    ax.set_title("Empirical Cumulative Distribution Function (ECDF)")
    ax.grid(True, linestyle="--", alpha=0.6)
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
