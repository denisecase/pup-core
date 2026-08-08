"""Tests for repository path normalization."""

from pathlib import Path

from pup_core.paths.normalize import normalize_repo_path


def test_normalize_windows_separators() -> None:
    """Convert backslashes to repository-standard forward slashes."""
    assert normalize_repo_path(r"src\example\cli.py") == "src/example/cli.py"


def test_normalize_path_object() -> None:
    """Normalize pathlib paths."""
    path = Path("src") / "example" / "cli.py"

    assert normalize_repo_path(path) == "src/example/cli.py"


def test_normalize_current_directory() -> None:
    """Represent the current directory as an empty repository path."""
    assert normalize_repo_path(".") == ""
