"""Python package inspection."""

from pathlib import Path

from pup_core.base.types import PackageInfo

__all__ = [
    "detect_packages",
    "detect_primary_package",
    "module_exists",
]


def detect_packages(root: Path) -> PackageInfo:
    """Detect importable packages in a repository."""
    src = root / "src"

    if src.is_dir():
        packages = _packages_under(src)
        return PackageInfo(
            src_layout=True,
            packages=packages,
            primary_package=_choose_primary_package(packages),
        )

    packages = _packages_under(root)

    return PackageInfo(
        src_layout=False,
        packages=packages,
        primary_package=_choose_primary_package(packages),
    )


def detect_primary_package(root: Path) -> str:
    """Return the primary detected Python package name."""
    return detect_packages(root).primary_package


def module_exists(root: Path, module_name: str) -> bool:
    """Return whether a dotted Python module exists in the repository."""
    relative = Path(*module_name.split("."))

    for base in (root / "src", root):
        package_path = base / relative / "__init__.py"
        module_path = base / relative.with_suffix(".py")

        if package_path.is_file() or module_path.is_file():
            return True

    return False


def _packages_under(base: Path) -> tuple[str, ...]:
    """Return top-level Python packages beneath a directory."""
    if not base.is_dir():
        return ()

    packages = [
        candidate.name
        for candidate in base.iterdir()
        if candidate.is_dir()
        and (candidate / "__init__.py").is_file()
        and not candidate.name.startswith(".")
    ]

    return tuple(sorted(packages))


def _choose_primary_package(packages: tuple[str, ...]) -> str:
    """Choose the primary package when one can be determined."""
    if len(packages) == 1:
        return packages[0]

    return packages[0] if packages else ""
