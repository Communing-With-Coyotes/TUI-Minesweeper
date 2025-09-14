

from typing import NamedTuple, Optional
from blessed import Terminal


class Color(NamedTuple):
    """
    Immutable RGB color representation.
    """
    r: int
    g: int
    b: int

    def to_blessed(self, term: Terminal, fg: bool = True) -> str:
        """
        Return blessed color string for this RGB color.

        Args:
            term (blessed.Terminal): Terminal instance.
            fg (bool): True for foreground, False for background.

        Returns:
            str: blessed color string.
        """
        if fg:
            return term.color_rgb(self.r, self.g, self.b)
        return term.on_color_rgb(self.r, self.g, self.b)



class ColorPair(NamedTuple):
    """
    Pair of foreground and background colors.
    """
    fg: Optional[Color] = None
    bg: Optional[Color] = None

    def to_blessed(self, term: Terminal, content: str) -> str:
        """
        Wrap content with blessed color formatting for fg/bg using blessed color strings.

        Args:
            term (blessed.Terminal): Terminal instance.
            content (str): Text to wrap.

        Returns:
            str: Content wrapped with blessed color formatting, terminated with term.normal.
        """
        result: str = content
        if self.bg:
            result = f"{self.bg.to_blessed(term, fg=False)}{result}"
        if self.fg:
            result = f"{self.fg.to_blessed(term, fg=True)}{result}"
        result += term.normal
        
        return result



# Default color constants (expand as needed)
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
YELLOW = Color(255, 255, 0)
CYAN = Color(0, 255, 255)
MAGENTA = Color(255, 0, 255)