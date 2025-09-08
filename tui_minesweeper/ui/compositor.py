from blessed import Terminal
from typing import NamedTuple
from tui_minesweeper.position import Position



class DrawCall(NamedTuple):
    """
    Represents a single draw call with position and z order.
    """

    position: Position
    z_layer: int
    content: list[str]
    width: int | None = None
    height: int | None = None

    def clip_content(
        self,
        width: int | None = None,
        height: int | None = None,
    ) -> list[str]:
        """
        Clip the content to fit within the given width and height, without wrapping.

        Args:
            width (int | None): The maximum width for each line. If not set, falls back to the DrawCall instance's width. If both are None, lines are not clipped horizontally.
            height (int | None): The maximum number of lines. If not set, falls back to the DrawCall instance's height. If both are None, lines are not clipped vertically.

        Returns:
            list[str]: Lines of text, clipped to fit the given size.
        """
        final_width: int | None = width if width is not None else self.width
        final_height: int | None = height if height is not None else self.height

        clipped_lines: list[str] = []

        for line in self.content:
            if final_width is not None:
                clipped_lines.append(line[:final_width])
            else:
                clipped_lines.append(line)

        if final_height is not None and len(clipped_lines) > final_height:
            return clipped_lines[:final_height]

        return clipped_lines


    def wrap_content(
        self,
        width: int | None = None,
        height: int | None = None,
    ) -> list[str]:
        """
        Wrap the content to fit within the given width and height.

        Args:
            width (int | None): The maximum width for wrapping lines. If not set, falls back to the DrawCall instance's width. If both are None, lines are not wrapped.
            height (int | None): The maximum number of lines. If not set, falls back to the DrawCall instance's height. If both are None, lines are not clipped vertically.

        Returns:
            list[str]: Lines of text, wrapped and clipped to fit the given size. Tab characters are preserved.
        """
        import textwrap

        final_width: int | None = width if width is not None else self.width
        final_height: int | None = height if height is not None else self.height

        wrapped_lines: list[str] = []

        for line in self.content:
            if final_width is not None:
                # Wrap strictly every final_width characters
                if line:
                    wrapped = [line[i:i+final_width] for i in range(0, len(line), final_width)]
                else:
                    # Preserve empty lines in wrapped output
                    wrapped = [""]
                wrapped_lines.extend(wrapped)
            else:
                wrapped_lines.append(line)

        if final_height is not None and len(wrapped_lines) > final_height:
            return wrapped_lines[:final_height]

        return wrapped_lines



class Compositor:
    """
    Compositor for batching and blitting text to the terminal in a single draw call.
    """

    def __init__(self) -> None:
        self._draw_calls: list[DrawCall] = []


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

        draw_call = DrawCall(
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

        term = Terminal()
        term_width: int = term.width or 80
        term_height: int = term.height or 24

        print(term.home + term.clear, end="")
        for _, draw_call in sorted_calls:
            content_lines: list[str] = draw_call.clip_content(
                width=term_width,
                height=term_height,
            )
            for content_line in content_lines:
                print(content_line)

        self._draw_calls.clear()