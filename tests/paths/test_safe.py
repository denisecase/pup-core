"""Tests for safe repository-relative paths."""

from pathlib import Path

import pytest

from pup_core.base.errors import UnsafePathError
from pup_core.paths.safe import safe_repo_path


def test_safe_repo_path_resolves_inside_repository(tmp_path: Path) -> None:
    """Resolve an ordinary repository-relative path."""
    result = safe_repo_path(tmp_path, "src/example/cli.py")

    assert result == (tmp_path / "src" / "example" / "cli.py").resolve()


def test_safe_repo_path_rejects_parent_escape(tmp_path: Path) -> None:
    """Reject a path that escapes the repository root."""
    with pytest.raises(UnsafePathError):
        safe_repo_path(tmp_path, "../outside.txt")


def test_safe_repo_path_rejects_absolute_path(tmp_path: Path) -> None:
    """Reject absolute paths."""
    absolute = (tmp_path.parent / "outside.txt").resolve()

    with pytest.raises(UnsafePathError):
        safe_repo_path(tmp_path, absolute)
