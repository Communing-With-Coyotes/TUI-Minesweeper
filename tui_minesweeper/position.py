from __future__ import annotations
from typing import NamedTuple


class Position(NamedTuple):
    """Immutable coordinate for a cell in the minefield."""
    row: int
    col: int

    def offset(self, other: Position) -> Position:
        return Position(self.row + other.row, self.col + other.col)
