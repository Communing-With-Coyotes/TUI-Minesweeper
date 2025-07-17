import random
from typing import Dict, Tuple
from dataclasses import dataclass


INVALID_NEIGHBOR_COUNT = -1
NEIGHBORS_NOT_COUNTED = -2

NO_TILE_SELECTED = (-1, -1)


@dataclass(frozen=True)
class Spot:
    mined: bool = False
    searched: bool = False
    neighbors: int = NEIGHBORS_NOT_COUNTED


OUT_OF_BOUNDS_SPOT = Spot(mined = False, searched = False, neighbors = INVALID_NEIGHBOR_COUNT)


class Minefield:
    """
    Represents the Minesweeper game grid and logic.
    """
    def __init__(self, x_size: int, y_size: int, mine_count: int, selected: Tuple[int, int] = NO_TILE_SELECTED):
        """
        Initializes the minefield with the given dimensions and mine count.

        :param x_size: Width of the grid.
        :param y_size: Height of the grid.
        :param mine_count: Number of mines to place.
        :param selected: Initially selected tile coordinates.
        """
        self.x_size = x_size
        self.y_size = y_size
        self.mine_count = mine_count
        self.selected = selected

        self.grid = self._setup_grid()

    def _setup_grid(self) -> Dict[Tuple[int, int], Spot]:
        """
        Initializes the grid with all spots and randomly places mines.

        :return: The initialized grid dictionary.
        """
        grid = {}

        all_positions = [(x, y) for x in range(self.x_size) for y in range(self.y_size)]
        mine_positions = set(random.sample(all_positions, self.mine_count))

        for x, y in all_positions:
            mined = (x, y) in mine_positions
            grid[(x, y)] = self._create_spot(mined = mined)

        return grid

    def _create_spot(self, mined: bool = False, searched: bool = False) -> Spot:
        """
        Creates a Spot dataclass instance for the grid.

        :param mined: Whether the spot contains a mine.
        :param searched: Whether the spot has been revealed.
        :return: Spot instance.
        """
        return Spot(
            mined = mined,
            searched = searched,
            neighbors = INVALID_NEIGHBOR_COUNT if mined else NEIGHBORS_NOT_COUNTED
        )
    
    def _modify_spot(self, x: int, y: int, mined = None, searched = None, neighbors = None) -> None:
        """
        Modifies the Spot at (x, y) with the provided named arguments and updates the grid.

        :param x: X coordinate.
        :param y: Y coordinate.
        :param mined: New value for mined, or None to keep existing.
        :param searched: New value for searched, or None to keep existing.
        """
        old_spot = self.get_spot(x, y)

        updated_spot = Spot(
            mined = old_spot.mined if mined is None else mined,
            searched = old_spot.searched if searched is None else searched,
            neighbors = old_spot.neighbors if neighbors is None else neighbors
        )

        self._swap_spot(x, y, updated_spot)

    def _swap_spot(self, x: int, y: int, new_spot: Spot) -> None:
        """
        Swaps the spot at (x, y) in the grid with the provided new_spot.

        :param x: X coordinate.
        :param y: Y coordinate.
        :param new_spot: The Spot instance to place at (x, y).
        """
        self.grid[(x, y)] = new_spot

    def select(self, x: int, y: int) -> None:
        """
        Sets the currently selected tile.

        :param x: X coordinate.
        :param y: Y coordinate.
        """
        self.selected = (x, y)

    def move_selection(self, by_x: int, by_y: int, wrap_around: bool = True) -> None:
        """
        Moves the selection by the given amount. If no tile is currently selected,
        starts at the appropriate edge of the game board.

        :param by_x: Amount to move in the x direction.
        :param by_y: Amount to move in the y direction.
        :param wrap_around: Whether to wrap around the edges.
        """
        
        if self.selected == NO_TILE_SELECTED:
            start_x = 0 if by_x > 0 else self.x_size - 1
            start_y = 0 if by_y > 0 else self.y_size - 1

            self.selected = (start_x, start_y)
        else:
            x, y = self.selected

            if wrap_around:
                x += by_x
                y += by_y

                if x < 0 or x >= self.x_size:
                    x = x % self.x_size
                if y < 0 or y >= self.y_size:
                    y = y % self.y_size
            else:
                x = max(0, min(self.x_size - 1, x + by_x))
                y = max(0, min(self.y_size - 1, y + by_y))
            
            self.selected = (x, y)

    def get_spot(self, x: int, y: int) -> Spot:
        """
        Safely retrieves the Spot at (x, y), or returns a new out-of-bounds Spot if out of bounds or missing.

        :param x: X coordinate.
        :param y: Y coordinate.
        :return: Spot instance or a new out-of-bounds Spot if out of bounds or missing.
        """
        spot = self.grid.get((x, y))
        
        if spot is not None:
            return spot
        
        return OUT_OF_BOUNDS_SPOT

    def search_spot(self, x: int, y: int) -> bool:
        """
        Reveals the spot at (x, y). Returns True if a mine is uncovered.

        :param x: X coordinate.
        :param y: Y coordinate.
        :return: True if a mine is uncovered, False otherwise.
        """
        spot = self.get_spot(x, y)
        self._modify_spot(x, y, searched = True)
        
        return spot.mined

    def count_neighbors(self, x: int, y: int) -> None:
        """
        Counts the number of neighboring mines for the spot at (x, y).

        :param x: X coordinate.
        :param y: Y coordinate.
        """
        spot = self.get_spot(x, y)

        # If the spot has a mine or an invalid neighbor count, skip counting.
        if spot.mined or spot.neighbors == INVALID_NEIGHBOR_COUNT:
            return
        
        # Offsets for the 8 neighboring spots
        neighbor_offsets = [
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0),
            (-1,  1), (0,  1), (1,  1)
        ]
        
        neighbor_count = 0
        for dx, dy in neighbor_offsets:
            if self.has_mine_at_position(x + dx, y + dy):
                neighbor_count += 1
        
        self._modify_spot(x, y, neighbors = neighbor_count)

    def has_mine_at_position(self, x: int, y: int) -> bool:
        """
        Checks if the spot at (x, y) contains a mine.

        :param x: X coordinate.
        :param y: Y coordinate.
        :return: True if the spot contains a mine, False otherwise.
        """
        return self.get_spot(x, y).mined

