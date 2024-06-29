from enum import Enum

import terminal
import term_colors
import tiles

from minefield import Minefield
import draw_minefield


class GAME_STATE(Enum):
    NEW_GAME = 1,
    CURRENT_GAME = 2,
    DEAD = 3


def game_loop():
    term = terminal.get_terminal()
    minefield = Minefield(10, 10, 20)
    game_state = GAME_STATE.NEW_GAME

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        key = ''
        draw_minefield.draw(minefield)

        # Handle key input
        while key.lower() != 'q':
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
                    minefield = Minefield(10, 10, 10)

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