"""Tests for shared exception types."""

from pathlib import Path

from pup_core.base.errors import (
    GitInspectionError,
    PupCoreError,
    PyprojectError,
    RepositoryDetectionError,
    SectionError,
    UnsafePathError,
)


def test_core_errors_inherit_from_pup_core_error() -> None:
    """Specialized core errors share the common base exception."""
    assert isinstance(RepositoryDetectionError("repository"), PupCoreError)
    assert isinstance(GitInspectionError("git"), PupCoreError)
    assert isinstance(PyprojectError("pyproject"), PupCoreError)
    assert isinstance(SectionError("section"), PupCoreError)


def test_unsafe_path_error_includes_path() -> None:
    """UnsafePathError identifies the rejected path."""
    path = Path("../outside")

    error = UnsafePathError(path)

    assert isinstance(error, PupCoreError)
    assert "../outside" in str(error).replace("\\", "/")
