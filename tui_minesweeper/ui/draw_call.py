from __future__ import annotations
from typing import NamedTuple

from tui_minesweeper.position import Position
from blessed import Terminal
import os

import regex


class DrawCall(NamedTuple):
    """
    Represents a single draw call with position and z order.
    """

    position: Position
    z_layer: int
    content: list[str]
    width: int | None = None
    height: int | None = None


    def with_z_layer(self, z_layer: int) -> DrawCall:
        """
        Return a new DrawCall with the given z_layer.
        """
        return self._replace(z_layer=z_layer)


    def move_z_layer(self, amount: int) -> DrawCall:
        """
        Return a new DrawCall with z_layer changed by the specified amount (positive or negative).
        """
        return self._replace(z_layer=self.z_layer + amount)
        

    def move_to(self, position: Position) -> DrawCall:
        """
        Return a new DrawCall at the given position.
        """
        return self._replace(position=position)


    def move_by(self, row_delta: int = 0, col_delta: int = 0) -> DrawCall:
        """
        Return a new DrawCall moved by the given row and column deltas.
        """
        offset = Position(row_delta, col_delta)
        new_position = self.position.offset(offset)

        return self._replace(position=new_position)


    def move_up(self, amount: int = 1) -> DrawCall:
        """
        Return a new DrawCall moved up by the given amount (decreasing row).
        """
        return self.move_by(row_delta=-amount)


    def move_down(self, amount: int = 1) -> DrawCall:
        """
        Return a new DrawCall moved down by the given amount (increasing row).
        """
        return self.move_by(row_delta=amount)


    def move_left(self, amount: int = 1) -> DrawCall:
        """
        Return a new DrawCall moved left by the given amount (decreasing col).
        """
        return self.move_by(col_delta=-amount)


    def move_right(self, amount: int = 1) -> DrawCall:
        """
        Return a new DrawCall moved right by the given amount (increasing col).
        """
        return self.move_by(col_delta=amount)


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
                clipped_lines.append(DrawCall._clip_line_to_width(line, final_width))
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
        final_width: int | None = width if width is not None else self.width
        final_height: int | None = height if height is not None else self.height

        wrapped_lines: list[str] = []

        for line in self.content:
            if final_width is not None:
                if line:
                    wrapped_lines.extend(DrawCall._wrap_line_to_width(line, final_width))
                else:
                    wrapped_lines.append("")
            else:
                wrapped_lines.append(line)

        if final_height is not None and len(wrapped_lines) > final_height:
            return wrapped_lines[:final_height]

        return wrapped_lines


    @staticmethod
    def _clip_line_to_width(line: str, width: int) -> str:
        """
        Clips a line to the specified visible width, preserving ANSI and blessed control sequences,
        and correctly handling wide/multibyte Unicode characters.
        Ensures trailing ANSI codes are not dropped when the visible width is reached.
        """

        term = Terminal()
        
        result = ""
        visible_count = 0
        segments = list(DrawCall._iter_graphemes(line))
        reached_width = False

        for segment in segments:
            if not reached_width:
                if segment.startswith("\x1b"):
                    result += segment
                else:
                    char_width = term.length(segment)
                    
                    if visible_count + char_width > width:
                        reached_width = True
                        continue

                    result += segment
                    visible_count += char_width

                    if visible_count >= width:
                        reached_width = True
            else:
                # After reaching width, only append ANSI codes
                if segment.startswith("\x1b"):
                    result += segment

        return result


    @staticmethod
    def _wrap_line_to_width(line: str, width: int) -> list[str]:
        """
        Wraps a line to the specified visible width, preserving ANSI and blessed control sequences,
        and correctly handling wide/multibyte Unicode characters.
        Returns a list of wrapped lines.
        """
        term = Terminal()
        result: list[str] = []
        segment = ""
        visible_count = 0
        # Track active SGR ("m") sequences so we can reapply formatting at the start
        # of each wrapped line and close it with a reset. We keep other ESC sequences
        # in-place but they do not affect active_sgr.
        active_sgr = ""

        def _is_sgr(seq: str) -> bool:
            return seq.startswith("\x1b") and seq.endswith("m")

        def flush_segment():
            nonlocal segment, visible_count
            if segment:
                # If we have active styling, ensure the segment is closed with reset
                if active_sgr and not segment.endswith("\x1b[0m"):
                    segment += "\x1b[0m"
                result.append(segment)
            # Start a new segment reapplying active SGR if present
            segment = active_sgr
            visible_count = 0

        for part in DrawCall._iter_graphemes(line):
            if part.startswith("\x1b"):
                # Append ANSI to current segment
                segment += part
                # Manage active SGR state
                if _is_sgr(part):
                    # Reset clears active styling
                    if part in ("\x1b[0m", "\x1b[m"):
                        active_sgr = ""
                    else:
                        active_sgr += part
                # Non-SGR ESC sequences appended but don't change active_sgr
            else:
                char_width = term.length(part)

                if visible_count + char_width > width:
                    flush_segment()

                # If starting fresh, ensure active styling is present
                if not segment and active_sgr:
                    segment = active_sgr

                segment += part
                visible_count += char_width

                if visible_count == width:
                    flush_segment()

        # Finalize
        if segment:
            # ensure closing reset is present for final segment
            if active_sgr and not segment.endswith("\x1b[0m"):
                segment += "\x1b[0m"
            result.append(segment)

        return result
    

    @staticmethod
    def _iter_graphemes(line: str):
        """
        Yields grapheme clusters and ANSI escape sequences from the line.
        """
        index = 0
        length = len(line)
        # Match full ANSI escape sequences (CSI and other ESC sequences) as single tokens,
        # otherwise fall back to extended grapheme clusters (\X).
        # - \x1b\[[0-9;?]*[ -/]*[@-~] matches CSI/SGR sequences like \x1b[31m
        # - \x1b[\x20-\x7e]+ matches other ESC sequences like \x1b(B
        grapheme_pattern = regex.compile(r'(?:\x1b\[[0-9;?]*[ -/]*[@-~]|\x1b[\x20-\x7e]+)|\X')

        while index < length:
            g_match = grapheme_pattern.match(line, index)

            if not g_match:
                break
            
            yield g_match.group()
            index = g_match.end()