from typing import Optional
from dataclasses import dataclass

from term_colors import *


# TILE SYMBOLS
UNSEARCHED_SPOT = "■"
SEARCHED_SPOT = "⛶"
FLAGGED_SPOT = "⟎"
MINED_SPOT = "⧆"


@dataclass(frozen=True)
class Tile:
    symbol: str
    color: Color
    selected_color: Color


UNSEARCHED_TILE = Tile(
    symbol = UNSEARCHED_SPOT,
    color = GRAY,
    selected_color = EMERALD
)


SEARCHED_TILE = Tile(
    symbol = SEARCHED_SPOT,
    color = BROWN,
    selected_color = EMERALD
)


EXPLODED_MINE = Tile(
    symbol = MINED_SPOT,
    color = RED,
    selected_color = RED
)


def get_tile(
    tile: Tile,
    selected: bool = False,
    symbol: Optional[str] = None
    ) -> str:
    """
    Returns the colored string required to draw a tile to the terminal.
    :param tile: The Tile instance.
    :param selected: Whether the tile is currently selected.
    :param symbol: Optional symbol to override the default tile symbol.
    :return: A colored string for drawing the tile to the terminal.
    """
    draw_symbol = symbol if symbol else tile.symbol
    draw_color = tile.selected_color.fg() if selected else tile.color.fg()

    return f"{draw_color}{draw_symbol}{RESET_COLOR}"

