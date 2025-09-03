from tui_minesweeper.game import Game

def test_game_initialization():
    """Test basic game initialization parameters"""
    game = Game(width=8, height=8, mines=5)
    assert game.width == 8
    assert game.height == 8
    assert game.mines == 5
    assert hasattr(game, 'term')
