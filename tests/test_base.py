"""Tests for shared pup-core base types and errors."""

from pathlib import Path

from pup_core.base.errors import UnsafePathError
from pup_core.base.types import PlannedFile, RepositoryContext, UpdatePlan


def test_repository_context() -> None:
    """RepositoryContext stores repository identity and structure."""
    context = RepositoryContext(
        root=Path("/repo"),
        github_handle="example",
        repo_name="example-project",
        repo_url="https://github.com/example/example-project",
        site_url="https://example.github.io/example-project/",
        src_package="example_project",
        files=frozenset({"pyproject.toml", "src"}),
        layers=("ALL", "ALL-PY", "ALL-PY-SRC"),
    )

    assert context.repo_name == "example-project"
    assert context.src_package == "example_project"
    assert context.files == frozenset({"pyproject.toml", "src"})
    assert context.layers == ("ALL", "ALL-PY", "ALL-PY-SRC")


def test_update_plan_contains_planned_files() -> None:
    """UpdatePlan stores its repository and planned files."""
    context = RepositoryContext(
        root=Path("/repo"),
        github_handle="example",
        repo_name="example-project",
        repo_url="https://github.com/example/example-project",
        site_url="https://example.github.io/example-project/",
        src_package="example_project",
        files=frozenset({"pyproject.toml"}),
        layers=("ALL", "ALL-PY"),
    )

    planned_file = PlannedFile(
        path=Path(".gitignore"),
        status="current",
        source_layer="ALL",
        source_path="ALL/.gitignore",
        current_text="*.log\n",
        desired_text="*.log\n",
    )

    plan = UpdatePlan(
        target=context,
        files=(planned_file,),
    )

    assert plan.target == context
    assert plan.files == (planned_file,)
    assert plan.files[0].status == "current"


def test_unsafe_path_error_is_exception() -> None:
    """UnsafePathError is a pup-core exception."""
    error = UnsafePathError(Path("/outside/repository"))

    assert isinstance(error, Exception)
    assert "Unsafe path escapes repository root" in str(error)
