"""dva-lab: Data Visualization and Analytics Laboratory Python Package.

A self-contained Python library for retrieving, displaying, and executing
DVA lab experiments directly inside Jupyter Notebook, JupyterLab, and Google Colab.
"""

from .core import (
    list_experiments,
    show_experiment,
    get_code,
    show_code,
    code,
    run_experiment,
    exp1,
    exp2,
    exp3,
    exp4,
    exp5,
    exp6,
    exp7,
    exp8,
    exp9,
    exp10,
    exp11,
    exp12,
    code1,
    code2,
    code3,
    code4,
    code5,
    code6,
    code7,
    code8,
    code9,
    code10,
    code11,
    code12,
    about,
    help,
)
from .experiments.exp10_powerbi_visualization import (
    get_sales_data_path,
    load_sales_data,
)
from .registry import registry

__version__ = "0.1.0"
__author__ = "DVA Lab"

__all__ = [
    "list_experiments",
    "show_experiment",
    "get_code",
    "show_code",
    "run_experiment",
    "exp1",
    "exp2",
    "exp3",
    "exp4",
    "exp5",
    "exp6",
    "exp7",
    "exp8",
    "exp9",
    "exp10",
    "exp11",
    "exp12",
    "code",
    "code1",
    "code2",
    "code3",
    "code4",
    "code5",
    "code6",
    "code7",
    "code8",
    "code9",
    "code10",
    "code11",
    "code12",
    "about",
    "help",
    "load_sales_data",
    "get_sales_data_path",
    "registry",
    "__version__",
]
