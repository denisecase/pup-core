"""Managed section planning."""

from pup_core.base.types import SectionPlan
from pup_core.sections.detect import find_managed_section

__all__ = ["plan_section_change"]


def plan_section_change(
    text: str,
    *,
    name: str,
    start_marker: str,
    end_marker: str,
    desired_content: str | None,
    insert_before_marker: str | None = None,
) -> SectionPlan:
    """Plan an add, replace, delete, or unchanged section operation."""
    current = find_managed_section(
        text,
        name=name,
        start_marker=start_marker,
        end_marker=end_marker,
    )

    if current is None:
        action = "unchanged" if desired_content is None else "add"
    elif desired_content is None:
        action = "delete"
    elif current.content == desired_content:
        action = "unchanged"
    else:
        action = "replace"

    return SectionPlan(
        name=name,
        action=action,
        start_marker=start_marker,
        end_marker=end_marker,
        current=current,
        desired_content=desired_content,
        insert_before_marker=insert_before_marker,
    )
