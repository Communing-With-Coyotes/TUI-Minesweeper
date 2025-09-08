from typing import NamedTuple

class RenderTile(NamedTuple):
    symbol: str
    fg_color: str
    bg_color: str

# Example usage:
# tile = RenderTile(symbol='*', fg_color='white', bg_color='black')
