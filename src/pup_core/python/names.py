"""Python project and package name normalization."""

import re

__all__ = [
    "canonical_distribution_name",
    "distribution_to_import_name",
    "normalize_import_name",
]


_SEPARATOR_RE = re.compile(r"[-_.]+")


def canonical_distribution_name(name: str) -> str:
    """Return the canonical comparison form of a distribution name."""
    return _SEPARATOR_RE.sub("-", name).lower()


def distribution_to_import_name(name: str) -> str:
    """Convert a distribution name to its conventional import-name form."""
    return _SEPARATOR_RE.sub("_", name).lower()


def normalize_import_name(name: str) -> str:
    """Normalize a dotted Python import name for comparison."""
    return ".".join(
        distribution_to_import_name(part) for part in name.strip().split(".") if part
    )
