"""
Unit tests for DrawCall and Compositor classes in tui_minesweeper.ui.compositor.
"""
import pytest
from tui_minesweeper.ui.compositor import DrawCall, Compositor
from tui_minesweeper.rect import Position

class DummyTerminal:
    width = 10
    height = 5
    home = "<HOME>"
    clear = "<CLEAR>"

def test_drawcall_clip_content_width_and_height():
    dc = DrawCall(
        position=Position(0, 0),
        z_layer=0,
        content=["abcdefghij", "klmnopqrst", "uvwxyz"],
        width=8,
        height=2,
    )
    clipped = dc.clip_content()
    assert clipped == ["abcdefgh", "klmnopqr"]

    clipped2 = dc.clip_content(width=5, height=1)
    assert clipped2 == ["abcde"]

    # Passing None falls back to instance width/height
    clipped3 = dc.clip_content(width=None, height=None)
    assert clipped3 == ["abcdefgh", "klmnopqr"]


def test_drawcall_wrap_content_width_and_height():
    dc = DrawCall(
        position=Position(0, 0),
        z_layer=0,
        content=["abcdefghij klmno", "pqrst uvwxyz"],
        width=8,
        height=3,
    )
    wrapped = dc.wrap_content()
    # Should wrap lines to width=8, max 3 lines
    assert wrapped == ["abcdefgh", "ij klmno", "pqrst uv"]

    wrapped2 = dc.wrap_content(width=5, height=2)
    assert wrapped2 == ["abcde", "fghij"]

    # Passing None falls back to instance width/height
    wrapped3 = dc.wrap_content(width=None, height=None)
    assert wrapped3 == ["abcdefgh", "ij klmno", "pqrst uv"]


def test_compositor_add_text_and_draw(monkeypatch, capsys):
    # Patch Compositor.terminal property to return DummyTerminal
    monkeypatch.setattr(
        "tui_minesweeper.ui.compositor.Compositor.terminal",
        property(lambda self: DummyTerminal)
    )
    comp = Compositor()
    comp.add_text("hello", col=2, row=1, z_layer=0)
    comp.add_text(["world", "!"], col=0, row=0, z_layer=1)
    comp.draw()
    out = capsys.readouterr().out
    # Should print home+clear, then world, !, then hello
    assert out.startswith(DummyTerminal.home + DummyTerminal.clear)
    assert "world" in out
    assert "!" in out
    assert "hello" in out
    # Draw queue should be cleared
    assert comp._draw_calls == []


def test_compositor_add_draw_call():
    comp = Compositor()
    dc = DrawCall(position=Position(1, 2), z_layer=0, content=["foo"])
    comp.add_draw_call(dc)
    assert comp._draw_calls == [dc]


def test_compositor_draw_z_layer_order(monkeypatch, capsys):
    comp = Compositor()
    monkeypatch.setattr("tui_minesweeper.ui.compositor.Terminal", lambda: DummyTerminal())
    comp.add_text("layer0", col=0, row=0, z_layer=0)
    comp.add_text("layer2", col=0, row=0, z_layer=2)
    comp.add_text("layer1", col=0, row=0, z_layer=1)
    comp.draw()
    out = capsys.readouterr().out
    # Should print in z_layer order: layer0, layer1, layer2
    idx0 = out.find("layer0")
    idx1 = out.find("layer1")
    idx2 = out.find("layer2")
    assert idx0 < idx1 < idx2
