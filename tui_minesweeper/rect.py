from __future__ import annotations
from typing import NamedTuple


class Position(NamedTuple):
    """Immutable coordinate for a cell in the minefield."""
    row: int
    col: int

    def offset(self, other: Position) -> Position:
        """Return a new Position offset by another Position."""
        return Position(self.row + other.row, self.col + other.col)


class Rect(NamedTuple):
    """Immutable rectangle defined by a top-left `Position`, `width`, and `height`.

    - `width` and `height` are integer counts of columns/rows (must be >= 0).
    """
    topleft: Position
    width: int
    height: int

    @staticmethod
    def from_position_size(row: int, col: int, width: int, height: int) -> Rect:
        return Rect(Position(row, col), width, height)

    def to_position(self) -> Position:
        return self.topleft

    def move_by(self, offset: Position) -> Rect:
        return Rect(self.topleft.offset(offset), self.width, self.height)

    def move_to(self, position: Position) -> Rect:
        return Rect(position, self.width, self.height)

    def contains(self, pos: Position) -> bool:
        return (
            pos.row >= self.topleft.row
            and pos.row < self.topleft.row + self.height
            and pos.col >= self.topleft.col
            and pos.col < self.topleft.col + self.width
        )

    def intersects(self, other: Rect) -> bool:
        # Two rects intersect if their projections on both axes overlap
        return not (
            self.topleft.row + self.height <= other.topleft.row
            or other.topleft.row + other.height <= self.topleft.row
            or self.topleft.col + self.width <= other.topleft.col
            or other.topleft.col + other.width <= self.topleft.col
        )

    def as_slices(self) -> tuple[slice, slice]:
        """Return (row_slice, col_slice) representing this rect.

        Useful for indexing 2D arrays with Python slice notation.
        """
        row_slice = slice(self.topleft.row, self.topleft.row + self.height)
        col_slice = slice(self.topleft.col, self.topleft.col + self.width)
        return row_slice, col_slice
