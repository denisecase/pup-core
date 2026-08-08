"""Tests for Python version normalization."""

from pup_core.python.versions import (
    minimum_python_version,
    normalize_python_version,
    python_version_to_ruff_target,
    ruff_target_to_python_version,
)


def test_normalize_python_version() -> None:
    """Normalize version declarations to major.minor."""
    assert normalize_python_version("Python 3.15.0") == "3.15"
    assert normalize_python_version(">=3.14") == "3.14"


def test_normalize_invalid_python_version() -> None:
    """Return empty text when no Python version can be identified."""
    assert normalize_python_version("latest") == ""


def test_minimum_python_version() -> None:
    """Extract the first version from requires-python."""
    assert minimum_python_version(">=3.15") == "3.15"


def test_python_version_to_ruff_target() -> None:
    """Convert Python version syntax to Ruff target syntax."""
    assert python_version_to_ruff_target("3.15") == "py315"


def test_ruff_target_to_python_version() -> None:
    """Convert Ruff target syntax to Python version syntax."""
    assert ruff_target_to_python_version("py315") == "3.15"


def test_invalid_ruff_target() -> None:
    """Return empty text for an invalid Ruff target."""
    assert ruff_target_to_python_version("3.15") == ""
