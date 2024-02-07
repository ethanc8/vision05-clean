import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import LXSettings
import datetime
import pathlib

class Target():
    def __init__(self, name: str, username: str, number: int):
        self.name = name
        self.username = username
        self.number = number
        self.firstVictimDay = datetime.date(2022, 2, 10+number)
    
    def isVictim(self) -> bool:
        return datetime.date.today() <= self.firstVictimDay

class TargetDirectoryButton(LXSettings.DirectoryButton):
    def __init__(self, target: Target):
        self.target = target
        super().__init__(label_str=target.name, onclick_page_str=f"Home -> {target.name}")

class TargetPage(LXSettings.DirectoryPage):
    def __init__(self, target: Target):
        super().init_begin()
        
        self.items = [
            LXSettings.DirectoryButton(
                icon_name = "camera-photo",
                label_str = "Take headshot", 
                description_str = 
"""Take a headshot of this person.""",
                onclick_command = ['python3', str(pathlib.Path(__file__).parent.resolve() / ".." / "playgrounds" / "headshot.py"), target.username],
            )
        ]
        self.page_path_str = f"Home -> {target.name}"
        self.page_name = target.name
        self.icon_name = "preferences-desktop-theme"
        
        super().init_end()
        
