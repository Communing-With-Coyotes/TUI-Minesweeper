from term_colors import *


# TILE CHARACTERS
UNSEARCHED_SPOT = "■"
SEARCHED_SPOT = "⛶"
FLAGGED_SPOT = "⟎"
MINED_SPOT = "⧆"

# COLORS
BLACK = Color(0, 0, 0)
GRAY = Color(128, 128, 128)
EMERALD = Color(99, 212, 113)
BROWN = Color(197, 123, 87)
RED = Color(255, 0, 0)


UNSEARCHED_TILE = {
    "symbol": UNSEARCHED_SPOT, 
    "color": GRAY.fg(),
    "selected_color": EMERALD.fg()
}


SEARCHED_TILE = {
    "symbol": SEARCHED_SPOT, 
    "color": BROWN.fg(),
    "selected_color": EMERALD.fg()
}


EXPLODED_MINE = {
    "symbol": MINED_SPOT,
    "color": RED.fg(),
    "selected_color": RED.fg()
}


def get_tile(tile_definition, selected = None, symbol = None):
    symbol = symbol if symbol else tile_definition["symbol"]
    draw_color = tile_definition["selected_color"] if selected else tile_definition["color"]

    return f"{draw_color}{symbol}{RESET_COLOR}"

