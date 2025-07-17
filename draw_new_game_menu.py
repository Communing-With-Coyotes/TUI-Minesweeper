import terminal
from term_colors import *

from minefield import Minefield
import draw_minefield

from menus.new_game_menu import NewGameMenu
from menus.draw_menu import DrawMenu, PREFIX_KEY
from ui_symbols import UP_DOWN_ARROW

def draw(game_menu: NewGameMenu) -> None:
    term = terminal.get_terminal()

    game_width, game_height = game_menu.game_size()
    mine_count = game_menu.mine_count

    minefield = Minefield(game_width, game_height, mine_count)

    terminal.reset()

    print(term.move_xy(2, 2), end='')
    draw_minefield.draw(minefield)
    print(f"{term.move_down(2)}{term.move_right(2)}", end='')

    # Prepare labels with values
    labels = [
        f"START GAME",
        f"WIDTH {game_width}",
        f"HEIGHT {game_height}",
        f"MINES {mine_count}"
    ]

    menu = DrawMenu(game_menu, layout=DrawMenu.LayoutStyles.HORIZONTAL)

    # Set styles for each menu item
    menu.set_style(NewGameMenu.MenuItems.START_GAME,
                  fg_color=EMERALD.fg() if game_menu.is_selected(NewGameMenu.MenuItems.START_GAME) else BROWN.fg(),
                  bg_color=BLACK.bg())
    menu.set_style(NewGameMenu.MenuItems.GAME_WIDTH,
                  fg_color=EMERALD.fg() if game_menu.is_selected(NewGameMenu.MenuItems.GAME_WIDTH) else BROWN.fg(),
                  bg_color=BLACK.bg(),
                  **{PREFIX_KEY: UP_DOWN_ARROW if game_menu.is_selected(NewGameMenu.MenuItems.GAME_WIDTH) else ""})
    menu.set_style(NewGameMenu.MenuItems.GAME_HEIGHT,
                  fg_color=EMERALD.fg() if game_menu.is_selected(NewGameMenu.MenuItems.GAME_HEIGHT) else BROWN.fg(),
                  bg_color=BLACK.bg(),
                  **{PREFIX_KEY: UP_DOWN_ARROW if game_menu.is_selected(NewGameMenu.MenuItems.GAME_HEIGHT) else ""})
    menu.set_style(NewGameMenu.MenuItems.MINE_COUNT,
                  fg_color=EMERALD.fg() if game_menu.is_selected(NewGameMenu.MenuItems.MINE_COUNT) else BROWN.fg(),
                  bg_color=BLACK.bg(),
                  **{PREFIX_KEY: UP_DOWN_ARROW if game_menu.is_selected(NewGameMenu.MenuItems.MINE_COUNT) else ""})

    info_str = f"{Color.style(EMERALD, BLACK, 'PRESS [SPACE] TO SELECT')} {Color.style(RED, BLACK, '[Q] TO QUIT')}"

    print(term.move_x(4), end='')
    menu.draw(info_str=info_str, labels=labels)
