"""Unit tests for experiment registry and metadata integrity."""

import pytest
import sys
from pathlib import Path

# Add src to path for direct testing
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import dva_lab
from dva_lab.registry import registry, ExperimentList


def test_registry_contains_all_twelve_experiments():
    """Verify that exactly 12 experiments are registered."""
    experiments = dva_lab.list_experiments()
    assert len(experiments) == 12
    assert isinstance(experiments, ExperimentList)

    numbers = [exp.number for exp in experiments]
    assert numbers == list(range(1, 13))


@pytest.mark.parametrize("number", range(1, 13))
def test_experiment_metadata_completeness(number):
    """Ensure every experiment has complete, non-empty metadata fields."""
    exp = registry.get(number)

    assert exp.number == number
    assert exp.title and isinstance(exp.title, str)
    assert exp.category and isinstance(exp.category, str)
    assert exp.aim and isinstance(exp.aim, str)
    assert exp.concept and isinstance(exp.concept, str)
    assert exp.code and isinstance(exp.code, str)
    assert isinstance(exp.dependencies, list) and len(exp.dependencies) > 0
    assert exp.expected_output and isinstance(exp.expected_output, str)
    assert exp.result and isinstance(exp.result, str)


@pytest.mark.parametrize("invalid_num", [0, 13, -1, 100, "three", None])
def test_invalid_experiment_number_raises_value_error(invalid_num):
    """Verify invalid experiment numbers raise a helpful ValueError."""
    with pytest.raises(ValueError) as excinfo:
        registry.get(invalid_num)
    assert "Invalid experiment number" in str(excinfo.value) or "Valid" in str(excinfo.value)


def test_experiment_list_representations():
    """Test HTML, Markdown, dictionary, and dataframe representations."""
    exp_list = dva_lab.list_experiments()

    # Dictionary conversion
    data_dicts = exp_list.to_dict()
    assert len(data_dicts) == 12
    assert data_dicts[0]["Number"] == 1
    assert "OLAP" in data_dicts[0]["Title"]

    # Markdown representation
    md_repr = exp_list._repr_markdown_()
    assert "| # | Title | Category | Aim |" in md_repr
    assert "| **1** |" in md_repr

    # HTML representation
    html_repr = exp_list._repr_html_()
    assert "<table" in html_repr
    assert "OLAP" in html_repr

    # String / CLI representation
    cli_repr = repr(exp_list)
    assert "#" in cli_repr
    assert "Vertical and Horizontal Bar Charts" in cli_repr

    # DataFrame representation
    df = exp_list.to_dataframe()
    assert len(df) == 12
