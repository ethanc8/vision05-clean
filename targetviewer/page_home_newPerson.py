import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

import subprocess
import targets
import pathlib
import os
import sys

import LXSettings

class __page_home_newPerson(LXSettings.Page):
    def __init__(self):
        super().init_begin()

        # self.top_widget = Gtk.ScrolledWindow()
        # self.top_widget.set_policy(hscrollbar_policy = Gtk.PolicyType.NEVER, vscrollbar_policy = Gtk.PolicyType.AUTOMATIC)

        # self.top_widget.props.hexpand = True
        # self.top_widget.props.vexpand = True

        self.top_widget = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        # self.box.set_valign(Gtk.Align.START)
        # self.box.set_max_children_per_line(30)
        # self.box.set_selection_mode(Gtk.SelectionMode.NONE)
        
        self.name_entry = Gtk.Entry()
        self.top_widget.pack_start(self.name_entry, True, True, 0)

        self.make_button = Gtk.Button(label="Create New Person")
        self.top_widget.pack_start(self.make_button, True, True, 0)
        self.make_button.connect("clicked", self.make_person)


        # self.top_widget.add(self.box)

        self.page_path_str = "Home -> New Person"
        self.page_name = "New Person"
        self.icon_name = "list-add"
        
        super().init_end()
        self.top_widget.show()

    def make_person(self, _):
        print(f"We need to make a user named {self.name_entry.get_text()}")
        name = self.name_entry.get_text()
        username = "".join(name.split())
        number = targets.targets[-1].number + 1

        with open(pathlib.Path(__file__).parent.resolve() / 'targets.py', 'r') as file:
            filedata = file.read()

        filedata = filedata.replace('# !!! page_home_newPerson NEW TARGET !!!', f"""    Target(name="{name}",
           username="{username}",
           number={number}),
# !!! page_home_newPerson NEW TARGET !!!""")


        with open(pathlib.Path(__file__).parent.resolve() / 'targets.py', 'w') as file:
            file.write(filedata)
        
        print(f"Finished adding person {name}")
        # Restart the program
        os.execl(sys.executable, f'"{sys.executable}"', *sys.argv)

    def on_enter(self):
        super().on_enter_begin()

        

        super().on_enter_end()

page_home_newPerson = __page_home_newPerson()
