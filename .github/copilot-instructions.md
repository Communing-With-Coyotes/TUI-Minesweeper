## Purpose

Guidance for AI agents contributing to the terminal Minesweeper project.


## Quick Start

- Create and activate a venv, install dependencies:
  ```bash
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```
- Run the game:
  ```bash
  python -m tui_minesweeper
  # Or:
  python tui-minesweeper/__main__.py
  ```
- Run tests:
  ```bash
  pytest -q
  ```

## Dependency Analysis

- When deciding how to accomplish a task, always analyze `requirements.txt` for frameworks and libraries in use. This ensures compatibility and leverages existing dependencies.


## Code Style

**When generating code, always follow these code style rules.**

- Follow PEP 8. Use `black` for formatting, `flake8` for linting.
- Use type hints for public APIs and local variables.
- Separate logical sections with blank lines.
- Always leave two blank lines between the end of one method and the declaration of the next.
- Use descriptive, snake_case variable names; avoid single-letter names except for simple counters.

## Code Guidance

- Prefer immutable data structures (tuples, frozensets) when data shouldn't change.
- Use tuples internally; for public APIs, prefer dataclasses, NamedTuple, TypedDict, or small custom classes.
- Keep functions small and focused; split large functions into helpers.
- Write unit tests for all features and bug fixes, covering typical and edge cases.
- Use descriptive commit messages; follow the conventional commit format where applicable.