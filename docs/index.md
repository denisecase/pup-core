# pup-core

`pup-core` provides shared repository inspection, typing, path-safety,
normalization, and planning primitives for the
Professional Python Project Updater
(`pup`) tool family.

It is the common foundation used by the user-facing tools and
centralizes behavior across those tools.

## Purpose

Professional Python repository tools need foundational capabilities:

- locating and identifying a repository
- inspecting repository files and structure
- reading project metadata
- identifying Python package and `src/` layouts
- normalizing project, package, path, and Python-version information
- handling repository-relative paths safely
- representing repository and file-planning information with shared types
- reporting common repository-detection and path errors

`pup-core` provides a shared implementation for the `pup` tool family.

## Repository Inspection

`pup-core` provides shared structures and utilities for
understanding repository characteristics such as:

- repository root
- repository and project names
- GitHub repository information
- available repository files
- Python project presence
- `src/` package layout
- package names
- project metadata
- Python versions
- repository-relative paths

## See Also

- [API](./api.md)
