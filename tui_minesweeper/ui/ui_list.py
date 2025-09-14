
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum, auto

from .render_tile import RenderTile
from .color import ColorPair



class Orientation(Enum):
    VERTICAL = auto()
    HORIZONTAL = auto()



@dataclass(frozen=True)
class UIListItem:
    text: str = ""
    symbol: Optional[RenderTile] = None
    selected_symbol: Optional[RenderTile] = None
    color: Optional[ColorPair] = None
    selected_color: Optional[ColorPair] = None
    # Add more fields as needed for UI state, selection, etc.



class UIList:
    def __init__(
        self,
        color: ColorPair,
        selected_color: ColorPair,
        items: Optional[List[UIListItem]] = None,
        orientation: Orientation = Orientation.VERTICAL,
        separator: str = "",
    ) -> None:
        """
        Initialize a UIList.

        Args:
            color: Default ColorPair for items.
            selected_color: ColorPair for selected item.
            items: Optional initial list of UIListItem.
            orientation: Orientation of the list (VERTICAL or HORIZONTAL).
            separation_amount: Amount of separation between items.
            separator: String separator between items (default empty string).
        """
        self._items: List[UIListItem] = items if items is not None else []
        self._selected_index: Optional[int] = 0 if self._items else None
        self.color: ColorPair = color
        self.selected_color: ColorPair = selected_color
        self.orientation: Orientation = orientation
        self.separator: str = separator


    def __len__(self) -> int:
        return len(self._items)


    def __getitem__(self, index: int) -> UIListItem:
        return self._items[index]


    @property
    def selected_index(self) -> Optional[int]:
        return self._selected_index


    @selected_index.setter
    def selected_index(self, index: Optional[int]) -> None:
        if index is not None and 0 <= index < len(self._items):
            self._selected_index = index
        elif not self._items:
            self._selected_index = None


    def add_item(self, item: UIListItem) -> None:
        """
        Add a UIListItem to the list.
        """
        self._items.append(item)
        if self._selected_index is None:
            self._selected_index = 0


    def get_items(self) -> List[UIListItem]:
        """
        Return a copy of the list of UIListItems.
        """
        return self._items.copy()


    def get_selected_item(self) -> Optional[UIListItem]:
        """
        Return the currently selected UIListItem, or None if no selection.
        """
        if (
            self._selected_index is not None
            and 0 <= self._selected_index < len(self._items)
        ):
            return self._items[self._selected_index]
        return None


    def increment_selection(self, wrap: bool = False) -> None:
        """
        Move selection to the next item, optionally wrapping to the start.
        """
        if self._selected_index is not None and self._items:
            if self._selected_index < len(self._items) - 1:
                self._selected_index += 1
            elif wrap:
                self._selected_index = 0


    def decrement_selection(self, wrap: bool = False) -> None:
        """
        Move selection to the previous item, optionally wrapping to the end.
        """
        if self._selected_index is not None and self._items:
            if self._selected_index > 0:
                self._selected_index -= 1
            elif wrap:
                self._selected_index = len(self._items) - 1
