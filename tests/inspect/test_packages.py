"""Tests for Python package inspection."""

from pathlib import Path

from pup_core.inspect.packages import (
    detect_packages,
    detect_primary_package,
    module_exists,
)


def test_detect_src_layout_package(tmp_path: Path) -> None:
    """Detect a package beneath src/."""
    package = tmp_path / "src" / "example"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")

    info = detect_packages(tmp_path)

    assert info.src_layout is True
    assert info.packages == ("example",)
    assert info.primary_package == "example"


def test_detect_multiple_packages_sorted(tmp_path: Path) -> None:
    """Detected packages use deterministic ordering."""
    for name in ("zebra", "alpha"):
        package = tmp_path / "src" / name
        package.mkdir(parents=True)
        (package / "__init__.py").write_text("", encoding="utf-8")

    info = detect_packages(tmp_path)

    assert info.packages == ("alpha", "zebra")
    assert info.primary_package == "alpha"


def test_detect_primary_package_without_src_layout(tmp_path: Path) -> None:
    """Detect a package located directly beneath the repository root."""
    package = tmp_path / "example"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")

    assert detect_primary_package(tmp_path) == "example"


def test_detect_primary_package_when_none_exists(tmp_path: Path) -> None:
    """Return an empty name when no package is detected."""
    assert detect_primary_package(tmp_path) == ""


def test_module_exists_for_python_module(tmp_path: Path) -> None:
    """Recognize a Python module beneath src/."""
    package = tmp_path / "src" / "example"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "cli.py").write_text("", encoding="utf-8")

    assert module_exists(tmp_path, "example.cli") is True
    assert module_exists(tmp_path, "example.missing") is False


def test_module_exists_for_package(tmp_path: Path) -> None:
    """Recognize a package by its __init__.py file."""
    package = tmp_path / "src" / "example" / "tools"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")

    assert module_exists(tmp_path, "example.tools") is True
