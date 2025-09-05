from typing import NamedTuple

class Position(NamedTuple):
    """Immutable coordinate for a cell in the minefield."""
    row: int
    col: int
