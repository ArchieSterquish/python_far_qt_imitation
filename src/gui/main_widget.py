from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget,QGridLayout,QMessageBox

from . import PanelsWidget
from . import ConsoleInteractionPanel
from . import ButtonsBar
from .dialog import *
from system_api import SystemAPI

class MainWidget(QWidget):
    close_app_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.widget_1 = PanelsWidget()
        self.widget_2 = ConsoleInteractionPanel(self)
        self.widget_3 = ButtonsBar("main widget")

        layout = QGridLayout()
        layout.addWidget(self.widget_1)
        layout.addWidget(self.widget_2)
        layout.addWidget(self.widget_3)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def update_buttons_text(self,key):
        self.widget_3.update_buttons_text(key)

    def get_focused_panel_path(self):
        return self.widget_1.get_focused_panel_path()

    def get_focused_file_or_folder(self):
        return self.widget_1.get_focused_file_or_folder()

    def update_panel(self,focused_panel):
        self.widget_1.update_panel(focused_panel)

    def show_deletion_dialog(self):
        focused_path,focused_panel = self.get_focused_panel_path()
        focused_file_or_folder = self.get_focused_file_or_folder()
        filename = SystemAPI.basename(focused_file_or_folder)
        reply = QMessageBox.question(self, 
                'Deletion Confirmation', 
                f'Are you sure you want to delete {filename}?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                QMessageBox.StandardButton.Yes
        )
        if reply == QMessageBox.StandardButton.Yes: 
            SystemAPI.remove_file_or_directory(focused_file_or_folder)
            self.update_panel(focused_panel)

    def show_input_dialog(self):
        focused_path,focused_panel = self.get_focused_panel_path()

        dialog = MakeFolderDialog(self)  
        dialog.exec()  
        
        # TODO:
        # add multiple_spaces check
        # add check for space in the beginnig
        if dialog.user_input not in ["",None]:
            print(f'user input: {dialog.user_input}')
            result = SystemAPI.make_directory(focused_path,dialog.user_input)
            if result != None:
                ErrorDialog(self,result)
                return
            self.update_panel(focused_panel)

    def closeEvent(self,event):
        self.close_app_signal.emit("")
        event.ignore()

