"""Jupyter Notebook / IPython magic commands extension for dva-lab."""

import sys
from typing import Optional

try:
    from IPython.core.magic import Magics, magics_class, line_magic
    from IPython.core.interactiveshell import InteractiveShell
    IPYTHON_AVAILABLE = True
except ImportError:
    IPYTHON_AVAILABLE = False

    class Magics:  # type: ignore
        def __init__(self, shell=None):
            self.shell = shell

    def line_magic(func):  # type: ignore
        return func

    def magics_class(cls):  # type: ignore
        return cls


@magics_class
class DVALabMagics(Magics):
    """IPython magic commands for interacting with DVA Lab experiments."""

    @line_magic
    def load_code(self, line: str) -> None:
        """%load_code <id> [--refresh]

        Fetch experiment code by ID and inject it directly into the active Jupyter cell,
        replacing the cell contents just like %load does.
        """
        self.load_experiment(line)

    @line_magic
    def load_experiment(self, line: str) -> None:
        """%load_experiment <id> [--refresh]

        Fetch experiment code by ID and inject it directly into the active Jupyter cell.
        """
        args = line.strip().split()
        if not args:
            print("Usage: %load_experiment <id> [--refresh] (e.g. %load_experiment 3)")
            return

        exp_id = None
        refresh = False

        for arg in args:
            if arg in ("--refresh", "-r"):
                refresh = True
            elif exp_id is None:
                exp_id = arg

        if exp_id is None:
            print("Error: Missing experiment ID. Usage: %load_experiment <id>")
            return

        try:
            from .core import get_code
            source = get_code(exp_id, refresh=refresh)
            if self.shell and hasattr(self.shell, "set_next_input"):
                self.shell.set_next_input(str(source), replace=True)
            else:
                print(str(source))
        except Exception as e:
            print(f"DVA Lab Error: {e}", file=sys.stderr)

    @line_magic
    def show_experiment(self, line: str) -> None:
        """%show_experiment <id> [--refresh]

        Display full Markdown manual for an experiment.
        """
        args = line.strip().split()
        if not args:
            print("Usage: %show_experiment <id> (e.g. %show_experiment 1)")
            return

        exp_id = args[0]
        refresh = "--refresh" in args or "-r" in args

        try:
            from .core import show_experiment
            show_experiment(exp_id, refresh=refresh)
        except Exception as e:
            print(f"DVA Lab Error: {e}", file=sys.stderr)

    @line_magic
    def list_experiments(self, line: str) -> None:
        """%list_experiments [--refresh]

        Display table of all 12 DVA experiments.
        """
        refresh = "--refresh" in line or "-r" in line
        try:
            from .core import list_experiments
            list_experiments(refresh=refresh)
        except Exception as e:
            print(f"DVA Lab Error: {e}", file=sys.stderr)

    @line_magic
    def run_experiment(self, line: str) -> None:
        """%run_experiment <id>

        Run the specified experiment inline.
        """
        args = line.strip().split()
        if not args:
            print("Usage: %run_experiment <id> (e.g. %run_experiment 3)")
            return
        try:
            from .core import run_experiment
            exp_id = int(args[0])
            run_experiment(exp_id)
        except Exception as e:
            print(f"DVA Lab Error: {e}", file=sys.stderr)


def load_ipython_extension(ipython) -> None:
    """Register magic commands when loaded via %load_ext dva_lab."""
    magics = DVALabMagics(ipython)
    ipython.register_magics(magics)


def unload_ipython_extension(ipython) -> None:
    """Cleanup when extension is unloaded."""
    pass
