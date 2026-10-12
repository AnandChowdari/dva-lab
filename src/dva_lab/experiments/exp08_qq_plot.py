"""Experiment 8: Q-Q (Quantile-Quantile) Plot."""

from typing import Any, Optional
from .base import Experiment

NUMBER = 8
TITLE = "Q-Q (Quantile-Quantile) Plot"
CATEGORY = "Data Visualization (Python)"
AIM = "Write a Python program to implement a Q-Q (quantile-quantile) plot to compare two datasets."
DEPENDENCIES = ["matplotlib", "numpy"]

CONCEPT = """\
A Quantile-Quantile (Q-Q) plot compares the quantiles of two distributions against each other. \
If both follow the same distribution shape, the points fall along the diagonal line y = x.\
"""

CODE = """\
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
data1 = np.random.normal(0, 1, 1000)
data2 = np.random.normal(1, 1.5, 1000)

q1 = np.sort(data1)
q2 = np.sort(data2)

plt.figure(figsize=(6, 4))
plt.scatter(q1, q2, s=10, color='blue')
lims = [min(q1.min(), q2.min()), max(q1.max(), q2.max())]
plt.plot(lims, lims, 'r--', label='y = x (same distribution)')
plt.xlabel('Quantiles of Dataset 1')
plt.ylabel('Quantiles of Dataset 2')
plt.title('Q-Q Plot to Compare Two Datasets')
plt.legend()
plt.show()
"""

OUTPUT = """\
Q-Q plot comparing two normal datasets generated.
"""


class Exp08QQPlot(Experiment):
    number = NUMBER
    title = TITLE
    category = CATEGORY
    aim = AIM
    concept = CONCEPT
    code = CODE
    output = OUTPUT
    dependencies = DEPENDENCIES

    def run(self, **kwargs: Any) -> Optional[Any]:
        import numpy as np
        import matplotlib.pyplot as plt

        np.random.seed(0)
        data1 = np.random.normal(0, 1, 1000)
        data2 = np.random.normal(1, 1.5, 1000)
        q1 = np.sort(data1)
        q2 = np.sort(data2)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(q1, q2, s=10, color='blue')
        lims = [min(q1.min(), q2.min()), max(q1.max(), q2.max())]
        ax.plot(lims, lims, 'r--', label='y = x (same distribution)')
        ax.set_xlabel('Quantiles of Dataset 1')
        ax.set_ylabel('Quantiles of Dataset 2')
        ax.set_title('Q-Q Plot to Compare Two Datasets')
        ax.legend()
        return fig
