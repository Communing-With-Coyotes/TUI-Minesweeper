from dataclasses import dataclass
from typing import Optional, NamedTuple

import terminal


RESET_COLOR: str = terminal.get_terminal().normal
"""Terminal escape sequence to reset all colors and formatting."""


class RGB(NamedTuple):
    """
    Represents an RGB color with red, green, and blue components.

    Attributes:
        r (int): The red component of the color (0-255).
        g (int): The green component of the color (0-255).
        b (int): The blue component of the color (0-255).
    """
    r: int
    g: int
    b: int


@dataclass(frozen=True)
class Color:
    """
    Represents an RGB color for terminal output. Provides methods to generate
    terminal escape sequences for foreground and background colors, as well as
    utility methods for color pairing and wrapping content with color.
    """
    r: int
    g: int
    b: int

    def __post_init__(self):
        for channel, name in zip((self.r, self.g, self.b), ('r', 'g', 'b')):
            if not (0 <= channel <= 255):
                raise ValueError(f"Color value for {name} must be in range 0-255, got {channel}")

    def rgb(self) -> RGB:
        """
        Returns the RGB named tuple for this color.
        :return: RGB(r, g, b)
        """
        return RGB(self.r, self.g, self.b)

    def fg(self) -> str:
        """
        Foreground terminal format string.
        :return: Terminal escape sequence for foreground color.
        """
        return Color.create_color(self.r, self.g, self.b)

    def bg(self) -> str:
        """
        Background terminal format string.
        :return: Terminal escape sequence for background color.
        """
        return Color.create_color(self.r, self.g, self.b, True)

    @staticmethod
    def create_color(r: int, g: int, b: int, is_background: bool = False) -> str:
        """
        Creates a terminal-usable color.
        :param r: Red value (0-255)
        :param g: Green value (0-255)
        :param b: Blue value (0-255)
        :param is_background: If True, returns a background color; otherwise, foreground.
        :return: Terminal color escape sequence as a string.
        """
        term = terminal.get_terminal()
        
        if is_background:
            return term.on_color_rgb(r, g, b)
        
        return term.color_rgb(r, g, b)

    @staticmethod
    def style(
        fg_color: Optional['Color'] = None,
        bg_color: Optional['Color'] = None,
        content: Optional[str] = None
    ) -> str:
        """
        Returns a combined terminal color escape sequence for foreground and background,
        and optionally wraps the provided content.
        :param fg_color: Color instance for the foreground (or None for default).
        :param bg_color: Color instance for the background (or None for default).
        :param content: If provided, wraps this string with the color codes.
        :return: Escape sequence or colored string.
        """
        fg = fg_color.fg() if fg_color else ''
        bg = bg_color.bg() if bg_color else ''
        
        if content is not None:
            return f"{fg}{bg}{content}{RESET_COLOR}"
        
        return f"{fg}{bg}"


# COLORS
BLACK = Color(0, 0, 0)
GRAY = Color(128, 128, 128)
EMERALD = Color(99, 212, 113)
BROWN = Color(197, 123, 87)
RED = Color(255, 0, 0)


__all__ = [
    "RESET_COLOR",
    "RGB",
    "Color",
    "BLACK",
    "GRAY",
    "EMERALD",
    "BROWN",
    "RED"
]

