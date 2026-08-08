"""Tests for Python project and package name normalization."""

from pup_core.python.names import (
    canonical_distribution_name,
    distribution_to_import_name,
    normalize_import_name,
)


def test_canonical_distribution_name() -> None:
    """Normalize Python distribution names for comparison."""
    assert canonical_distribution_name("My_Package.Name") == "my-package-name"


def test_distribution_to_import_name() -> None:
    """Convert distribution separators to import-name underscores."""
    assert distribution_to_import_name("my-package.name") == "my_package_name"


def test_normalize_import_name() -> None:
    """Normalize each component of a dotted import name."""
    assert normalize_import_name("My-Package.Sub_Package") == "my_package.sub_package"
