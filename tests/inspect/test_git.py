"""Tests for Git repository inspection."""

from pathlib import Path

import pup_core.inspect.git as git_module


def test_inspect_git_collects_repository_facts(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """Collect Git facts returned by read-only Git commands."""
    (tmp_path / ".git").mkdir()

    def fake_run_git(root: Path, *args: str) -> str:
        assert root == tmp_path

        responses = {
            (
                "config",
                "--get",
                "remote.origin.url",
            ): "https://github.com/denisecase/example.git",
            ("ls-files",): "README.md\nsrc/example/__init__.py",
            ("ls-files", "--others", "--exclude-standard"): "notes.txt",
            (
                "ls-files",
                "--others",
                "--ignored",
                "--exclude-standard",
            ): ".venv/file.txt",
            ("status", "--porcelain"): " M README.md",
        }

        return responses.get(args, "")

    monkeypatch.setattr(git_module, "_run_git", fake_run_git)

    info = git_module.inspect_git(tmp_path)

    assert info.origin_url == "https://github.com/denisecase/example.git"
    assert info.github_owner == "denisecase"
    assert info.github_repo == "example"
    assert info.tracked_files == frozenset({"README.md", "src/example/__init__.py"})
    assert info.untracked_files == frozenset({"notes.txt"})
    assert info.ignored_files == frozenset({".venv/file.txt"})
    assert info.dirty is True


def test_inspect_git_handles_non_github_remote(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """A non-GitHub remote does not invent GitHub identity."""
    (tmp_path / ".git").mkdir()

    def fake_run_git(root: Path, *args: str) -> str:
        if args == ("config", "--get", "remote.origin.url"):
            return "https://example.com/team/repo.git"
        return ""

    monkeypatch.setattr(git_module, "_run_git", fake_run_git)

    info = git_module.inspect_git(tmp_path)

    assert info.github_owner == ""
    assert info.github_repo == ""
    assert info.dirty is False
