from PyQt6.QtWidgets import(QListWidget,QListWidgetItem)
from PyQt6.QtCore import QEvent,pyqtSignal,Qt
import re

from system_api import KEY
from system_api import SystemAPI
from .colors import *
from .quick_search_panel_widget import QuickSearchPanelWidget

# TODO:
# refactor function names due to confusing naming:
#   open_folder()    
#   open_directory()

class Panel(QListWidget):
    change_label_signal = pyqtSignal(str)
    def __init__(self,panel_name,path):
        super().__init__()

        self.panel_name = panel_name
        self.path = path
        self.files_list = None
        self.directories_list = None

        self.update()
        self.setCurrentRow(0) 
        self.itemDoubleClicked.connect(self.open_folder)

        # Hiding scrollbars
        self.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")
        self.horizontalScrollBar().setStyleSheet("QScrollBar {height:0px;}")

        # setting quick list search
        self.quick_search = QuickSearchPanelWidget(self)
        self.quick_search.installEventFilter(self) # TODO: read about installEventFilter
        self.quick_search.textChangedConnect(self.search_items)

        from .change_location_widget import ChangeLocationWidget
        self.change_location = ChangeLocationWidget(self)
        self.change_location.installEventFilter(self)
        self.change_location.returnPressed.connect(self.open_by_path)

        self.change_location_key = KEY.F1 if self.panel_name == "left panel" else KEY.F2
        ALT = Qt.KeyboardModifier.AltModifier
        self.list_of_appliable_keys = [
            KEY.ENTER,
            KEY.LEFT_ARROW,   
            KEY.RIGHT_ARROW,  
            ALT,
            self.change_location_key
        ]

    def eventFilter(self,obj,event):
        if not hasattr(self,'quick_search'):
            return super().eventFilter(obj,event)

        # hiding quick search if ESC is pressed 
        if obj == self.quick_search and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.quick_search.clear()
            self.quick_search.hide()
            self.setFocus()
            return True
        # hiding change_location widget if ESC is pressed 
        if obj == self.change_location and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Escape:
            self.change_location.hide()
            self.setFocus()
            return True

        return super().eventFilter(obj,event)

    def keyPressEvent(self, event):
        if event.key() not in self.list_of_appliable_keys:
            super().keyPressEvent(event)
        # in case we're not focused
        if not self.currentItem(): # if no items means we aren't focused or something else
            return

        if event.key() == self.change_location_key and event.modifiers() == Qt.KeyboardModifier.AltModifier: 
            self.show_change_location()

        # show_quick_search handling. Adding check if text isn't empty. Otherwise it invokes quick_search without text
        if event.modifiers() == Qt.KeyboardModifier.AltModifier and event.text().isprintable() and event.text() != '':
            self.show_quick_search(event.text())
            return 

        # Change Left and Right arrow keys to PageUp and PageDown keys
        if event.key() == Qt.Key.Key_Left:
            new_event = type(event)(event.type(), Qt.Key.Key_PageUp,event.modifiers())
            super().keyPressEvent(new_event)
        if event.key() == Qt.Key.Key_Right:
            new_event = type(event)(event.type(),Qt.Key.Key_PageDown,event.modifiers())
            super().keyPressEvent(new_event)

        if (event.key() == KEY.ENTER): 
            self.open_folder()

    def focusInEvent(self, event):
        self.change_label_signal.emit(self.panel_name)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.change_label_signal.emit(self.panel_name)
        super().focusOutEvent(event)

    # TODO:
    # make so after deletion it goes to next item in the list instead of first one
    # if no items left just use setCurrentRow(0)
    # maybe somehow use previous location before deletion?
    def update(self):
        self.clear()
        files_list,directories_list = SystemAPI.get_files_and_directories_list(self.path)
        self.files_list = files_list
        self.directories_list = directories_list 

        for d in directories_list:
            item = QListWidgetItem(d)
            item.setForeground(COLOR_EXTENSIONS["folder"])  
            self.addItem(item)

        for f in files_list:
            item = QListWidgetItem(f)
            color = None
            
            extension = re.search(r"\.[a-zA-Z0-9]*$",f)
            if extension != None:
                extension = extension.group().lower() 
            if extension in COLOR_EXTENSIONS.keys():
                color = COLOR_EXTENSIONS[extension]

            if color is None:
                color = COLOR_EXTENSIONS["default"]

            item.setForeground(color)  
            self.addItem(item)
        # workaround to get focus after deletion
        self.setCurrentRow(0) 

    def open_by_path(self,path):
        self.path = path
        self.update()
        self.change_location.hide()
        self.setCurrentRow(0)
        self.change_location.hide()
        self.setFocus()

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
            if previous_directory_name in files_list:
                last_position = files_list.index(previous_directory_name)
            else: 
                last_position = 0
            self.setCurrentRow(last_position)
        else:
            self.setCurrentRow(0) # to avoid case when opening new directory it instantly loses focus on list elements
        self.change_label_signal.emit(self.panel_name)

    def get_current_file_or_folder(self):
        return self.currentItem().text()

    def open_folder(self):
        if self.quick_search.hasFocus():
            self.quick_search.clear()
            self.quick_search.hide()
            self.setFocus()

        temp_path = SystemAPI.join(self.path,self.currentItem().text())

        if SystemAPI.is_file(temp_path):
            SystemAPI.open_file_in_editor(temp_path)
        else: 
            self.open_directory(self.currentItem().text())

    def show_change_location(self):
        self.change_location.show()
        x = self.width()//2 - self.quick_search.width()
        y = self.height()//2 - self.quick_search.height()
        self.change_location.move(x,y)
        self.change_location.setFocus()

    def show_quick_search(self, initial_char=""):
        self.quick_search.setText(initial_char)
        self.quick_search.show()
        x = self.width()//2 - self.quick_search.width()
        y = self.height() - self.quick_search.height()
        self.quick_search.move(x,y)
        self.quick_search.setFocus()

    # TODO: quick search bug:
    # if using digits or |? etc characters then it shows the search input empty without those characters which isn't supposed to happen
    def search_items(self, text):
        if text == "": # edge case
            self.quick_search.clear()
            self.quick_search.hide()
            self.setFocus()

        if not text:            
            return
            
        items = [self.item(i) for i in range(self.count())]
        
        for item in items:
            item_text_lower = item.text().lower()
            text_lower = text.lower()
            if item_text_lower.startswith(text_lower):                
                self.setCurrentItem(item)
                self.scrollToItem(item)
                return

        self.quick_search.setText(text[:-1])
