import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import LXSettings
from targets import *

class __page_home(LXSettings.DirectoryPage):
    def __init__(self):
        super().init_begin()
        
        self.items = [
            *target_buttons,
            LXSettings.DirectoryButton(
                icon_name = "preferences-system",
                label_str = "Administrative Settings",
                description_str = "Internal use only.",
                onclick_page_str = "Home -> Administrative Settings",
            )
        ]
        self.page_path_str = "Home"
        self.page_name = "Home"
        self.icon_name = "user-home"
        
        super().init_end()

page_home = __page_home()
