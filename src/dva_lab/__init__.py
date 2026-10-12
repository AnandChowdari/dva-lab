"""dva-lab: Data Visualization and Analytics Laboratory Python Package.

A cloud-synchronized Python library for retrieving, displaying, and executing
DVA lab experiments directly inside Jupyter Notebook, JupyterLab, Google Colab,
and standalone scripts.
"""

from .config import configure, get_config, reset_config
from .core import (
    list_experiments,
    show_experiment,
    get_code,
    show_code,
    code,
    run_experiment,
    search,
    get_info,
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
from .exceptions import (
    DVALabError,
    ExperimentNotFoundError,
    RepositoryNotFoundError,
    RemoteFetchError,
    ConfigurationError,
    ExecutionEnvironmentError,
)
from .jupyter_extension import load_ipython_extension, unload_ipython_extension

__version__ = "0.2.1"
__author__ = "Anand Chowdari"

__all__ = [
    "configure",
    "get_config",
    "reset_config",
    "list_experiments",
    "show_experiment",
    "get_code",
    "show_code",
    "code",
    "run_experiment",
    "search",
    "get_info",
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
    "load_sales_data",
    "get_sales_data_path",
    "registry",
    "about",
    "help",
    "DVALabError",
    "ExperimentNotFoundError",
    "RepositoryNotFoundError",
    "RemoteFetchError",
    "ConfigurationError",
    "ExecutionEnvironmentError",
    "load_ipython_extension",
    "unload_ipython_extension",
]

# Auto-register IPython magic extension when inside an active IPython session
try:
    from IPython import get_ipython
    _ip = get_ipython()
    if _ip is not None:
        load_ipython_extension(_ip)
except Exception:
    pass
