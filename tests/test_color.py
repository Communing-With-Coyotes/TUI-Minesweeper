import pytest
from blessed import Terminal
from tui_minesweeper.ui.color import Color, ColorPair

term = Terminal()

def test_color_to_blessed_fg():
    color = Color(10, 20, 30)
    result = color.to_blessed(term, fg=True)
    assert isinstance(result, str)
    assert result == term.color_rgb(10, 20, 30)

def test_color_to_blessed_bg():
    color = Color(100, 150, 200)
    result = color.to_blessed(term, fg=False)
    assert isinstance(result, str)
    assert result == term.on_color_rgb(100, 150, 200)

def test_colorpair_to_blessed_fg_only():
    pair = ColorPair(fg=Color(1, 2, 3))
    content = "hello"
    result = pair.to_blessed(term, content)
    assert term.color_rgb(1, 2, 3) in result
    assert content in result
    assert result.endswith(term.normal)

def test_colorpair_to_blessed_bg_only():
    pair = ColorPair(bg=Color(4, 5, 6))
    content = "world"
    result = pair.to_blessed(term, content)
    assert term.on_color_rgb(4, 5, 6) in result
    assert content in result
    assert result.endswith(term.normal)

def test_colorpair_to_blessed_fg_and_bg():
    pair = ColorPair(fg=Color(7, 8, 9), bg=Color(10, 11, 12))
    content = "test"
    result = pair.to_blessed(term, content)
    assert term.color_rgb(7, 8, 9) in result
    assert term.on_color_rgb(10, 11, 12) in result
    assert content in result
    assert result.endswith(term.normal)

def test_colorpair_to_blessed_none():
    pair = ColorPair()
    content = "plain"
    result = pair.to_blessed(term, content)
    assert result == content + term.normal
