"""Repository path normalization."""

from pathlib import Path, PurePosixPath

__all__ = ["normalize_repo_path"]


def normalize_repo_path(path: str | Path) -> str:
    """Return a repository path using normalized POSIX separators."""
    value = str(path).replace("\\", "/")
    normalized = PurePosixPath(value)

    if str(normalized) == ".":
        return ""

    return normalized.as_posix()
