from typing import List, Set, Tuple, Optional, NamedTuple
import random


class Offset(NamedTuple):
    """Offset for neighboring cells.

    Attributes:
        delta_row: Change in row coordinate.
        delta_col: Change in column coordinate.
    """

    delta_row: int
    delta_col: int


class Position(NamedTuple):
    """Immutable coordinate for a cell in the minefield."""

    row: int
    col: int


class RevealResult(NamedTuple):
    """Return value for `Minefield.reveal`.

    Attributes:
        hit_mine: True when the revealed cell contained a mine.
        newly_revealed: Set of positions that were revealed by this call.
    """

    hit_mine: bool
    newly_revealed: Set[Position]


class AdjacentMineMatrix(NamedTuple):
    """Wrapper for the 2D grid of adjacent mine counts.

    Field:
        counts: mutable 2D list of ints where -1 represents a mine and 0-8 are
                adjacent mine counts.
    """
    counts: List[List[int]]


NEIGHBOR_OFFSETS: Tuple[Offset, ...] = (
    Offset(-1, -1), Offset(-1, 0), Offset(-1, 1),
    Offset(0, -1),                 Offset(0, 1),
    Offset(1, -1),  Offset(1, 0),  Offset(1, 1),
)


class Minefield:
    """Represents a Minesweeper minefield.

    Grid cells use -1 for mines and 0-8 for adjacent mine counts.
    """

    def __init__(self, rows: int, columns: int, mine_count: int) -> None:
        self.rows: int = rows
        self.columns: int = columns
        self.mine_count: int = mine_count

        self.adjacent_mine_counts: AdjacentMineMatrix = AdjacentMineMatrix([])
        self.mine_positions: Set[Position] = set()
        self.revealed_positions: Set[Position] = set()
        self.flagged_positions: Set[Position] = set()

        self.setup_minefield()


    def is_loss(self) -> bool:
        """Return True if any revealed position is a mine."""
        return any(pos in self.mine_positions for pos in self.revealed_positions)


    def is_win(self) -> bool:
        """Return True if all non-mine positions have been revealed."""
        total_cells = self.rows * self.columns
        non_mine_cells = total_cells - self.mine_count
        
        return len(self.revealed_positions - self.mine_positions) == non_mine_cells


    def flag(self, row: int, col: int) -> None:
        """Flag a position on the minefield."""
        position: Position = Position(row, col)
        self.flagged_positions.add(position)


    def unflag(self, row: int, col: int) -> None:
        """Remove a flag from a position."""
        position: Position = Position(row, col)
        self.flagged_positions.discard(position)


    def is_flagged_correctly(self, row: int, col: int) -> bool:
        """Return True if the flag is on a mine, False otherwise."""
        position: Position = Position(row, col)
        return position in self.flagged_positions and position in self.mine_positions


    def in_bounds(self, row: int, col: int) -> bool:
        """Return True when (row, col) is inside the minefield bounds."""
        return 0 <= row < self.rows and 0 <= col < self.columns


    def reveal(self, row: int, col: int) -> RevealResult:
        """
        Reveal the cell at (row, col) and update the minefield state.

        If the cell contains a mine, only that cell is revealed and game over is triggered.
        If the cell contains a number (>0), only that cell is revealed.
        If the cell is empty (0), reveals all contiguous empty cells and their numbered borders.

        Returns:
            RevealResult: NamedTuple with:
                hit_mine (bool): True if the revealed cell was a mine.
                newly_revealed (Set[Position]): Set of positions revealed by this call (excluding already revealed positions).
        """

        if not self.adjacent_mine_counts.counts:
            raise ValueError("Grid is not initialized")

        if not self.in_bounds(row, col):
            raise IndexError("Cell position out of bounds")

        selected_pos: Position = Position(row, col)
        hit_mine: bool = False
        newly_revealed: Set[Position] = set()

        if selected_pos in self.revealed_positions or selected_pos in self.flagged_positions:
            # No action: revealed spots have nothing left to do,  
            # and flagged spots should not be revealed
            pass
        elif self.adjacent_mine_counts.counts[row][col] == -1:
            # Hit a mine
            self.revealed_positions.add(selected_pos)
            hit_mine = True
            newly_revealed = {selected_pos}
        elif self.adjacent_mine_counts.counts[row][col] > 0:
            # Reveal a numbered cell
            newly_revealed.add(selected_pos)
            self.revealed_positions.update(newly_revealed)
        else:
            # Reveal empty cell and cascade
            newly_revealed = self._cascade_empty_cells(selected_pos)
            self.revealed_positions.update(newly_revealed)
        return RevealResult(hit_mine, newly_revealed)

    
    def setup_minefield(self) -> None:
        """Initialize the minefield grid, randomly place mines, and calculate the number of adjacent mines for each cell."""
        total_cells: int = self.rows * self.columns

        if total_cells < 3:
            raise ValueError("Board too small: needs at least 3 cells to allow two free spots")
        if self.mine_count <= 0 or self.mine_count > (total_cells - 2):
            raise ValueError(f"mine_count must be between 1 and {total_cells - 2}")
        
        # Get all cell positions
        all_cells = [Position(row, col) for row in range(self.rows) for col in range(self.columns)]

        # Randomly place mines
        self.mine_positions = set(random.sample(all_cells, self.mine_count))

        # Create empty grid
        matrix = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.adjacent_mine_counts = AdjacentMineMatrix(matrix)
        
        # Mark mines on grid
        for mine_pos in self.mine_positions:
            self.adjacent_mine_counts.counts[mine_pos.row][mine_pos.col] = -1

        # Calculate adjacent mine counts
        self._calculate_adjacent_mine_counts()


    def _cascade_empty_cells(self, start_pos: Position) -> Set[Position]:
        """
        Flood fill to reveal all contiguous empty cells and their numbered borders.
        """
        newly_revealed: Set[Position] = set()
        stack: List[Position] = [start_pos]
        while stack:
            current_pos: Position = stack.pop()

            if current_pos in self.revealed_positions or current_pos in newly_revealed:
                continue

            newly_revealed.add(current_pos)

            if self.adjacent_mine_counts.counts[current_pos.row][current_pos.col] == 0:
                for delta_row, delta_col in NEIGHBOR_OFFSETS:
                    neighbor_row: int = current_pos.row + delta_row
                    neighbor_col: int = current_pos.col + delta_col
                    if not self.in_bounds(neighbor_row, neighbor_col):
                        continue
                    neighbor_pos: Position = Position(neighbor_row, neighbor_col)
                    if neighbor_pos in self.revealed_positions or neighbor_pos in newly_revealed:
                        continue
                    if self.adjacent_mine_counts.counts[neighbor_pos.row][neighbor_pos.col] == -1:
                        continue
                    stack.append(neighbor_pos)
        return newly_revealed


    def _calculate_adjacent_mine_counts(self) -> None:
        for row in range(self.rows):
            for col in range(self.columns):
                if self.adjacent_mine_counts.counts[row][col] == -1:
                    continue

                adjacent_mine_count: int = 0

                for delta_row, delta_col in NEIGHBOR_OFFSETS:
                    neighbor_row: int = row + delta_row
                    neighbor_col: int = col + delta_col
                    neighbor_pos: Position = Position(neighbor_row, neighbor_col)

                    if self.in_bounds(neighbor_row, neighbor_col) and neighbor_pos in self.mine_positions:
                        adjacent_mine_count += 1

                self.adjacent_mine_counts.counts[row][col] = adjacent_mine_count

