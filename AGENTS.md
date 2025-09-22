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

- When deciding how to accomplish a task, always analyze `requirements.txt` for frameworks and libraries in use to ensure compatibility.


## Code Style Guidelines

When generating code, follow these rules:

- **PEP 8:** Use `black` and `flake8`.
- **Type hints:** For public APIs and local variables.
- **Spacing:** Separate logical sections with blank lines; leave two blank lines between methods.
- **Names:** Use descriptive `snake_case` names; avoid single-letter names except simple counters.
- **Comments:** For complex logic, add concise intent/behavior comments and update them when altering code.
- **Method naming:** Prefer names that describe what the method does (its intent/use) rather than how. Avoid exposing implementation details in public method names. Exceptions: private or internal APIs may include implementation-specific terms when the name reflects intended usage tied to that implementation.


## Code Guidance

- Prefer immutable structures (tuples, frozensets) when data shouldn't change.
- Use tuples internally; for public APIs prefer `dataclasses`, `NamedTuple`, or `TypedDict`.
- Keep functions small and focused; split large functions into helpers.
- Write unit tests for features and bug fixes, covering typical and edge cases.
- Use descriptive commit messages; follow conventional commit format when applicable.

## Testing Guidance

- **Purpose:** Tests must validate that functions produce intended outputs based on their design and usage.
- **Approach:** Identify a function's intent, then assert correct behavior for typical inputs and edge cases.
- **Failures:** Include tests that confirm known-bad inputs fail as expected (specific exceptions or error states).
- **Scope:** Prefer focused unit tests checking outputs, side-effects, and error conditions rather than implementation details.
- **Ensure terminal styling in tests:** For tests that assert colors or styling, set `TERM` to a 256-color value and create a blessed `Terminal` with `force_styling=True` so color/styling sequences are emitted.
  - **Snippet (place at top of test modules):**
    ```python
    import os
    from blessed import Terminal

    os.environ.setdefault("TERM", "xterm-256color")
    term = Terminal(force_styling=True)
    ```