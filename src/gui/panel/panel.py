from PyQt6.QtWidgets import(
    QListWidget,
    QListWidgetItem,
)
from PyQt6.QtCore import pyqtSignal, QObject,Qt
from system_api import KEY
from system_api import SystemAPI
from .colors import *

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

        # FIXME - Move in init_function to know that these fields exists
        self.files_list = files_list
        self.directories_list = directories_list 

        for d in directories_list:
            item = QListWidgetItem(d)
            item.setForeground(COLOR_EXTENSIONS["folder"])  
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
            self.path = SystemAPI.join(self.path,new_directory)
        else:
            previous_directory = SystemAPI.dirname(self.path) 
            previous_directory_name = SystemAPI.basename(self.path)
            self.path = previous_directory 
    
        self.update()
        files_list = self.directories_list # bad possible optimization process

        if previous_directory_name != None: # meaning we're going backwards
            last_position = files_list.index(previous_directory_name)
            self.setCurrentRow(last_position)
        else:
            self.setCurrentRow(0) # to avoid case when opening new directory it instantly loses focus on list elements
        self.change_label_signal.emit(self.panel_name)

    def get_current_file_or_folder(self):
        return self.currentItem().text()

    def open_folder(self):
        temp_path = SystemAPI.join(self.path,self.currentItem().text())
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

        # Change Left and Right arrow keys to PageUp and PageDown keys
        if event.key() == Qt.Key.Key_Left:
            new_event = type(event)(event.type(), 
                                  Qt.Key.Key_PageUp,
                                  event.modifiers())
            super().keyPressEvent(new_event)
        elif event.key() == Qt.Key.Key_Right:
            new_event = type(event)(event.type(),
                                  Qt.Key.Key_PageDown,
                                  event.modifiers())
            super().keyPressEvent(new_event)

        if (event.key() == KEY.ENTER): 
            self.open_folder()

