import pytest
from blessed import Terminal
import regex
from tui_minesweeper.position import Position
from tui_minesweeper.ui.draw_call import DrawCall


def test_with_z_layer():
    dc = DrawCall(Position(1, 2), 3, ["foo"])
    new_dc = dc.with_z_layer(10)
    assert new_dc.z_layer == 10
    assert new_dc.position == dc.position
    assert new_dc.content == dc.content


def test_move_z_layer():
    dc = DrawCall(Position(1, 2), 3, ["foo"])
    new_dc = dc.move_z_layer(2)
    assert new_dc.z_layer == 5
    new_dc = dc.move_z_layer(-1)
    assert new_dc.z_layer == 2


def test_move_to():
    dc = DrawCall(Position(1, 2), 3, ["foo"])
    new_pos = Position(5, 6)
    new_dc = dc.move_to(new_pos)
    assert new_dc.position == new_pos
    assert new_dc.z_layer == dc.z_layer


def test_move_by():
    dc = DrawCall(Position(1, 2), 3, ["foo"])
    new_dc = dc.move_by(row_delta=2, col_delta=3)
    assert new_dc.position.row == 3
    assert new_dc.position.col == 5


def test_move_up_down_left_right():
    dc = DrawCall(Position(5, 5), 0, ["foo"])
    assert dc.move_up().position.row == 4
    assert dc.move_down().position.row == 6
    assert dc.move_left().position.col == 4
    assert dc.move_right().position.col == 6
    # Test with amount
    assert dc.move_up(3).position.row == 2
    assert dc.move_right(2).position.col == 7


def test_clip_content_basic():
    dc = DrawCall(Position(0, 0), 0, ["abcdef", "ghijkl"], width=4)
    clipped = dc.clip_content()
    assert clipped == ["abcd", "ghij"]


def test_clip_content_height():
    dc = DrawCall(Position(0, 0), 0, ["a", "b", "c", "d"], height=2)
    clipped = dc.clip_content()
    assert clipped == ["a", "b"]


def test_clip_content_width_and_height():
    dc = DrawCall(Position(0, 0), 0, ["abcdef", "ghijkl", "mnopqr"], width=3, height=2)
    clipped = dc.clip_content()
    assert clipped == ["abc", "ghi"]


def test_clip_content_args_override():
    dc = DrawCall(Position(0, 0), 0, ["abcdef"], width=6)
    clipped = dc.clip_content(width=2)
    assert clipped == ["ab"]
    clipped = dc.clip_content(height=0)
    assert clipped == []


def test_wrap_content_basic():
    dc = DrawCall(Position(0, 0), 0, ["abcdef", "ghijkl"], width=3)
    wrapped = dc.wrap_content()
    assert wrapped == ["abc", "def", "ghi", "jkl"]


def test_wrap_content_height():
    dc = DrawCall(Position(0, 0), 0, ["abcdef", "ghijkl"], width=3, height=2)
    wrapped = dc.wrap_content()
    assert wrapped == ["abc", "def"]


def test_wrap_content_args_override():
    dc = DrawCall(Position(0, 0), 0, ["abcdef"], width=6)
    wrapped = dc.wrap_content(width=2)
    assert wrapped == ["ab", "cd", "ef"]
    wrapped = dc.wrap_content(height=1)
    assert wrapped == ["abcdef"]


def test_clip_and_wrap_preserves_ansi():
    """
    Ensure that clipping and wrapping preserve ANSI escape codes and visible text.
    """
    import os
    os.environ.setdefault("TERM", "xterm-256color")

    term = Terminal(force_styling=True)
    red_text = term.red("abcdef")
    print(red_text)  # For debugging
    dc = DrawCall(Position(0, 0), 0, [red_text], width=3)

    clipped = dc.clip_content()
    # ANSI codes should be present in clipped output
    assert "\x1b[" in clipped[0]
    # Visible text should be present after stripping ANSI
    assert "abc" in term.strip_seqs(clipped[0])

    wrapped = dc.wrap_content()
    # Each wrapped segment should either contain ANSI or be empty
    assert all("\x1b[" in seg or seg == "" for seg in wrapped)
    # First wrapped segment should contain visible text
    assert "abc" in term.strip_seqs(wrapped[0])


def test_iter_graphemes_basic():
    # Should yield graphemes and ANSI codes
    s = "a\x1b[31mbc\x1b[0md"
    graphemes = list(DrawCall._iter_graphemes(s))
    # Should include the ANSI codes as separate segments
    assert any(g.startswith("\x1b[") for g in graphemes)
    # Should include all visible characters
    visible = [g for g in graphemes if not g.startswith("\x1b")]
    assert "a" in visible and "b" in visible and "c" in visible and "d" in visible


def test_clip_and_wrap_unicode_wide():
    # Wide unicode chars (e.g., emoji)
    emoji = "😀😀😀😀"
    term = Terminal(force_styling=True)
    # Each emoji typically occupies 2 terminal columns. Use visual width checks.
    dc = DrawCall(Position(0, 0), 0, [emoji], width=2)
    clipped = dc.clip_content()
    # Visible width should be at least 2 (we shouldn't split the emoji into half-cells)
    assert term.length(clipped[0]) >= 2
    wrapped = dc.wrap_content()
    # Each wrapped segment should be at most the configured visual width and contain whole emoji
    assert all(term.length(seg) <= 2 for seg in wrapped)
    assert all("😀" in seg or seg == "" for seg in wrapped)


@pytest.mark.parametrize(
    "input_line,expected",
    [
        # Simple grapheme
        ("a", ["a"]),
        # Simple ANSI escape
        ("\x1b[31ma", ["\x1b[31m", "a"]),
        # Multiple ANSI and graphemes
        ("\x1b[31ma\x1b[0mb", ["\x1b[31m", "a", "\x1b[0m", "b"]),
        # Mixed: emoji, ANSI, combining
        ("\x1b[32m😀é\x1b[0m", ["\x1b[32m", "😀", "é", "\x1b[0m"]),
        # Complex: ANSI, emoji, combining, normal
        ("\x1b[1;31mÁ😀\x1b[0mB", ["\x1b[1;31m", "Á", "😀", "\x1b[0m", "B"]),
        # Edge: consecutive ANSI
        ("\x1b[31m\x1b[1mA", ["\x1b[31m", "\x1b[1m", "A"]),
        # Edge: ANSI at end
        ("A\x1b[0m", ["A", "\x1b[0m"]),
    ]
)
def test_iter_graphemes_param(input_line, expected):
    result = list(DrawCall._iter_graphemes(input_line))
    assert result == expected
