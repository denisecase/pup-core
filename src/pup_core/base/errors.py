"""Shared exception types."""

from pathlib import Path

__all__ = [
    "PupCoreError",
    "RepositoryDetectionError",
    "UnsafePathError",
]


class PupCoreError(Exception):
    """Base exception."""


class RepositoryDetectionError(PupCoreError):
    """Raised when the target repository cannot be determined."""

    def __init__(self, message: str) -> None:
        """Initialize the error."""
        super().__init__(message)


class UnsafePathError(PupCoreError):
    """Raised when a path would escape the target repository."""

    def __init__(self, path: Path) -> None:
        """Initialize the error."""
        super().__init__(f"Unsafe path escapes repository root: {path}")
