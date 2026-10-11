"""Experiments package for DVA Lab."""

from typing import Dict
from .base import Experiment
from . import exp01_olap
from . import exp02_star_schema
from . import exp03_bar_charts
from . import exp04_grouped_stacked
from . import exp05_histograms
from . import exp06_density
from . import exp07_ecdf
from . import exp08_qq_plot
from . import exp09_scatter
from . import exp10_powerbi_visualization
from . import exp11_powerbi_dax
from . import exp12_powerbi_logic

MODULES = [
    exp01_olap,
    exp02_star_schema,
    exp03_bar_charts,
    exp04_grouped_stacked,
    exp05_histograms,
    exp06_density,
    exp07_ecdf,
    exp08_qq_plot,
    exp09_scatter,
    exp10_powerbi_visualization,
    exp11_powerbi_dax,
    exp12_powerbi_logic,
]

EXPERIMENTS: Dict[int, Experiment] = {
    mod.NUMBER: mod.get_experiment() for mod in MODULES
}

__all__ = [
    "Experiment",
    "EXPERIMENTS",
    "MODULES",
    "exp01_olap",
    "exp02_star_schema",
    "exp03_bar_charts",
    "exp04_grouped_stacked",
    "exp05_histograms",
    "exp06_density",
    "exp07_ecdf",
    "exp08_qq_plot",
    "exp09_scatter",
    "exp10_powerbi_visualization",
    "exp11_powerbi_dax",
    "exp12_powerbi_logic",
]
