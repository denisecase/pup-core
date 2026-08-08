"""Repository detection."""

from pathlib import Path

from pup_core.base.errors import RepositoryDetectionError
from pup_core.base.types import RepositoryContext
from pup_core.inspect.git import inspect_git
from pup_core.inspect.packages import detect_primary_package

__all__ = [
    "detect_repository",
    "resolve_repository_root",
    "snapshot_repository_files",
]


def detect_repository(root: Path | None = None) -> RepositoryContext:
    """Detect objective facts about a repository."""
    repo_root = resolve_repository_root(root)
    files = snapshot_repository_files(repo_root)
    git_info = inspect_git(repo_root)

    github_handle = git_info.github_owner
    repo_name = git_info.github_repo or repo_root.name

    if github_handle:
        repo_url = f"https://github.com/{github_handle}/{repo_name}"
        site_url = f"https://{github_handle}.github.io/{repo_name}/"
    else:
        repo_url = ""
        site_url = ""

    return RepositoryContext(
        root=repo_root,
        github_handle=github_handle,
        repo_name=repo_name,
        repo_url=repo_url,
        site_url=site_url,
        src_package=detect_primary_package(repo_root),
        files=frozenset(files),
    )


def resolve_repository_root(root: Path | None = None) -> Path:
    """Resolve the target repository root."""
    start = Path.cwd() if root is None else root
    start = start.expanduser().resolve()

    if not start.exists():
        raise RepositoryDetectionError(f"Repository path does not exist: {start}")

    if start.is_file():
        start = start.parent

    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate

    return start


def snapshot_repository_files(root: Path) -> set[str]:
    """Return repository-relative file and directory markers."""
    result: set[str] = set()

    ignored_dirs = {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "htmlcov",
        "node_modules",
        "site",
    }

    for path in root.rglob("*"):
        relative = path.relative_to(root)

        if any(part in ignored_dirs for part in relative.parts):
            continue

        rel = relative.as_posix()

        if path.is_dir():
            result.add(rel)
            result.add(f"{rel}/")
        else:
            result.add(rel)

    return result
