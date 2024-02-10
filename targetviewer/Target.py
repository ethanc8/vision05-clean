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
        try:
            self.firstVictimDay = datetime.date(2024, 2, 10+number)
        except:
            self.firstVictimDay = datetime.date(2024, 12, 31)
    
    def isVictim(self) -> bool:
        return datetime.date.today() <= self.firstVictimDay

class TargetDirectoryButton(LXSettings.DirectoryButton):
    def __init__(self, target: Target):
        self.target = target
        super().__init__(
            icon_name = "user-info",
            label_str = target.name, 
            description_str = target.username,
            onclick_page_str = f"Home -> {target.name}")

class TargetPage(LXSettings.DirectoryPage):
    def __init__(self, target: Target):
        super().init_begin()
        
        self.items = [
            LXSettings.DirectoryButton(
                icon_name = "camera-photo",
                label_str = "Take headshot", 
                description_str = 
"""Take a headshot of this person.""",
                onclick_command = ['python3', str(pathlib.Path(__file__).parent.resolve() / ".." / "playgrounds" / "headshot.py"), target.username, target.name],
            )
        ]
        self.page_path_str = f"Home -> {target.name}"
        self.page_name = target.name
        self.icon_name = "user-info"
        
        super().init_end()
        
