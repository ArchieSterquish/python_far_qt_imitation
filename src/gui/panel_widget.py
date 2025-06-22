from PyQt6.QtWidgets import(QWidget,QGridLayout,)
from PyQt6.QtCore import Qt
import os

from system_api import KEY
from system_api import SystemAPI
from .panel import Panel
from .panel import PathLabel
# set with mind that settings are stored in some sort of file
LEFT_PANEL_PATH  = os.path.expanduser("~")
RIGHT_PANEL_PATH = os.path.expanduser("~")

MAX_VISIBLE_PATH_LENGTH = 100

# TODO:
#   make so panel doesn't lose focus when bottom bar button is pressed
class PanelsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.last_focused_panel = "left panel" # for case when panel becomes unfocused 
        self.setup_ui()

    def shorten_path(self,path):
        if len(path) > MAX_VISIBLE_PATH_LENGTH:
            path = "..." + path[len(path) - MAX_VISIBLE_PATH_LENGTH:]
        return path

    # TODO: rethink to use last_focused_panel here to determine which panel to update or better store reference to focused panel
    def update_panel(self,panel_name):
        if (panel_name == "left panel"):
            self.left_panel.update()
        if (panel_name == "right panel"):
            self.right_panel.update()

    def get_focused_file_or_folder(self):
        path,focused_panel = self.get_focused_panel_path()
        if (focused_panel == "left panel"):
            return SystemAPI.join(path,self.left_panel.get_current_file_or_folder())
        if (focused_panel == "right panel"):
            return SystemAPI.join(path,self.right_panel.get_current_file_or_folder())

    def get_focused_panel_path(self):
        if self.left_panel.hasFocus():
            self.last_focused_panel = "left panel"
            return (self.left_panel.path,"left panel")
        if self.right_panel.hasFocus():            
            self.last_focused_panel = "right panel"
            return (self.right_panel.path,"right panel")
    
    # FIXME: can't change location in unfocused panel without focusing on it 
    # How it works in far:
    #   When left panel is focused and when you try to change right panel location 
    #   it changes right panel location 
    #   and when it changes left panel is still left focused
    # Currently:
    #   When changing location on unfocused panel after chaning location 
    #   it switches focus to unfocused panel 
    #   but it should change focus if user does it using TAB key
    def keyPressEvent(self,event):
        # Workaround to change location on unfocused panels
        # using setFocus breaks the app because it changes focus to another panel but leaving ChangeLocationWidget hang in the QThread but 
        if event.key() == KEY.F1 and event.modifiers() == Qt.KeyboardModifier.AltModifier and not self.left_panel.hasFocus():
            self.left_panel.show_change_location()
        elif event.key() == KEY.F2 and event.modifiers() == Qt.KeyboardModifier.AltModifier and not self.right_panel.hasFocus():
            self.right_panel.show_change_location()
        super().keyPressEvent(event) # to allow app.py use it's bindings

    def update_label_path(self, emitted_panel_name):
        change_highlight_focus_panel = lambda path, label,other_label:(
            label.setText(self.shorten_path(path)),
            label.highlight(),
            other_label.unhighlight()
        )
        if emitted_panel_name == "left panel":
            change_highlight_focus_panel(self.left_panel.path, self.left_panel_path_label, self.right_panel_path_label)
        if emitted_panel_name == "right panel":
            change_highlight_focus_panel(self.right_panel.path, self.right_panel_path_label, self.left_panel_path_label)
       
    def setup_ui(self):
        layout = QGridLayout()

        self.left_panel  = Panel("left panel", LEFT_PANEL_PATH)
        self.right_panel = Panel("right panel", RIGHT_PANEL_PATH)

        self.left_panel_path_label = PathLabel(self.left_panel.path,self.palette())
        self.right_panel_path_label = PathLabel(self.right_panel.path,self.palette())

        self.left_panel.change_label_signal.connect(self.update_label_path)
        self.right_panel.change_label_signal.connect(self.update_label_path)
        
        layout.addWidget(self.left_panel_path_label, 0, 0)  
        layout.addWidget(self.right_panel_path_label, 0, 1)  

        layout.addWidget(self.left_panel, 1, 0)  
        layout.addWidget(self.right_panel, 1, 1)  
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)
