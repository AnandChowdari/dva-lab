"""Base data structures and interfaces for DVA Lab experiments."""

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Any, Dict


@dataclass
class Experiment:
    """Represents a DVA laboratory experiment with all metadata and executable logic."""

    number: int
    title: str
    category: str
    aim: str
    concept: str
    code: str
    dependencies: List[str] = field(default_factory=list)
    expected_output: str = ""
    result: str = ""
    notes: str = ""
    run_func: Optional[Callable[..., Any]] = None

    def run(self, **kwargs) -> Any:
        """Execute the experiment or display execution instructions."""
        if self.run_func is not None:
            return self.run_func(**kwargs)
        raise NotImplementedError(
            f"Execution logic is not defined for Experiment {self.number}: {self.title}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert experiment metadata to a dictionary."""
        return {
            "number": self.number,
            "title": self.title,
            "category": self.category,
            "aim": self.aim,
            "concept": self.concept,
            "dependencies": self.dependencies,
            "expected_output": self.expected_output,
            "result": self.result,
            "notes": self.notes,
        }
