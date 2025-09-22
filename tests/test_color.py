import pytest
import os
from blessed import Terminal
from tui_minesweeper.ui.color import Color, ColorPair

# Ensure tests run with a 256-color TERM so blessed emits color sequences.
os.environ.setdefault("TERM", "xterm-256color")

term = Terminal(force_styling=True)

def test_color_to_blessed_fg():
    color = Color(10, 20, 30)
    result = color.sequence(term, fg=True)
    assert isinstance(result, str)
    assert result == term.color_rgb(10, 20, 30)

def test_color_to_blessed_bg():
    color = Color(100, 150, 200)
    result = color.sequence(term, fg=False)
    assert isinstance(result, str)
    assert result == term.on_color_rgb(100, 150, 200)

def test_colorpair_to_blessed_fg_only():
    pair = ColorPair(fg=Color(1, 2, 3))
    content = "hello"
    result = pair.wrap(term, content)
    assert term.color_rgb(1, 2, 3) in result
    assert content in result
    # Should reset only the foreground color (SGR 39)
    assert result.endswith("\x1b[39m")

def test_colorpair_to_blessed_bg_only():
    pair = ColorPair(bg=Color(4, 5, 6))
    content = "world"
    result = pair.wrap(term, content)
    assert term.on_color_rgb(4, 5, 6) in result
    assert content in result
    # Should reset only the background color (SGR 49)
    assert result.endswith("\x1b[49m")

def test_colorpair_to_blessed_fg_and_bg():
    pair = ColorPair(fg=Color(7, 8, 9), bg=Color(10, 11, 12))
    content = "test"
    result = pair.wrap(term, content)
    assert term.color_rgb(7, 8, 9) in result
    assert term.on_color_rgb(10, 11, 12) in result
    assert content in result
    # Both fg and bg should be reset: FG (39) then BG (49)
    assert result.endswith("\x1b[39m\x1b[49m")
    # Background sequence should appear before the foreground sequence
    assert result.index(term.on_color_rgb(10, 11, 12)) < result.index(term.color_rgb(7, 8, 9))

def test_colorpair_to_blessed_none():
    pair = ColorPair()
    content = "plain"
    result = pair.wrap(term, content)
    # No color applied; content should be returned unchanged
    assert result == content


def test_color_channels_clamped_low_and_high():
    # Values below 0 should clamp to 0, above 255 should clamp to 255
    low = Color(-10, -1, -300)
    high = Color(256, 300, 1000)

    # Foreground clamps
    assert low.sequence(term, fg=True) == term.color_rgb(0, 0, 0)
    assert high.sequence(term, fg=True) == term.color_rgb(255, 255, 255)

    # Background clamps
    assert low.sequence(term, fg=False) == term.on_color_rgb(0, 0, 0)
    assert high.sequence(term, fg=False) == term.on_color_rgb(255, 255, 255)


def test_color_wrap_fg_and_bg_reset():
    # Ensure Color.wrap uses the correct reset depending on fg flag
    fg = Color(12, 34, 56)
    bg = Color(98, 76, 54)

    fg_wrapped = fg.wrap(term, "A", fg=True)
    assert fg_wrapped.startswith(term.color_rgb(12, 34, 56))
    assert fg_wrapped.endswith("\x1b[39m")
    assert "A" in fg_wrapped

    bg_wrapped = bg.wrap(term, "B", fg=False)
    assert bg_wrapped.startswith(term.on_color_rgb(98, 76, 54))
    assert bg_wrapped.endswith("\x1b[49m")
    assert "B" in bg_wrapped
