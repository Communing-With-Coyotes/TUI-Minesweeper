# Terminal Minesweeper Clone

A Minesweeper clone implemented in Python using the `blessed` library for terminal interaction.

## Installation

1. Ensure Python 3.8+ is installed
2. Create virtual environment:
```bash
python -m venv .venv
```
3. Activate virtual environment:
```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
## Running the Game

To run the game after installation:
```bash
python -m tui_minesweeper
```
Or directly execute the main file:
```bash
python tui-minesweeper/__main__.py
```

## Project Structure

```
TUI_Minesweeper/
├── venv/             # Python virtual environment
├── src/              # Core game implementation
│   ├── __init__.py
│   └── game.py       # Main game logic
├── tests/            # Unit tests
│   └── test_game.py
├── README.md         ← This file
├── requirements.txt  # Dependency specifications
└── agents.md         # Agent definition and constraints
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines and API documentation.
