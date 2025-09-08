from ..minefield import Minefield
from .render_tile import RenderTile
from .compositor import Compositor
from ..position import Position


# Minefield RenderTile constants
UNSEARCHED_TILE: RenderTile = RenderTile(symbol="□", fg_color="white", bg_color="black")
SEARCHED_TILE: RenderTile = RenderTile(symbol=" ", fg_color="white", bg_color="black")
FLAGGED_TILE: RenderTile = RenderTile(symbol="⚑", fg_color="red", bg_color="black")
MINED_TILE: RenderTile = RenderTile(symbol="*", fg_color="yellow", bg_color="black")



def draw_minefield(minefield: Minefield, compositor: Compositor) -> None:
    """
    Draw the minefield to the terminal using the provided compositor.

    Args:
        minefield (Minefield): The minefield to render.
        compositor (Compositor): The compositor to use for rendering.
    """
    rows: int = minefield.rows
    columns: int = minefield.columns
    z_layer: int = 0  # Main minefield layer
    lines: list[str] = []

    for row_index in range(rows):
        line: str = ""
        for col_index in range(columns):
            position: Position = Position(row_index, col_index)

            if position in minefield.revealed_positions:
                if position in minefield.mine_positions:
                    tile: RenderTile = MINED_TILE
                else:
                    adjacent_count: int = minefield.adjacent_mine_counts.counts[row_index][col_index]
                    if adjacent_count > 0:
                        tile = RenderTile(symbol=str(adjacent_count), fg_color="cyan", bg_color="black")
                    else:
                        tile = SEARCHED_TILE
            elif position in minefield.flagged_positions:
                tile = FLAGGED_TILE
            else:
                tile = UNSEARCHED_TILE

            line += tile.symbol + " "  # Add space between columns
        lines.append(line.rstrip())  # Remove trailing space for neatness

    compositor.add_text(lines, col=0, row=0, z_layer=z_layer)
    compositor.draw()
