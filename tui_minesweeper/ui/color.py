from typing import NamedTuple, Optional
from blessed import Terminal


# Standard SGR sequences to reset only the foreground or background color.
# Exported so other modules can reuse these resets rather than embedding
# literal escape sequences throughout the codebase.
FG_RESET: str = "\x1b[39m"
BG_RESET: str = "\x1b[49m"


class Color(NamedTuple):
    """
    Immutable RGB color representation.
    """

    r: int
    g: int
    b: int

    def sequence(self, term: Terminal, fg: bool = True) -> str:
        """Return only the SGR/escape sequence for this color (no reset)."""

        # Clamp channels to valid 0..255 range to avoid invalid sequences
        def clamp_channel(v: int) -> int:
            if v < 0:
                return 0
            if v > 255:
                return 255
            return v

        r: int = clamp_channel(self.r)
        g: int = clamp_channel(self.g)
        b: int = clamp_channel(self.b)

        return term.color_rgb(r, g, b) if fg else term.on_color_rgb(r, g, b)

    def wrap(self, term: Terminal, content: str, fg: bool = True) -> str:
        """Wrap `content` with this color's sequence and a color-only reset."""
        seq = self.sequence(term, fg=fg)
        reset = FG_RESET if fg else BG_RESET
        return f"{seq}{content}{reset}"


class ColorPair(NamedTuple):
    """
    Pair of foreground and background colors.
    """

    fg: Optional[Color] = None
    bg: Optional[Color] = None

    def wrap(self, term: Terminal, content: str) -> str:
        """
        Wrap `content` with blessed color formatting for fg/bg and append
        color-only reset sequences. If neither `fg` nor `bg` is set, return
        the content unchanged.

        Args:
            term (blessed.Terminal): Terminal instance.
            content (str): Text to wrap.

        Returns:
            str: Content wrapped with blessed color formatting and resets.
        """
        if not self.fg and not self.bg:
            return content

        parts: list[str] = []

        # Prepend background then foreground sequences when present so that
        # resets can be appended in the reverse order (like nested scopes).
        if self.bg:
            parts.append(self.bg.sequence(term, fg=False))
        if self.fg:
            parts.append(self.fg.sequence(term, fg=True))

        wrapped = "".join(parts) + content

        # Append resets in reverse order of application: foreground then background.
        resets = ""
        if self.fg:
            resets += FG_RESET
        if self.bg:
            resets += BG_RESET

        return wrapped + resets


# Default color constants (expand as needed)
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
YELLOW = Color(255, 255, 0)
CYAN = Color(0, 255, 255)
MAGENTA = Color(255, 0, 255)
