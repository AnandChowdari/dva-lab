"""Tests for CLI commands, Jupyter extension, and dvalab module alias."""

import io
import sys
import pytest
from pathlib import Path

import dva_lab
import dvalab
from dva_lab.cli import main as cli_main
from dva_lab.jupyter_extension import DVALabMagics


def test_dvalab_alias():
    """Verify dvalab alias exports the same API as dva_lab."""
    assert dvalab.configure is dva_lab.configure
    assert dvalab.list_experiments is dva_lab.list_experiments
    assert dvalab.get_code is dva_lab.get_code
    assert dvalab.show_experiment is dva_lab.show_experiment
    assert dvalab.run_experiment is dva_lab.run_experiment
    assert dvalab.__version__ == dva_lab.__version__


def test_cli_list(capsys):
    """Test 'dva-lab list' command."""
    code = cli_main(["list"])
    assert code == 0
    captured = capsys.readouterr()
    assert "OLAP" in captured.out
    assert "Bar Charts" in captured.out


def test_cli_show(capsys):
    """Test 'dva-lab show 3' command."""
    code = cli_main(["show", "3"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Experiment 3" in captured.out
    assert "Aim" in captured.out


def test_cli_get(capsys, tmp_path):
    """Test 'dva-lab get 3' printing and saving to file."""
    # Print to console
    code = cli_main(["get", "3"])
    assert code == 0
    captured = capsys.readouterr()
    assert "plt.bar" in captured.out

    # Save to file
    out_file = tmp_path / "test_exp3.py"
    code2 = cli_main(["get", "3", "--output", str(out_file)])
    assert code2 == 0
    assert out_file.exists()
    assert "plt.bar" in out_file.read_text(encoding="utf-8")


def test_cli_search(capsys):
    """Test 'dva-lab search' command."""
    code = cli_main(["search", "scatter"])
    assert code == 0
    captured = capsys.readouterr()
    assert "Scatter Plot" in captured.out


def test_cli_config(capsys):
    """Test 'dva-lab config' command."""
    code = cli_main(["config", "--username", "CLIUser", "--repository", "CLI-repo"])
    assert code == 0
    captured = capsys.readouterr()
    assert "CLIUser" in captured.out
    assert "CLI-repo" in captured.out


def test_jupyter_magics():
    """Test Jupyter magic commands with mock shell."""
    shell_mock = type("MockShell", (), {"set_next_input": lambda self, text, replace=True: None})()
    magics = DVALabMagics(shell_mock)

    # Test load_code magic
    magics.load_code("3")
    # Test show_experiment magic
    magics.show_experiment("3")
    # Test list_experiments magic
    magics.list_experiments("")
