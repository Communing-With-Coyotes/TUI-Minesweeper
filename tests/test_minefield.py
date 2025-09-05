import pytest
from tui_minesweeper.minefield import Minefield, Position, RevealResult


def test_minefield_initialization():
    mf = Minefield(rows=5, columns=5, mine_count=5)
    assert mf.rows == 5
    assert mf.columns == 5
    assert mf.mine_count == 5
    assert len(mf.mine_positions) == 5
    assert all(isinstance(pos, Position) for pos in mf.mine_positions)
    assert mf.adjacent_mine_counts.counts is not None
    assert len(mf.adjacent_mine_counts.counts) == 5
    assert len(mf.adjacent_mine_counts.counts[0]) == 5


def test_in_bounds():
    mf = Minefield(3, 3, 1)
    assert mf.in_bounds(0, 0)
    assert mf.in_bounds(2, 2)
    assert not mf.in_bounds(-1, 0)
    assert not mf.in_bounds(3, 0)
    assert not mf.in_bounds(0, 3)


def test_flag_and_unflag():
    mf = Minefield(3, 3, 1)
    mf.flag(1, 1)
    assert Position(1, 1) in mf.flagged_positions
    mf.unflag(1, 1)
    assert Position(1, 1) not in mf.flagged_positions


def test_is_flagged_correctly():
    mf = Minefield(3, 3, 1)
    mine = next(iter(mf.mine_positions))
    mf.flag(mine.row, mine.col)
    assert mf.is_flagged_correctly(mine.row, mine.col)
    mf.unflag(mine.row, mine.col)
    assert not mf.is_flagged_correctly(mine.row, mine.col)
    mf.flag(0, 0)
    if Position(0, 0) not in mf.mine_positions:
        assert not mf.is_flagged_correctly(0, 0)


def test_reveal_mine():
    mf = Minefield(3, 3, 1)
    mine = next(iter(mf.mine_positions))
    result = mf.reveal(mine.row, mine.col)
    assert result.hit_mine is True
    assert mine in result.newly_revealed
    assert mine in mf.revealed_positions
    assert mf.is_loss()


def test_reveal_numbered_cell():
    mf = Minefield(3, 3, 1)
    # Find a cell adjacent to a mine
    mine = next(iter(mf.mine_positions))
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            r, c = mine.row + dr, mine.col + dc
            if mf.in_bounds(r, c) and Position(r, c) not in mf.mine_positions:
                if mf.adjacent_mine_counts.counts[r][c] > 0:
                    result = mf.reveal(r, c)
                    assert result.hit_mine is False
                    assert Position(r, c) in result.newly_revealed
                    assert Position(r, c) in mf.revealed_positions
                    return
    pytest.skip("No numbered cell found")


def test_reveal_empty_cell_cascade():
    mf = Minefield(5, 5, 3)
    # Find a cell with 0 adjacent mines
    for row in range(5):
        for col in range(5):
            if mf.adjacent_mine_counts.counts[row][col] == 0:
                result = mf.reveal(row, col)
                assert result.hit_mine is False
                assert Position(row, col) in result.newly_revealed
                # Should reveal more than one cell
                assert len(result.newly_revealed) > 1
                for pos in result.newly_revealed:
                    assert pos in mf.revealed_positions
                return
    pytest.skip("No empty cell found")


def test_is_win():
    mf = Minefield(3, 3, 1)
    # Reveal all non-mine cells
    for row in range(3):
        for col in range(3):
            if Position(row, col) not in mf.mine_positions:
                mf.reveal(row, col)
    assert mf.is_win()
    assert not mf.is_loss()


def test_invalid_initialization():
    with pytest.raises(ValueError):
        Minefield(1, 1, 1)
    with pytest.raises(ValueError):
        Minefield(3, 3, 0)
    with pytest.raises(ValueError):
        Minefield(3, 3, 8)


def test_reveal_out_of_bounds():
    mf = Minefield(3, 3, 1)
    with pytest.raises(IndexError):
        mf.reveal(-1, 0)
    with pytest.raises(IndexError):
        mf.reveal(3, 3)


def test_reveal_already_revealed_or_flagged():
    mf = Minefield(3, 3, 1)
    mf.flag(0, 0)
    result = mf.reveal(0, 0)
    assert result.newly_revealed == set()
    mf.unflag(0, 0)
    result1 = mf.reveal(0, 0)
    result2 = mf.reveal(0, 0)
    assert result2.newly_revealed == set()
