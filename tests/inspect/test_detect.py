"""Tests for repository detection."""

from pathlib import Path

from pup_core.base.errors import RepositoryDetectionError
from pup_core.base.types import GitInfo
import pup_core.inspect.detect as detect_module


def test_resolve_repository_root_from_child(tmp_path: Path) -> None:
    """Resolve upward to the directory containing .git."""
    (tmp_path / ".git").mkdir()
    child = tmp_path / "src" / "example"
    child.mkdir(parents=True)

    result = detect_module.resolve_repository_root(child)

    assert result == tmp_path.resolve()


def test_resolve_repository_root_rejects_missing_path(tmp_path: Path) -> None:
    """Reject a repository path that does not exist."""
    missing = tmp_path / "missing"

    try:
        detect_module.resolve_repository_root(missing)
    except RepositoryDetectionError as exc:
        assert "does not exist" in str(exc)
    else:
        raise AssertionError("Expected RepositoryDetectionError")


def test_snapshot_repository_files(tmp_path: Path) -> None:
    """Snapshot repository files while excluding generated directories."""
    source = tmp_path / "src" / "example"
    source.mkdir(parents=True)
    (source / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "README.md").write_text("Example", encoding="utf-8")

    cache = tmp_path / ".venv"
    cache.mkdir()
    (cache / "ignored.txt").write_text("", encoding="utf-8")

    files = detect_module.snapshot_repository_files(tmp_path)

    assert "README.md" in files
    assert "src/" in files
    assert "src/example/" in files
    assert "src/example/__init__.py" in files
    assert ".venv/ignored.txt" not in files


def test_detect_repository(tmp_path: Path, monkeypatch) -> None:
    """Combine repository, Git, and package facts."""
    (tmp_path / ".git").mkdir()

    package = tmp_path / "src" / "example"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")

    git_info = GitInfo(
        origin_url="https://github.com/denisecase/example.git",
        github_owner="denisecase",
        github_repo="example",
        tracked_files=frozenset(),
        untracked_files=frozenset(),
        ignored_files=frozenset(),
        dirty=False,
    )

    monkeypatch.setattr(
        detect_module,
        "inspect_git",
        lambda root: git_info,
    )

    context = detect_module.detect_repository(tmp_path)

    assert context.root == tmp_path.resolve()
    assert context.github_handle == "denisecase"
    assert context.repo_name == "example"
    assert context.repo_url == "https://github.com/denisecase/example"
    assert context.site_url == "https://denisecase.github.io/example/"
    assert context.src_package == "example"
