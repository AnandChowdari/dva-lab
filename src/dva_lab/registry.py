"""Experiment registry and lookup services for DVA Lab."""

from typing import List, Dict, Any, Optional
from .experiments.base import Experiment
from .experiments import EXPERIMENTS


class ExperimentList(list):
    """Rich container for the list of experiments supporting Jupyter display and table rendering."""

    def __init__(self, experiments: List[Experiment]):
        super().__init__(experiments)

    def to_dict(self) -> List[Dict[str, Any]]:
        """Return list of experiment summaries as dictionaries."""
        return [
            {
                "Number": exp.number,
                "Title": exp.title,
                "Category": exp.category,
                "Aim": exp.aim,
            }
            for exp in self
        ]

    def to_dataframe(self) -> Any:
        """Convert experiments list to a pandas DataFrame if pandas is installed."""
        try:
            import pandas as pd
            return pd.DataFrame(self.to_dict())
        except ImportError:
            return self.to_dict()

    def _repr_html_(self) -> str:
        """Render a styled HTML table in Jupyter Notebook."""
        rows = "".join(
            f"<tr>"
            f"<td style='text-align:center;font-weight:bold;'>{exp.number}</td>"
            f"<td style='text-align:left;font-weight:600;'>{exp.title}</td>"
            f"<td style='text-align:left;'><span style='background-color:#eef2ff;color:#3730a3;padding:2px 8px;border-radius:12px;font-size:0.85em;'>{exp.category}</span></td>"
            f"<td style='text-align:left;font-size:0.9em;color:#4b5563;'>{exp.aim}</td>"
            f"</tr>"
            for exp in self
        )
        return (
            "<div style='overflow-x:auto;'>"
            "<table style='border-collapse:collapse;width:100%;font-family:sans-serif;margin:1em 0;box-shadow:0 1px 3px rgba(0,0,0,0.1);'>"
            "<thead style='background-color:#1e293b;color:#ffffff;'>"
            "<tr>"
            "<th style='padding:10px;text-align:center;'>#</th>"
            "<th style='padding:10px;text-align:left;'>Title</th>"
            "<th style='padding:10px;text-align:left;'>Category</th>"
            "<th style='padding:10px;text-align:left;'>Aim</th>"
            "</tr>"
            "</thead>"
            f"<tbody>{rows}</tbody>"
            "</table>"
            "</div>"
        )

    def _repr_markdown_(self) -> str:
        """Render a Markdown table in Jupyter."""
        lines = [
            "| # | Title | Category | Aim |",
            "|---|---|---|---|",
        ]
        for exp in self:
            lines.append(f"| **{exp.number}** | {exp.title} | `{exp.category}` | {exp.aim} |")
        return "\n".join(lines)

    def __repr__(self) -> str:
        """Render an aligned ASCII table for standard terminal/console output."""
        header = f"{'#':<3} | {'Title':<45} | {'Category':<30} | Aim"
        sep = "-" * len(header)
        rows = [header, sep]
        for exp in self:
            aim_snippet = (exp.aim[:40] + "...") if len(exp.aim) > 43 else exp.aim
            rows.append(f"{exp.number:<3} | {exp.title:<45} | {exp.category:<30} | {aim_snippet}")
        return "\n".join(rows)


class ExperimentRegistry:
    """Manages the complete catalog of 12 DVA experiments."""

    def __init__(self):
        self._experiments: Dict[int, Experiment] = EXPERIMENTS

    def get(self, number: int) -> Experiment:
        """Retrieve an experiment by its integer index (1 to 12).

        Raises:
            ValueError: If number is not an integer between 1 and 12.
        """
        if not isinstance(number, int) or number < 1 or number > 12:
            raise ValueError(
                f"Invalid experiment number: {number}. "
                "Valid experiment numbers are integers from 1 to 12."
            )
        if number not in self._experiments:
            raise ValueError(f"Experiment {number} is not registered.")
        return self._experiments[number]

    def all(self) -> ExperimentList:
        """Return an ExperimentList containing all 12 experiments ordered by number."""
        ordered = [self._experiments[i] for i in sorted(self._experiments.keys())]
        return ExperimentList(ordered)


registry = ExperimentRegistry()
