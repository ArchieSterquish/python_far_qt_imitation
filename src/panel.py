from PyQt6.QtWidgets import(
    QListWidget,
    QListWidgetItem,
    QWidget,
    QGridLayout,
    QLabel
)
from PyQt6.QtCore import pyqtSignal, QObject,Qt
import os
import re
from system_api import KEY
from system_api import SystemAPI
from PyQt6.QtGui import QColor, QBrush
# set with mind that settings are stored in some sort of file
LEFT_PANEL_PATH  = os.path.expanduser("~")
RIGHT_PANEL_PATH = os.path.expanduser("~")

MAX_VISIBLE_PATH_LENGTH = 100

COLOR_FOLDER = QBrush(QColor(255,165,0))
COLOR_FILE = QBrush(QColor(255,255,255))

COLOR_EXTENSIONS ={
    # Folders
    "folder": QBrush(QColor(255, 165, 0)),  # Orange
    
    # Programming files
    ".py": QBrush(QColor(65, 105, 225)),    # Royal Blue (Python)
    ".cpp": QBrush(QColor(100, 149, 237)),  # Cornflower Blue (C++)
    ".js": QBrush(QColor(240, 219, 79)),    # Yellow (JavaScript)
    ".html": QBrush(QColor(227, 79, 56)),   # Red-Orange (HTML)
    ".css": QBrush(QColor(86, 61, 124)),    # Purple (CSS)
    
    # Documents
    ".pdf": QBrush(QColor(220, 20, 60)),    # Crimson (PDF)
    ".docx": QBrush(QColor(0, 100, 0)),     # Dark Green (Word)
    ".doc": QBrush(QColor(0, 100, 0)),     # Dark Green (Word)
    ".xlsx": QBrush(QColor(0, 128, 0)),     # Green (Excel)
    
    # Media
    ".jpg": QBrush(QColor(218, 165, 32)),   # Goldenrod (Images)
    ".mp3": QBrush(QColor(138, 43, 226)),   # Blue Violet (Audio)
    ".mp4": QBrush(QColor(219, 112, 147)), # Pale Violet Red (Video)

    # archives
    ".7z": QBrush(QColor(255,0,255)), # magenta
    ".zip": QBrush(QColor(255,0,255)), # magenta
    ".tar": QBrush(QColor(255,0,255)), # magenta
    ".rar": QBrush(QColor(255,0,255)), # magenta
    
    # Default file color
    "_default": QBrush(QColor(200, 200, 200))  # Light Gray
}

class Panel(QListWidget):
    change_label_signal = pyqtSignal(str)
    def __init__(self,panel_name,path):
        super().__init__()
        self.panel_name = panel_name
        self.path = path
        self.update()

        self.list_of_appliable_keys = [
            KEY.ENTER,
            KEY.LEFT_ARROW,   
            KEY.RIGHT_ARROW,  
        ]
        self.setCurrentRow(0) 
        self.itemDoubleClicked.connect(self.open_folder)

    def focusInEvent(self, event):
        self.change_label_signal.emit(self.panel_name)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.change_label_signal.emit(self.panel_name)
        super().focusOutEvent(event)


    # TODO:
    # make so after deletion it goes to next item in the list instead of first one
    # if no items left just use setCurrentRow(0)
    def update(self):
        self.clear()

        files_list = SystemAPI.get_ff_list(self.path)
        directories_list = SystemAPI.get_directories_list(self.path)

        for d in directories_list:
            item = QListWidgetItem(d)
            item.setForeground(COLOR_FOLDER)  
            self.addItem(item)
        for f in files_list:
            item = QListWidgetItem(f)
            color = None
            for ext in sorted(COLOR_EXTENSIONS.keys(), key=len, reverse=True):
                if f.lower().endswith(ext.lower()):
                    color = COLOR_EXTENSIONS[ext]
                    break
            
            # Use default if no match found
            if color is None:
                color = COLOR_EXTENSIONS["_default"]

            item.setForeground(color)  
            self.addItem(item)
        # workaround to get focus after deletion
        self.setCurrentRow(0) 

    def open_directory(self,new_directory):
        previous_directory = None 
        previous_directory_name = None 

        if new_directory != '..':            
            self.path = os.path.join(self.path,new_directory)
        else:
            previous_directory = os.path.dirname(self.path)
            previous_directory_name = os.path.basename(self.path)
            self.path = previous_directory 
    
        self.update()

        files_list = SystemAPI.get_files_list(self.path)
        if previous_directory_name != None: # meaning we're going backwards
            last_position = files_list.index(previous_directory_name)
            self.setCurrentRow(last_position)
        else:
            self.setCurrentRow(0) # to avoid case when opening new directory it instantly loses focus on list elements
        self.change_label_signal.emit(self.panel_name)

    def get_current_file_or_folder(self):
        return self.currentItem().text()

    def open_folder(self):
        temp_path = os.path.join(self.path,self.currentItem().text())
        if SystemAPI.is_file(temp_path):
            SystemAPI.open_file_in_editor(temp_path)
        else: 
            self.open_directory(self.currentItem().text())
        pass

    def keyPressEvent(self, event):
        if event.key() not in self.list_of_appliable_keys:
            super().keyPressEvent(event)

        if not self.currentItem(): # if no items means we aren't focused or something else
            return

        if event.key() == Qt.Key.Key_Left:
            # Create a new event for Page Up
            new_event = type(event)(event.type(), 
                                  Qt.Key.Key_PageUp,
                                  event.modifiers())
            super().keyPressEvent(new_event)
        elif event.key() == Qt.Key.Key_Right:
            # Create a new event for Page Down
            new_event = type(event)(event.type(),
                                  Qt.Key.Key_PageDown,
                                  event.modifiers())
            super().keyPressEvent(new_event)

        if (event.key() == KEY.ENTER): 
            self.open_folder()

class PathLabel(QLabel):
    def __init__(self,text,palette):
        super().__init__(text)
        self.palette = palette
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def apply_style(self,style):
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {style['bg']};
                color: {style['text']};
                border: {style['border']};
            }}
        """)
        self.style().unpolish(self)
        self.style().polish(self)

    def highlight(self):
        self.apply_style({  # Standard highlight (theme default)
            'bg': self.palette.highlight().color().name(),
            'text': self.palette.highlightedText().color().name(),
            'border': 'none'
        })

    def unhighlight(self):
        self.apply_style({  # No highlight
            'bg': 'transparent',
            'text': self.palette.text().color().name(),
            'border': 'none'
        })

class PanelsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_panels()

    def shorten_path(self,path):
        if len(path) > MAX_VISIBLE_PATH_LENGTH:
            path = "..." + path[len(path) - MAX_VISIBLE_PATH_LENGTH:]
        return path

    def update_panel(self,panel_name):
        if (panel_name == "left panel"):
            self.left_panel.update()
        if (panel_name == "right panel"):
            self.right_path.update()

    def get_focused_file_or_folder(self):
        path,focused_panel = self.get_focused_panel_path()
        if (focused_panel == "left panel"):
            return os.path.join(path,self.left_panel.get_current_file_or_folder())
        if (focused_panel == "right panel"):
            return os.path.join(path,self.right_panel.get_current_file_or_folder())

    def get_focused_panel_path(self):
        if self.left_panel.hasFocus():
            return (self.left_panel.path,"left panel")
        if self.right_panel.hasFocus():            
            return (self.right_panel.path,"right panel")
        else:            
            print("BAD NO PANEL IS FOCUSED")
            return "/home/"

    def update_label_path(self,emitted_panel_name):
        """ called when one of the panels changes directory and emits signal"""
        if (emitted_panel_name == "left panel"):
            path = self.shorten_path(self.left_panel.path)
            self.left_panel_path_label.setText(path)
            self.left_panel_path_label.highlight()
            self.right_panel_path_label.unhighlight()
        if (emitted_panel_name == "right panel"):
            path = self.shorten_path(self.right_panel.path)
            self.right_panel_path_label.setText(path)
            self.right_panel_path_label.highlight()
            self.left_panel_path_label.unhighlight()
       
    def _init_panels(self):
        layout = QGridLayout()
        # init panels
        self.left_panel  = Panel("left panel", LEFT_PANEL_PATH)
        self.right_panel = Panel("right panel", RIGHT_PANEL_PATH)

        self.left_panel_path_label = PathLabel(self.left_panel.path,self.palette())
        self.right_panel_path_label = PathLabel(self.right_panel.path,self.palette())
        # connecting signals for label update
        self.left_panel.change_label_signal.connect(self.update_label_path)
        self.right_panel.change_label_signal.connect(self.update_label_path)
        
        # widgets placement
        layout.addWidget(self.left_panel_path_label, 0, 0)  # Row 0, Column 0
        layout.addWidget(self.right_panel_path_label, 0, 1)  # Row 0, Column 1

        layout.addWidget(self.left_panel, 1, 0)  # Row 0, Column 0
        layout.addWidget(self.right_panel, 1, 1)  # Row 0, Column 1
        self.setLayout(layout)
