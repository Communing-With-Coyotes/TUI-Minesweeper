import terminal


RESET_COLOR = terminal.get_terminal().normal


# Creates a terminal-usable color.
def create_color(r, g, b, is_background=False):
    term = terminal.get_terminal()

    if is_background:
        return term.on_color_rgb(r, g, b)

    return term.color_rgb(r, g, b)


def color_pair(fg_color = None, bg_color = None):
    fg_color_str = fg_color.fg() if fg_color else ''
    bg_color_str = bg_color.bg() if bg_color else ''

    return f"{fg_color_str}{bg_color_str}"


# Wraps content with a foreground and background color.
def wrap(content, fg_color = None, bg_color = None):
    fg_color = '' if not fg_color else fg_color
    bg_color = '' if not bg_color else bg_color

    return f"{fg_color}{bg_color}{content}{RESET_COLOR}"


class Color:

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    

    def rgb(self):
        return (self.r, self.g, self.b)
    

    # Foreground terminal format string
    def fg(self):
        return create_color(self.r, self.g, self.b)
    

    # Background terminal format string
    def bg(self):
        return create_color(self.r, self.g, self.b, True)