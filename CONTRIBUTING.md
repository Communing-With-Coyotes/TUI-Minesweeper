# Contributing to Terminal Minesweeper

Thank you for contributing to this project! Please follow these guidelines to ensure consistency and quality.

## Development Workflow

1. **Set up environment**  
   Follow [README.md](README.md) installation instructions including virtualenv setup

2. **Code Structure**  
   - Game logic lives in `src/game.py`
   - Add tests in `tests/test_game.py`
   - Maintain single responsibility per class/function

3. **Testing**  
   Add unit tests for new features:
   ```bash
   python -m pytest tests/
   ```

4. **Documentation**  
   - Update this file for new contribution patterns
   - Maintain API docs in code comments (Sphinx style)

## Commit Guidelines

- Use semantic commit types: `feat/`, `fix/`, `docs/`, `chore/`
- Reference relevant issues in commit messages
- Keep changes focused on single logical change

## Style Requirements

- Python 3.8+ type hints
- PEP8 compliance (max 88 chars/line)
- Docstrings for public APIs
