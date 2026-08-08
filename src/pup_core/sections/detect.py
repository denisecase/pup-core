"""Managed section detection."""

from pup_core.base.errors import SectionError
from pup_core.base.types import ManagedSection

__all__ = ["find_managed_section"]


def find_managed_section(
    text: str,
    *,
    name: str,
    start_marker: str,
    end_marker: str,
) -> ManagedSection | None:
    """Find one explicitly bounded managed section."""
    start_count = text.count(start_marker)
    end_count = text.count(end_marker)

    if start_count == 0 and end_count == 0:
        return None

    if start_count != 1 or end_count != 1:
        raise SectionError(
            f"Managed section {name!r} must have exactly one "
            "start marker and one end marker."
        )

    start_index = text.index(start_marker)
    content_start = start_index + len(start_marker)
    end_marker_index = text.index(end_marker)

    if end_marker_index < content_start:
        raise SectionError(f"Managed section {name!r} has markers in the wrong order.")

    end_index = end_marker_index + len(end_marker)

    return ManagedSection(
        name=name,
        start_marker=start_marker,
        end_marker=end_marker,
        start_index=start_index,
        end_index=end_index,
        content_start=content_start,
        content_end=end_marker_index,
        content=text[content_start:end_marker_index],
    )
