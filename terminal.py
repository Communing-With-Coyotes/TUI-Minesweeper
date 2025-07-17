
from blessed import Terminal
import sys
from typing import Optional
from term_colors import Color


TERMINAL = Terminal()


def get_terminal() -> Terminal:
    """
    Returns the global Terminal instance.
    """
    return TERMINAL


def reset(bg_color: 'Optional[Color]' = None) -> None:
    """
    Clears the terminal and moves the cursor to the home position.
    If bg_color is provided, sets the background color before clearing.
    According to the blessed documentation, clearing the screen after setting the background color will repaint the background on the screen for most terminals.
    :param bg_color: Optional Color instance for background.
    """
    if bg_color is not None:
        print(f"{TERMINAL.home}{bg_color.bg()}{TERMINAL.clear}", end='')
    else:
        print(f"{TERMINAL.home}{TERMINAL.clear}", end='')


def check_for_terminal(error_msg: str) -> None:
    """
    Checks if the current environment is a TTY. If not, prints the error message and exits.

    :param error_msg: The error message to display if not running in a TTY.
    """
    if not TERMINAL.is_a_tty:
        output = " ".join(line.strip() for line in error_msg.splitlines())
        print(output)

        sys.exit()