"""Shared exception types."""

from pathlib import Path

__all__ = [
    "GitInspectionError",
    "PupCoreError",
    "PyprojectError",
    "RepositoryDetectionError",
    "SectionError",
    "UnsafePathError",
]


class PupCoreError(Exception):
    """Base exception for pup-core."""


class RepositoryDetectionError(PupCoreError):
    """Raised when the target repository cannot be determined."""


class GitInspectionError(PupCoreError):
    """Raised when required Git repository information cannot be inspected."""


class PyprojectError(PupCoreError):
    """Raised when pyproject.toml cannot be read or interpreted."""


class UnsafePathError(PupCoreError):
    """Raised when a path would escape the target repository."""

    def __init__(self, path: Path) -> None:
        """Initialize the error."""
        super().__init__(f"Unsafe path escapes repository root: {path}")


class SectionError(PupCoreError):
    """Raised when a managed file section is malformed or ambiguous."""
