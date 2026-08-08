"""Command modules for pup-core.

Each command module exposes a stable run(...) -> int entry point.

The CLI parser lives in pup_core.cli.
Behavior lives here.
"""

from pup_core.commands import update

__all__ = ["update"]
