from ..minefield import Minefield
from .render_tile import RenderTile
from .compositor import Compositor, DrawCall
from ..position import Position
from .color import Color, ColorPair, WHITE, BLACK, RED, YELLOW, CYAN  # Import color symbols


# Minefield RenderTile constants using Color and ColorPair
UNSEARCHED_TILE: RenderTile = RenderTile(symbol="□", color=ColorPair(fg=WHITE, bg=BLACK))
SEARCHED_TILE: RenderTile = RenderTile(symbol=" ", color=ColorPair(fg=WHITE, bg=BLACK))
FLAGGED_TILE: RenderTile = RenderTile(symbol="⚑", color=ColorPair(fg=RED, bg=BLACK))
MINED_TILE: RenderTile = RenderTile(symbol="*", color=ColorPair(fg=YELLOW, bg=BLACK))


def render_minefield(minefield: Minefield, compositor: Compositor, position: Position = Position(0, 0), z_layer: int = 0) -> DrawCall:
    """
    Draw the minefield to the terminal using the provided compositor.

    Args:
        minefield (Minefield): The minefield to render.
        compositor (Compositor): The compositor to use for rendering.
    """
    rows: int = minefield.rows
    columns: int = minefield.columns
    lines: list[str] = []

    for row_index in range(rows):
        line: str = ""
        for col_index in range(columns):
            cell_position: Position = Position(row_index, col_index)

            if cell_position in minefield.revealed_positions:
                if cell_position in minefield.mine_positions:
                    tile: RenderTile = MINED_TILE
                else:
                    adjacent_count: int = minefield.adjacent_mine_counts.counts[row_index][col_index]
                    if adjacent_count > 0:
                        tile = RenderTile(
                            symbol=str(adjacent_count),
                            color=ColorPair(fg=CYAN, bg=BLACK)
                        )
                    else:
                        tile = SEARCHED_TILE
            elif cell_position in minefield.flagged_positions:
                tile = FLAGGED_TILE
            else:
                tile = UNSEARCHED_TILE

            line += tile.to_blessed(compositor.terminal)
        lines.append(line.rstrip())  # Remove trailing space for neatness

    return DrawCall(
        position=position,
        z_layer=z_layer,
        content=lines
    )
