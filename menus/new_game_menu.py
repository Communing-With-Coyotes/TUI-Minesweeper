from enum import IntEnum
from menus.menu import Menu

class NewGameMenu(Menu):

    class MenuItems(IntEnum):
        START_GAME = 1
        GAME_WIDTH = 2
        GAME_HEIGHT = 3
        MINE_COUNT = 4


    def __init__(self, game_width = 10, game_height = 10, mine_count = 20):
        super().__init__(len(self.MenuItems))

        self.game_width = max(2, game_width)
        self.game_height = max(2, game_height)
        self.mine_count = max(1, mine_count)

        self.selected = self.MenuItems.START_GAME
    

    def game_size(self):
        return (self.game_width, self.game_height)


    def increment_menu_item(self):
        if self.is_selected(self.MenuItems.GAME_WIDTH):
            self.game_width += 1
        elif self.is_selected(self.MenuItems.GAME_HEIGHT):
            self.game_height += 1
        elif self.is_selected(self.MenuItems.MINE_COUNT):
            self.mine_count += 1

        # Always ensure mine_count does not exceed available spaces
        self.mine_count = min(self.mine_count, self.game_width * self.game_height - 1)


    def decrement_menu_item(self):
        if self.is_selected(self.MenuItems.GAME_WIDTH):
            self.game_width = max(2, self.game_width - 1)
        elif self.is_selected(self.MenuItems.GAME_HEIGHT):
            self.game_height = max(2, self.game_height - 1)
        elif self.is_selected(self.MenuItems.MINE_COUNT):
            self.mine_count = max(1, self.mine_count - 1)

        # Ensure mine_count is valid after any change. We can't have more mines than available spaces.
        self.mine_count = min(self.mine_count, self.game_width * self.game_height - 1)

