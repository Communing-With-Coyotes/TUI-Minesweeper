from blessed import Terminal
from typing import NamedTuple
from tui_minesweeper.position import Position
from tui_minesweeper.ui.draw_call import DrawCall


class Compositor:
    """
    Compositor for batching and blitting text to the terminal in a single draw call.
    """
    def __init__(self, terminal: Terminal | None = None) -> None:
        self._draw_calls: list[DrawCall] = []
        self._terminal: Terminal = terminal if terminal is not None else Terminal()


    @property
    def terminal(self) -> Terminal:
        """
        Read-only access to the Terminal instance used by the compositor.
        """
        return self._terminal


    def add_text(
        self,
        content: str | list[str],
        col: int,
        row: int,
        z_layer: int,
    ) -> None:
        """
        Add text (string or list of strings) to the draw queue at the given position and z layer.

        Args:
            content (str | list[str]): The text to draw.
            col (int): The column position.
            row (int): The row position.
            z_layer (int): The z layer for drawing.
        """
        if isinstance(content, str):
            lines: list[str] = content.splitlines() or [content]
        else:
            lines: list[str] = content

        draw_call: DrawCall = DrawCall(
            position=Position(row, col),
            z_layer=z_layer,
            content=lines,
        )
        self.add_draw_call(draw_call)


    def add_draw_call(self, draw_call: DrawCall) -> None:
        """
        Add a DrawCall to the compositor's draw call queue.

        Args:
            draw_call (DrawCall): The draw call to queue for drawing.
        """
        self._draw_calls.append(draw_call)


    def draw(self) -> None:
        """
        Blit all queued text to the terminal in a single draw call.
        """
        sorted_calls = sorted(
            enumerate(self._draw_calls),
            key=lambda item: (item[1].z_layer, item[0]),
        )

        term_width: int = self.terminal.width or 80
        term_height: int = self.terminal.height or 24

        print(self.terminal.home + self.terminal.clear, end="")

        for _, draw_call in sorted_calls:
            content_lines: list[str] = draw_call.clip_content(
                width=term_width,
                height=term_height,
            )
            for content_line in content_lines:
                print(content_line)

        self._draw_calls.clear()