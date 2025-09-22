
from typing import NamedTuple, Optional

from blessed import Terminal
from tui_minesweeper.ui.color import ColorPair


class RenderTile(NamedTuple):
    symbol: str
    color: ColorPair

    def render(self, term: Terminal) -> str:
        """
        Render the symbol with blessed color formatting.

        Args:
            term (blessed.Terminal): Terminal instance.

        Returns:
            str: Symbol wrapped with blessed color formatting.
        """
        return self.color.wrap(term, self.symbol)
