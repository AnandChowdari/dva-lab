"""Experiment 7: Empirical Cumulative Distribution Function (ECDF)."""

from typing import Any, Optional
from .base import Experiment

NUMBER = 7
TITLE = "Empirical Cumulative Distribution Function (ECDF)"
CATEGORY = "Data Visualization (Python)"
AIM = "Write a Python program to implement an Empirical Cumulative Distribution Function (ECDF) plot."
DEPENDENCIES = ["matplotlib", "numpy"]

CONCEPT = """\
An Empirical Cumulative Distribution Function (ECDF) estimates the underlying cumulative \
distribution function of a sample by plotting sorted values against their cumulative fractions.\
"""

CODE = """\
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
data = np.random.normal(0, 1, 100)

x = np.sort(data)
y = np.arange(1, len(x) + 1) / len(x)

plt.figure(figsize=(6, 4))
plt.step(x, y, where='post')
plt.xlabel('Data Values')
plt.ylabel('ECDF')
plt.title('Empirical Cumulative Distribution Function (ECDF)')
plt.grid(True)
plt.show()
"""

OUTPUT = """\
ECDF step plot displayed successfully.
"""


class Exp07ECDF(Experiment):
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
        data = np.random.normal(0, 1, 100)
        x = np.sort(data)
        y = np.arange(1, len(x) + 1) / len(x)

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.step(x, y, where='post')
        ax.set_xlabel('Data Values')
        ax.set_ylabel('ECDF')
        ax.set_title('Empirical Cumulative Distribution Function (ECDF)')
        ax.grid(True)
        return fig
