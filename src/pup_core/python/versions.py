"""Python version normalization."""

import re

__all__ = [
    "minimum_python_version",
    "normalize_python_version",
    "python_version_to_ruff_target",
    "ruff_target_to_python_version",
]


_VERSION_RE = re.compile(r"(?P<major>\d+)\.(?P<minor>\d+)")
_RUFF_RE = re.compile(r"py(?P<major>\d)(?P<minor>\d+)$")


def normalize_python_version(value: str) -> str:
    """Normalize a Python version to major.minor form."""
    match = _VERSION_RE.search(value.strip())

    if match is None:
        return ""

    return f"{match.group('major')}.{match.group('minor')}"


def minimum_python_version(requires_python: str) -> str:
    """Extract the first major.minor version from requires-python."""
    return normalize_python_version(requires_python)


def python_version_to_ruff_target(version: str) -> str:
    """Convert a Python major.minor version to Ruff target form."""
    normalized = normalize_python_version(version)

    if not normalized:
        return ""

    major, minor = normalized.split(".", maxsplit=1)
    return f"py{major}{minor}"


def ruff_target_to_python_version(target: str) -> str:
    """Convert a Ruff target version to Python major.minor form."""
    match = _RUFF_RE.fullmatch(target.strip().lower())

    if match is None:
        return ""

    return f"{match.group('major')}.{match.group('minor')}"
