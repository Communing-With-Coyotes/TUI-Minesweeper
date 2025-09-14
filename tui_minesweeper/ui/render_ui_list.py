
from typing import List
from blessed import Terminal

from tui_minesweeper.position import Position
from tui_minesweeper.ui.compositor import Compositor
from tui_minesweeper.ui.draw_call import DrawCall
from .ui_list import UIList, Orientation


def render_ui_list(ui_list: UIList, compositor: Compositor, position: Position = Position(0, 0), z_layer: int = 0) -> DrawCall:
    """
    Render the list items with separation.
    Returns a list of strings for each line.

    Args:
        ui_list (UIList): The UIList to render.
        term (blessed.Terminal): Terminal instance for color formatting.

    Returns:
        List[str]: Rendered lines for the UI list.
    """
    rendered_items: List[str] = []

    for item_index, item in enumerate(ui_list._items):
        is_selected: bool = item_index == ui_list._selected_index

        symbol: str = ""
        if is_selected and item.selected_symbol is not None:
            symbol = f"{item.selected_symbol.to_blessed(compositor.terminal)} "
        elif item.symbol is not None:
            symbol = f"{item.symbol.to_blessed(compositor.terminal)} "

        if is_selected:
            color_pair = item.selected_color if item.selected_color is not None else ui_list.selected_color
        else:
            color_pair = item.color if item.color is not None else ui_list.color
        content: str = color_pair.to_blessed(compositor.terminal, item.text)

        rendered_item: str = f"{symbol}{content}"
        rendered_items.append(rendered_item)

    # Handle separators and orientation
    if ui_list.orientation == Orientation.VERTICAL:
        if ui_list.separator:
            separated_items = []
            for i, item in enumerate(rendered_items):
                separated_items.append(item)
                # Add separator after each item except the last
                if i < len(rendered_items) - 1:
                    separated_items.append(ui_list.separator)
            final_content = separated_items
        else:
            final_content = rendered_items
    else:  # Orientation.HORIZONTAL
        if ui_list.separator:
            final_content = [ui_list.separator.join(rendered_items)]
        else:
            final_content = [" ".join(rendered_items)]

    return DrawCall(
        position=position,
        z_layer=z_layer,
        content=final_content,
    )
