"""Safe repository-relative path handling."""

from pathlib import Path

from pup_core.base.errors import UnsafePathError

__all__ = ["safe_repo_path"]


def safe_repo_path(root: Path, relative_path: str | Path) -> Path:
    """Resolve a repository-relative path without allowing escape."""
    root = root.resolve()
    candidate_input = Path(relative_path)

    if candidate_input.is_absolute():
        raise UnsafePathError(candidate_input)

    candidate = (root / candidate_input).resolve()

    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise UnsafePathError(candidate) from exc

    return candidate
