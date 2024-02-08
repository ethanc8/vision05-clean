import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# import pages
# import LXSettingsMainStack
import pages
import LXSettings

class __LXSettingsMainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="ECAI Targets")
        self.set_border_width(10)
        self.set_default_size(500, 500)
        
        self.top_widget = Gtk.Box()
        self.top_widget.props.orientation = Gtk.Orientation.VERTICAL
        self.top_widget.props.hexpand = True
        self.top_widget.props.vexpand = True
        
        self.top_widget.add(LXSettings.main_breadcrumb)
        self.top_widget.add(LXSettings.main_stack)
        self.add(self.top_widget)
        
        LXSettings.main_stack.navigateToPage("Home")
        
        self.show_all()


LXSettingsMainWindow = __LXSettingsMainWindow()
LXSettingsMainWindow.connect("destroy", Gtk.main_quit)
LXSettingsMainWindow.show_all()
Gtk.main()