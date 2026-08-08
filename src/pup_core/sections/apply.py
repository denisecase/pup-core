"""Managed section application."""

from pup_core.base.errors import SectionError
from pup_core.base.types import SectionPlan

__all__ = ["apply_section_plan"]


def apply_section_plan(text: str, plan: SectionPlan) -> str:
    """Apply one previously planned managed-section operation."""
    if plan.action == "unchanged":
        return text

    if plan.action == "delete":
        if plan.current is None:
            return text

        return text[: plan.current.start_index] + text[plan.current.end_index :]

    replacement = _render_section(plan)

    if plan.action == "replace":
        if plan.current is None:
            raise SectionError(f"Cannot replace missing managed section {plan.name!r}.")

        return (
            text[: plan.current.start_index]
            + replacement
            + text[plan.current.end_index :]
        )

    if plan.action == "add":
        if plan.current is not None:
            raise SectionError(f"Cannot add existing managed section {plan.name!r}.")

        if plan.insert_before_marker is not None:
            marker_count = text.count(plan.insert_before_marker)

            if marker_count != 1:
                raise SectionError(
                    f"Insertion marker for section {plan.name!r} "
                    "must occur exactly once."
                )

            index = text.index(plan.insert_before_marker)
            return text[:index] + replacement + text[index:]

        if not text:
            return replacement

        separator = "" if text.endswith("\n") else "\n"
        return text + separator + replacement

    raise SectionError(f"Unknown managed-section action: {plan.action!r}")


def _render_section(plan: SectionPlan) -> str:
    """Render a complete managed section including its markers."""
    if plan.desired_content is None:
        raise SectionError(f"Managed section {plan.name!r} has no desired content.")

    return f"{plan.start_marker}{plan.desired_content}{plan.end_marker}"
