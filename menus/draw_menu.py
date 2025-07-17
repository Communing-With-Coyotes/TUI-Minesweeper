from enum import IntEnum
from menus.menu import Menu
import terminal
from term_colors import *
from typing import Optional


SELECTED_STYLE_PREFIX = "selected_"
UNSELECTED_STYLE_PREFIX = "unselected_"
PREFIX_KEY = "prefix"
POSTFIX_KEY = "postfix"


class DrawMenu:

    class LayoutStyles(IntEnum):
        HORIZONTAL = 1
        VERTICAL = 2


    def __init__(self, menu: Menu, layout = LayoutStyles.VERTICAL):
        self.menu = menu 
        self.layout = layout

        self.menu_item_styles: dict[int, dict[str, str]] = {}


    # Each stylization should be passed as its own named argument, where the argument name is the type of stylization 
    # (bold, fg_color, underlined, etc.) and the value is the [string] terminal command that commands the terminal to 
    # use the requested stylization. Stylization names can be anything and simply exist as a simple way to access the 
    # stylization later. Stylizations can also be a combination of styles (bold and underlined, italic and green bg).
    # Stylizations can be made conditional by prefixing the name with a known condition:
    #
    # • NONE            — Stylization is always applied, unless there's another entry with the same name, with a prefix 
    #                     that overrides it.
    # • selected_       — Stylization is applied when the menu item is currently selected.
    # • unselected_     — Stylization is applied when the menu item is NOT currently selected.
    def set_style(self, menu_item_idx: int, **kwargs: str) -> None:
        self.menu_item_styles[menu_item_idx] = kwargs


    def remove_style(self, menu_item_idx: int) -> dict[str, str] | None:
        return self.menu_item_styles.pop(menu_item_idx, None)


    def add_to_style(self, menu_item_idx: int, name: str, term_command: str) -> None:
        if menu_item_idx not in self.menu_item_styles:
            self.menu_item_styles[menu_item_idx] = {}
        
        self.menu_item_styles[menu_item_idx][name] = term_command
    

    def remove_from_style(self, menu_item_idx: int, name: str) -> str | None:
        if menu_item_idx in self.menu_item_styles:
            return self.menu_item_styles[menu_item_idx].pop(name, None)
        
        return None


    def menu_item(self, idx: int, content: str) -> str:
        menu_item_style = self.menu_item_styles.get(idx, {})
        is_selected = self.menu.is_selected(idx)

        style_cmds = []
        prefix_str = ''
        postfix_str = ''

        # Unconditional styles (no prefix)
        for key, value in menu_item_style.items():
            if key == PREFIX_KEY:
                prefix_str = value
            elif key == POSTFIX_KEY:
                postfix_str = value
            elif not key.startswith(SELECTED_STYLE_PREFIX) and not key.startswith(UNSELECTED_STYLE_PREFIX):
                style_cmds.append(value)

        # Conditional styles
        prefix = SELECTED_STYLE_PREFIX if is_selected else UNSELECTED_STYLE_PREFIX
        for key, value in menu_item_style.items():
            if key.startswith(prefix):
                style_cmds.append(value)

        style_prefix = ''.join(style_cmds)
        style_suffix = terminal.get_terminal().normal

        return f"{style_prefix}{prefix_str}{content}{postfix_str}{style_suffix}"


    def draw(self, info_str: str = '', labels: Optional[list[str]] = None, item_callback = None) -> None:
        """
        Draws the menu to the terminal, including all menu items and an optional info/help string.
        :param info_str: String to display below the menu (e.g., help or info).
        :param labels: Optional list of labels for menu items, in order.
        :param item_callback: Optional callback (idx, label, selected) -> str for custom menu item rendering.
        """
        terminal.reset()

        items = []

        for idx in range(self.menu.item_count):
            label = labels[idx] if labels and idx < len(labels) else str(idx)
            selected = self.menu.is_selected(idx)

            item_str = ''
            if item_callback:
                item_str = item_callback(idx, label, selected)
            else:
                item_str = self.menu_item(idx, label)
            items.append(item_str)

        if self.layout == self.LayoutStyles.VERTICAL:
            for item in items:
                print(item)
        else:
            print('   '.join(items))

        if info_str:
            print(info_str)
