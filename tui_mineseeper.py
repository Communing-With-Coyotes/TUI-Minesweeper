from enum import Enum

import terminal
import term_colors
import tiles

from minefield import Minefield
import draw_minefield

from menus.new_game_menu import NewGameMenu
import draw_new_game_menu

class GAME_STATE(Enum):
    NEW_GAME = 1,
    CURRENT_GAME = 2,
    DEAD = 3,
    DEBUG = 4


def game_loop():
    term = terminal.get_terminal()
    minefield = Minefield(10, 10, 20)
    game_state = GAME_STATE.NEW_GAME

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        key = ''
        should_quit = False

        new_game_menu = NewGameMenu()

        while not should_quit:
            # Draw the new game menu on starting the program, as we'll otherwise just sit here, 
            # waiting for the first input before we draw anything.
            draw_new_game_menu.draw(new_game_menu)

            key = term.inkey()

            if key.lower() == 'q':
                should_quit = True
                continue

            if game_state == GAME_STATE.NEW_GAME:
                draw_new_game_menu.draw(new_game_menu)

                if key.is_sequence:
                    if key.name == "KEY_UP":
                        new_game_menu.increment_menu_item()
                    elif key.name == "KEY_DOWN":
                        new_game_menu.decrement_menu_item()
                    elif key.name == "KEY_LEFT":
                        new_game_menu.select_prev_item()
                    elif key.name == "KEY_RIGHT":
                        new_game_menu.select_next_item()
                    elif key.name == 'KEY_INSERT':
                        game_state = GAME_STATE.DEBUG
                else:
                    # Start the game if the START GAME menu item is activated.
                    if key.lower() == ' ' and new_game_menu.is_selected(NewGameMenu.MenuItems.START_GAME):
                        game_state = GAME_STATE.CURRENT_GAME
                        

            elif game_state == GAME_STATE.CURRENT_GAME:

                if key.is_sequence:
                    if key.name == "KEY_UP":
                        minefield.move_selection(0, -1)
                    elif key.name == "KEY_DOWN":
                        minefield.move_selection(0, 1)
                    elif key.name == "KEY_LEFT":
                        minefield.move_selection(-1, 0)
                    elif key.name == "KEY_RIGHT":
                        minefield.move_selection(1, 0)
            else:
                pass

        # Handle key input
        while False: #key.lower() != 'q':
            key = term.inkey()

            # Switch to our death-state keymap. Other keys will do nothing in this state.
            if game_state == GAME_STATE.DEAD:
                if key.lower() == 'q':
                    break
                elif key.lower() != 'r':
                    continue
            elif game_state == GAME_STATE.NEW_GAME:
                draw_new_game_state()

            if key.is_sequence:
                if key.name == "KEY_UP":
                    minefield.move_selection(0, -1)
                elif key.name == "KEY_DOWN":
                    minefield.move_selection(0, 1)
                elif key.name == "KEY_LEFT":
                    minefield.move_selection(-1, 0)
                elif key.name == "KEY_RIGHT":
                    minefield.move_selection(1, 0)

                print(minefield.selected)
            else:
                if key == ' ':
                    dead = minefield.search_spot(*minefield.selected)

                    if dead:
                        game_state = GAME_STATE.DEAD

                        print( term_colors.wrap("You Died!", tiles.BLACK.fg(), tiles.RED.bg()), end = '' )
                        print( term.move_down, end = '' )
                        print( term_colors.wrap("Press 'q' to exit, or 'r' to restart.", tiles.BLACK.fg(), tiles.EMERALD.bg()), end = '' )

                elif game_state == GAME_STATE.DEAD and key == 'r':
                    minefield = Minefield(10, 10, 20)

                    print(f"{term.clear}", end = '')

            draw_minefield.draw(minefield)
    
    print(f"{term_colors.RESET_COLOR}")


def draw_new_game_state():
    pass


def main():
    terminal.check_for_terminal(
            """
                Sorry, this Minesweeper clone is meant to be played directly from a terminal.
                You shouldn't attempt to pipe the output.
            """)

    game_loop()

main()