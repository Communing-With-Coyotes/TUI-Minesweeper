import terminal
import tiles
from minefield import Minefield


def draw(minefield):
    term = terminal.get_terminal()
    print(term.home, end='')

    for y in range(minefield.y_size):
        for x in range(minefield.x_size):
            position = (x, y)
            tile_is_selected = position == minefield.selected

            tile_definition = tiles.UNSEARCHED_TILE
            draw_symbol = None

            # This position is mined, flagged or already searched.
            if minefield.grid.get(position):
                spot = minefield.grid[position]

                if spot["searched"] and not spot["mined"]:
                    tile_definition = tiles.SEARCHED_TILE
                    draw_symbol = str( spot["neighbors"] )
                elif spot["searched"]:
                    tile_definition = tiles.EXPLODED_MINE

            if not draw_symbol:
                draw_symbol = tile_definition["symbol"]

            tile = tiles.get_tile(tile_definition, selected = tile_is_selected, symbol = draw_symbol)
            print(f"{term.move_right}{tile}", end='')
        
        print(term.move_down, end='')