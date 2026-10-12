"""Command-Line Interface for the dva-lab package."""

import argparse
import sys
from pathlib import Path

from .config import configure, get_config, reset_config
from .core import (
    list_experiments,
    show_experiment,
    get_code,
    run_experiment,
    search,
    about,
)
from .exceptions import DVALabError


def main(args=None) -> int:
    """Main CLI entrypoint for dva-lab."""
    parser = argparse.ArgumentParser(
        prog="dva-lab",
        description="DVA Lab: Retrieve, display, and run Data Visualization & Analytics experiments.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: list
    list_p = subparsers.add_parser("list", help="List all 12 DVA experiments")
    list_p.add_argument("--refresh", "-r", action="store_true", help="Refresh catalog from GitHub")

    # Command: show
    show_p = subparsers.add_parser("show", help="Display full manual for an experiment")
    show_p.add_argument("id", type=int, help="Experiment number (1-12)")
    show_p.add_argument("--refresh", "-r", action="store_true", help="Refresh from GitHub")

    # Command: get
    get_p = subparsers.add_parser("get", help="Print or download experiment source code")
    get_p.add_argument("id", type=int, help="Experiment number (1-12)")
    get_p.add_argument("--output", "-o", type=str, default=None, help="Save to destination file")
    get_p.add_argument("--refresh", "-r", action="store_true", help="Refresh from GitHub")

    # Command: run
    run_p = subparsers.add_parser("run", help="Execute an experiment (Python plots or instructions)")
    run_p.add_argument("id", type=int, help="Experiment number (1-12)")

    # Command: search
    search_p = subparsers.add_parser("search", help="Search experiments by query string")
    search_p.add_argument("query", type=str, help="Search term (e.g. 'bar', 'sql', 'dax')")

    # Command: config
    cfg_p = subparsers.add_parser("config", help="View or modify GitHub repository settings")
    cfg_p.add_argument("--username", "-u", type=str, help="GitHub username")
    cfg_p.add_argument("--repository", "-repo", type=str, help="GitHub repository name")
    cfg_p.add_argument("--branch", "-b", type=str, help="Git branch name")
    cfg_p.add_argument("--timeout", "-t", type=float, help="Network timeout in seconds")
    cfg_p.add_argument("--persist", action="store_true", help="Save permanently to config file")

    # Command: info
    subparsers.add_parser("info", help="Display version and repository information")

    parsed = parser.parse_args(args)

    if not parsed.command:
        parser.print_help()
        return 0

    try:
        if parsed.command == "list":
            exp_list = list_experiments(refresh=parsed.refresh)
            print(repr(exp_list))

        elif parsed.command == "show":
            show_experiment(parsed.id, refresh=parsed.refresh)

        elif parsed.command == "get":
            code = get_code(parsed.id, refresh=parsed.refresh)
            if parsed.output:
                out_path = Path(parsed.output)
                out_path.write_text(str(code), encoding="utf-8")
                print(f"Saved experiment {parsed.id} code to {out_path.resolve()}")
            else:
                print(code)

        elif parsed.command == "run":
            run_experiment(parsed.id)

        elif parsed.command == "search":
            results = search(parsed.query)
            if not results:
                print(f"No experiments found matching: '{parsed.query}'")
            else:
                print(f"Found {len(results)} matching experiment(s):")
                for r in results:
                    print(f"  [{r['id']:>2}] {r['title']} ({r['category']})")

        elif parsed.command == "config":
            if any([parsed.username, parsed.repository, parsed.branch, parsed.timeout]):
                cfg = configure(
                    username=parsed.username,
                    repository=parsed.repository,
                    branch=parsed.branch,
                    timeout=parsed.timeout,
                    persist=parsed.persist,
                )
                print("Configuration updated:")
            else:
                cfg = get_config()
                print("Active Configuration:")
            for k, v in cfg.to_dict().items():
                print(f"  {k}: {v}")

        elif parsed.command == "info":
            about()

        return 0
    except DVALabError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
