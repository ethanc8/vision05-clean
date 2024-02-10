import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import subprocess
import pathlib

import LXSettings

class __page_home_admin(LXSettings.DirectoryPage):
    def __init__(self):
        super().init_begin()
        
        self.items = [
            LXSettings.DirectoryButton(
                icon_name = "document-save",
                label_str = "Pickle embeddings", 
                description_str = 
"""Calculate embeddings of the training data and write them to encodings.pickle.""",
                onclick_command = ['python3', str(pathlib.Path(__file__).parent.resolve() / ".." / "playgrounds" / "pickleEmbeddings.py")],
            )
        ]
        self.page_path_str = "Home -> Administrative Settings"
        self.page_name = "Administrative Settings"
        self.icon_name = "settings-configure"
        
        super().init_end()

page_home_appearance = __page_home_admin()
