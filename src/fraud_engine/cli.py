"""Command-line interface for the Fraud Engine."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .orchestrator import Orchestrator


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fraud-engine",
        description="Agentic BFSI Fraud & Tokenization Engine.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"fraud-engine {__version__}",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Analyze a transaction.")
    run.add_argument("--tx", required=True, type=Path, help="Path to transaction JSON.")
    run.add_argument("--workdir", default=Path("out"), type=Path, help="Output directory.")
    
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command != "run":
        parser.print_help()
        sys.exit(2)

    if not args.tx.exists():
        print(f"[ERROR] Transaction file not found: {args.tx}", file=sys.stderr)
        sys.exit(2)

    orchestrator = Orchestrator(args.workdir)
    sys.exit(orchestrator.run(args.tx))


if __name__ == "__main__":
    main()
