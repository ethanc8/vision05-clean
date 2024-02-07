import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

# import pages

import subprocess
import os

from typing import Callable, Any

## Declare singletons

main_breadcrumb = None
main_stack = None

## Open Process function

def open_process(args, addenv={}):
    subprocess.Popen(args, env={
        **os.environ,
        **addenv,
    })

def open_process_sudo(args, addenv={}):
    open_process(["sudo", "-A"] + args, {
        "SUDO_ASKPASS" : "/usr/lib/rc-gui/pwdrcg.sh",
        **addenv
    })

## Main Stack

class MainStack(Gtk.Stack):
#     pages = []
    pages_dict = {}
    # - Instance methods and variables
    def __init__(self):
#         print("MainStack() called")
        super().__init__()
#         print(self.pages)
#         for page in self.pages:
#             self.addPage(page)
#         self.navigateToPage("Home")
#         self.navigateToPage("Home -> Appearance")
#         self.navigateToPage("Home")
        # self.pages = self.pages.copy()
        self.current_page = None

    def addPage(self, page):
        # print("addPageToMainStack(" + str(self) + ", " + str(page) + ", \"" + str(pageName) + "\"")
        pageName = page.page_path_str
#         print("Adding page: " + pageName)
        self.add_named(page.top_widget, pageName)
        self.pages_dict[pageName] = page
        # page.top_widget.show()

    def navigateToPage(self, pageName: str):
        page = self.pageForPageName(pageName)
        page.on_enter()
        
        if self.current_page != None:
            self.current_page.on_exit()

        self.props.visible_child = page.top_widget

        self.current_page = page
        main_breadcrumb.update()

    def pageForPageName(self, pageName: str):
#         print(self.pages_dict)
        return self.pages_dict[pageName]




## Pages

class Page:
    def __init__(self):
        self.init_begin() # What needs to be done before variable initialization
        self.init_end() # What needs to be done after variable initialization by subclasses
    
    def init_begin(self):
        self.items = []
        self.page_path_str = ""
        self.page_name = ""
        self.icon_name = ""
    
    def init_end(self):
        main_stack.addPage(self)


    @property
    def icon_widget(self, icon_size: Gtk.IconSize):
        return Gtk.Image.new_from_icon_name(self.icon_name, icon_size) 


    def on_enter(self):
        self.on_enter_begin()
        self.on_enter_end()
    
    def on_enter_begin(self):
        pass

    def on_enter_end(self):
        pass


    def on_exit(self):
        self.on_exit_begin()
        self.on_exit_end()
    
    def on_exit_begin(self):
        pass

    def on_exit_end(self):
        pass

class DirectoryPage(Page):
    def __init__(self):
        self.init_begin()
        self.init_end()

    def init_begin(self):
        super().init_begin()
        
        self.top_widget = Gtk.ScrolledWindow()
        self.top_widget.set_policy(hscrollbar_policy = Gtk.PolicyType.NEVER, vscrollbar_policy = Gtk.PolicyType.AUTOMATIC)

        self.top_widget.props.hexpand = True
        self.top_widget.props.vexpand = True

        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(30)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        
        self.top_widget.add(self.flowbox)

    def init_end(self):
        self.init_flowbox()

        super().init_end()
        self.top_widget.show()

    # @property
    # def main_widget(self):
    #     return self.top_widget

    def init_flowbox(self):
        for item in self.items:
            # self.flowbox.add(DirectoryButton(
            #     icon_name = item[0], label_str = item[1],
            #     description_str = item[2], onclick = item[3]
            # ))
            self.flowbox.add(item)

class XEmbedPage(Page):
    def __init__(self):
        self.init_begin()
        self.init_end()

    def init_begin(self):
        super().init_begin()
        self.top_widget = Gtk.Box()
    
    def init_end(self):
        super().init_end()
        self.top_widget.show()
        

    def on_enter(self):
        self.on_enter_begin()
        self.on_enter_end()

    def on_enter_begin(self):
        super().on_enter_begin()

        self.socket = Gtk.Socket()

        self.socket.props.hexpand = True
        self.socket.props.vexpand = True

        self.socket.show()
        self.top_widget.add(self.socket)
        self.top_widget.show()

        self.window_id = self.socket.get_id() 
        
    def on_enter_end(self):
        super().on_enter_end()

    def on_exit(self):
        self.on_exit_begin()
        self.on_exit_end()
    
    def on_exit_begin(self):
        pass

    def on_exit_end(self):
        self.socket.get_plug_window().destroy()
    




## Buttons

class Button(Gtk.Button):
    def __init__(self):
        super().__init__()

class DirectoryButton(Button):
    def __init__(
        self, icon_widget: Gtk.Widget = None, icon_name: str = None,
        label_widget: Gtk.Widget = None, label_str: str = None,
        description_widget: Gtk.Widget = None, description_str: str = None,
        onclick: Callable[[Gtk.Widget], Any] = None, onclick_page_str: str = None, onclick_command: list = None
    ):
        super().__init__()
        self.grid = Gtk.Grid()
        self.add(self.grid)
        
        self.props.hexpand = True
        self.props.vexpand = True
        
        # - Gtk.Grid.attach(child, left, top, width, height)
        # | child  | Gtk.Widget | the widget to attach to the grid         |
        # | left   | int        | the row number of the top-left corner    |
        # | top    | int        | the column number of the top-left corner |
        # | width  | int        | the amount of columns spanned            |
        # | height | int        | the amount of rows spanned               |
        
        # Set up icon

        if icon_widget == None:
            if icon_name == None:
                icon_widget = Gtk.Image.new_from_icon_name("preferences-desktop", Gtk.IconSize.DIALOG)  
            else:
                icon_widget = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.DIALOG) 

        self.grid.attach(icon_widget, left=0, top=0, width=1, height=2)

        # Set up label
        
        if label_widget == None:
            if label_str == None:
                label_widget = Gtk.Label.new()
                label_widget.set_markup("<big><b>???</b></big>")
            else:
                label_widget = Gtk.Label.new()
                label_widget.set_markup("<big><b>" + label_str + "</b></big>")
        
        label_widget.props.hexpand = True
        label_widget.props.vexpand = True
        label_widget.props.justify = Gtk.Justification.LEFT
        label_widget.props.halign = Gtk.Align.START
        label_widget.props.wrap = True
        label_widget.props.wrap_mode = Pango.WrapMode.WORD_CHAR
        
        self.grid.attach(label_widget, left=1, top=0, width=1, height=1)
        
        # Set up description
        
        if description_widget == None:
            if description_str == None:
                description_widget = Gtk.Label.new()
            else:
                description_widget = Gtk.Label.new()
                description_widget.set_markup(description_str)
        
        description_widget.props.hexpand = True
        description_widget.props.vexpand = True
        description_widget.props.justify = Gtk.Justification.LEFT
        description_widget.props.halign = Gtk.Align.START
        label_widget.props.wrap = True
        label_widget.props.wrap_mode = Pango.WrapMode.WORD_CHAR

        self.grid.attach(description_widget, left=1, top=1, width=1, height=1)
        
        # Set up `onclick` action

        if onclick == None:
            if onclick_command != None:
                # print("Using onclick_command")
                onclick = lambda _: [
                    # print("Performing command " + str(onclick_command)),
                    open_process(onclick_command),
                ]
            elif onclick_page_str != None:
                # print("Using onclick_page_str")
                onclick = lambda _: [
                    # print("Navigating to page " + onclick_page_str),
                    main_stack.navigateToPage(onclick_page_str),
                ]
            else:
                print("Warning: onclick is None")
                print("onclick_page_str = " + onclick_page_str)
                print("onclick_command = " + str(onclick_command))

                onclick = lambda _: [
                    # print("Doing nothing...")
                ]

        self.connect("clicked", onclick)
        # print("Onclick connected!")

        # button = super().new_from_icon_name(icon_name, Gtk.IconSize.DIALOG)
        # button.connect("clicked", onclick)
        # button.props.label = button_label
        # button.props.always_show_image = True
        # button.props.image_position = Gtk.PositionType.TOP
        # return button
    


## Breadcrumbs

class Breadcrumb(Gtk.Box):
    pagePath = []
    def __init__(self):
        super().__init__()
        Button.new_from_icon_name("user-home", Gtk.IconSize.BUTTON)
        
        self.pagePath = ["Home"]
        
        self.add_button("user-home", "Home", "Home")
    
    def add_button(self, icon_name, label_str, page_path_str):
#         print("add_button (" + str(self) + ',  \"' + str(icon_name) + '", "' + str(label_str) + '", "' + str(page_path_str) + '")')
        button = Button.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
        button.connect("clicked", lambda sender: [
            main_stack.navigateToPage(page_path_str),
        ])
        button.props.label = label_str
        button.props.always_show_image = True
        button.props.image_position = Gtk.PositionType.LEFT
        self.add(button)
        button.show()
        self.show()
    
    def remove_buttons(self):
        for widget in self.get_children():
            widget.destroy()
    
    def update(self):
        self.remove_buttons()
#         print("Updating breadcrumb...")
        self.pagePath = main_stack.current_page.page_path_str.split(" -> ")
        for pageNameIndex in range(0, len(self.pagePath)):
#             print("self.pagePath: " + str(self.pagePath))
            pageName = self.pagePath[pageNameIndex]
            if pageName == "Home":
                self.add_button("user-home", "Home", "Home")
            else:
                pagePathString = " -> ".join(self.pagePath[0:pageNameIndex+1])
#                 print("pagePathString: " + pagePathString)
                self.add_button(main_stack.pageForPageName(pagePathString).icon_name , pageName, pagePathString)
            



## Define singletons

main_stack = MainStack()
main_breadcrumb = Breadcrumb()







       
        
        
        
        
        
















