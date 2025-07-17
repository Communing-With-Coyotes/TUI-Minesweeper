from abc import ABC
from enum import IntEnum


class Menu(ABC):
    """
    Abstract base class for menu navigation systems.
    Provides selection logic and index management for menu items.
    Subclasses should implement specific menu behaviors.
    """

    def __init__(self, item_count: int, initial_selection:int | IntEnum = 0):
        """
        Initialize the menu with a given number of items and an initial selection.
        :param item_count: Total number of selectable menu items (must be > 0).
        :param initial_selection: The initially selected menu item (default is 0).
        """
        assert item_count > 0, "A menu cannot be empty. It must contain at least one possible selection."

        self.item_count = item_count
        self.selected = initial_selection
    

    def select(self, menu_item:int | IntEnum) -> None:
        """
        Select a specific menu item.
        :param menu_item: The menu item to select (int or IntEnum).
        """
        self.selected = menu_item

    
    def is_selected(self, menu_item:int | IntEnum) -> bool:
        """
        Check if the given menu item is currently selected.
        :param menu_item: The menu item to check.
        :return: True if the menu item is selected, False otherwise.
        """
        return menu_item == self.selected
    

    def select_next_item(self, wrap: bool = False) -> None:
        """
        Select the next menu item.
        :param wrap: If True, wrap around to the first item when at the end.
        """
        idx = self.selected + 1
        self.selected = self._clamp_menu_item_idx(idx) if not wrap else self._wrap_menu_item_idx(idx)


    def select_prev_item(self, wrap: bool = False) -> None:
        """
        Select the previous menu item.
        :param wrap: If True, wrap around to the last item when at the beginning.
        """
        idx = self.selected - 1
        self.selected = self._clamp_menu_item_idx(idx) if not wrap else self._wrap_menu_item_idx(idx)


    def _wrap_menu_item_idx(self, idx: int) -> int:
        """
        Wrap the menu index around the valid range (0 to item_count - 1).
        :param idx: The index to wrap.
        :return: The wrapped index.
        """
        return idx % self.item_count


    def _clamp_menu_item_idx(self, idx: int) -> int:
        """
        Clamp the menu index to the valid range (0 to item_count - 1).
        :param idx: The index to clamp.
        :return: The clamped index.
        """
        return max( 0, min( self.item_count - 1, idx ) )

