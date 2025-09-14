# Minesweeper Game Implementation

from blessed import Terminal
import sys
from tui_minesweeper.minefield import Minefield
from tui_minesweeper.ui import render_minefield
from tui_minesweeper.ui.compositor import Compositor


# Global input constants
QUIT_KEY: str = 'q'


class Game:
    """Main game class handling board state and logic."""

    def __init__(
        self,
        width: int = 10,
        height: int = 10,
        mines: int = 10,
        compositor: Compositor | None = None,
        fps: int = 60,
    ) -> None:
        """Initialize game with given dimensions, mine count, and compositor."""
        self.width: int = width
        self.height: int = height
        self.mines: int = mines
        self.term: Terminal = Terminal()
        self.compositor: Compositor = compositor if compositor is not None else Compositor()
        self.minefield: Minefield = Minefield(width, height, mines)
        self.frame_interval: float = 1.0 / fps


    def start(self) -> None:
        """Initialize and start the game loop."""
        with self.term.fullscreen(), self.term.cbreak():
            self._main_loop()


    def _main_loop(self) -> None:
        """Handle user input and game state updates."""
        import time
        last_update: float = time.time()

        while True:
            user_input = self.term.inkey(timeout=self.frame_interval)
            now: float = time.time()
            should_update: bool = user_input is not None or (now - last_update) >= self.frame_interval

            # Handle quit
            if user_input is not None and user_input.lower() == QUIT_KEY:
                sys.exit(0)

            if should_update:
                self.compositor.add_draw_call(render_minefield.render_minefield(self.minefield, self.compositor))
                self.compositor.draw()
                last_update = now


def main() -> None:
    """Entry point for the application."""
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
